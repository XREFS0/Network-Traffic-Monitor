import time
from typing import Optional
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from app.models.traffic import PacketSummary

try:
    from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, conf
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

class PacketWorker(QThread):
    packet_captured = Signal(PacketSummary)
    error_occurred = Signal(str)

    def __init__(self, interface_name: str):
        super().__init__()
        self._interface_name = interface_name
        self._is_running = True
        self._mutex = QMutex()

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False

    def run(self):
        if not SCAPY_AVAILABLE:
            self.error_occurred.emit("Scapy is not installed.")
            return

        try:
            scapy_iface = None
            for iface in conf.ifaces.values():
                if iface.name == self._interface_name or iface.description == self._interface_name:
                    scapy_iface = iface
                    break
            
            if not scapy_iface:
                scapy_iface = self._interface_name

            def stop_check(pkt) -> bool:
                with QMutexLocker(self._mutex):
                    return not self._is_running

            def packet_callback(packet):
                try:
                    self._parse_packet(packet)
                except Exception:
                    pass

            sniff(
                iface=scapy_iface,
                prn=packet_callback,
                store=False,
                stop_filter=stop_check,
                timeout=1.0
            )

        except Exception as e:
            self.error_occurred.emit(str(e))

    def _parse_packet(self, packet):
        proto_name = "Unknown"
        src_ip = "Unknown"
        dest_ip = "Unknown"
        src_port: Optional[int] = None
        dest_port: Optional[int] = None
        size = len(packet)

        if IP in packet:
            src_ip = packet[IP].src
            dest_ip = packet[IP].dst
        elif IPv6 in packet:
            src_ip = packet[IPv6].src
            dest_ip = packet[IPv6].dst
        else:
            return

        if TCP in packet:
            proto_name = "TCP"
            src_port = packet[TCP].sport
            dest_port = packet[TCP].dport
            if src_port == 80 or dest_port == 80:
                proto_name = "HTTP"
            elif src_port == 443 or dest_port == 443:
                proto_name = "HTTPS/TLS"
        elif UDP in packet:
            proto_name = "UDP"
            src_port = packet[UDP].sport
            dest_port = packet[UDP].dport
            if src_port == 53 or dest_port == 53:
                proto_name = "DNS"
        elif ICMP in packet:
            proto_name = "ICMP"

        summary = PacketSummary(
            protocol=proto_name,
            source_ip=src_ip,
            dest_ip=dest_ip,
            source_port=src_port,
            dest_port=dest_port,
            size=size,
            timestamp=time.time()
        )
        self.packet_captured.emit(summary)
