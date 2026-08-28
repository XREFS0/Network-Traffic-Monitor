import time
import psutil
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from app.models.traffic import ThroughputStats

class StatsWorker(QThread):
    stats_updated = Signal(ThroughputStats)
    error_occurred = Signal(str)

    def __init__(self, interface_name: str, interval_ms: int = 1000):
        super().__init__()
        self._interface_name = interface_name
        self._interval_s = interval_ms / 1000.0
        self._is_running = True
        self._is_paused = False
        self._mutex = QMutex()
        
        self._prev_bytes_sent = 0
        self._prev_bytes_recv = 0
        self._prev_packets_sent = 0
        self._prev_packets_recv = 0
        self._prev_time = 0.0

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False

    def set_paused(self, paused: bool):
        with QMutexLocker(self._mutex):
            self._is_paused = paused

    def run(self):
        try:
            initial_stats = psutil.net_io_counters(pernic=True)
            if self._interface_name not in initial_stats:
                self.error_occurred.emit(f"Interface {self._interface_name} not found.")
                return
            
            interface_counters = initial_stats[self._interface_name]
            self._prev_bytes_sent = interface_counters.bytes_sent
            self._prev_bytes_recv = interface_counters.bytes_recv
            self._prev_packets_sent = interface_counters.packets_sent
            self._prev_packets_recv = interface_counters.packets_recv
            self._prev_time = time.monotonic()
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize monitoring: {str(e)}")
            return

        while True:
            time.sleep(self._interval_s)
            
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    break
                paused = self._is_paused

            if paused:
                self._prev_time = time.monotonic()
                try:
                    counters = psutil.net_io_counters(pernic=True).get(self._interface_name)
                    if counters:
                        self._prev_bytes_sent = counters.bytes_sent
                        self._prev_bytes_recv = counters.bytes_recv
                        self._prev_packets_sent = counters.packets_sent
                        self._prev_packets_recv = counters.packets_recv
                except Exception:
                    pass
                continue

            try:
                io_stats = psutil.net_io_counters(pernic=True)
                if self._interface_name not in io_stats:
                    self.error_occurred.emit(f"Interface {self._interface_name} disconnected.")
                    break
                
                counters = io_stats[self._interface_name]
                curr_time = time.monotonic()
                time_delta = curr_time - self._prev_time
                
                if time_delta <= 0:
                    time_delta = self._interval_s

                bytes_sent_per_sec = (counters.bytes_sent - self._prev_bytes_sent) / time_delta
                bytes_recv_per_sec = (counters.bytes_recv - self._prev_bytes_recv) / time_delta
                packets_sent_per_sec = (counters.packets_sent - self._prev_packets_sent) / time_delta
                packets_recv_per_sec = (counters.packets_recv - self._prev_packets_recv) / time_delta

                stats = ThroughputStats(
                    bytes_sent=counters.bytes_sent,
                    bytes_recv=counters.bytes_recv,
                    bytes_sent_per_sec=max(0.0, bytes_sent_per_sec),
                    bytes_recv_per_sec=max(0.0, bytes_recv_per_sec),
                    packets_sent=counters.packets_sent,
                    packets_recv=counters.packets_recv,
                    packets_sent_per_sec=max(0.0, packets_sent_per_sec),
                    packets_recv_per_sec=max(0.0, packets_recv_per_sec),
                    errors_in=counters.errin,
                    errors_out=counters.errout,
                    drop_in=counters.dropin,
                    drop_out=counters.dropout
                )

                self._prev_bytes_sent = counters.bytes_sent
                self._prev_bytes_recv = counters.bytes_recv
                self._prev_packets_sent = counters.packets_sent
                self._prev_packets_recv = counters.packets_recv
                self._prev_time = curr_time

                self.stats_updated.emit(stats)

            except Exception as e:
                self.error_occurred.emit(f"Error during stats polling: {str(e)}")
                break
