import logging
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTabWidget, QLabel, QStatusBar
from PySide6.QtCore import Slot
from app.config import AppConfig
from app.ui.style import Style
from app.ui.dashboard import DashboardWidget
from app.ui.packets import PacketsWidget
from app.network.interfaces import get_network_interfaces
from app.workers.stats_worker import StatsWorker
from app.workers.packet_worker import PacketWorker, SCAPY_AVAILABLE
from app.models.traffic import ThroughputStats, PacketSummary

logger = logging.getLogger("NetworkTrafficMonitor")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = AppConfig()
        self.setWindowTitle(self.config.APP_NAME)
        self.resize(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        self.setStyleSheet(Style.DARK_STYLESHEET)

        self.stats_worker = None
        self.packet_worker = None
        self.monitoring_active = False
        self.monitoring_paused = False

        self.setup_ui()
        self.refresh_interfaces()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)

        self.interface_combo = QComboBox()
        self.interface_combo.currentIndexChanged.connect(self.on_interface_changed)
        controls_layout.addWidget(self.interface_combo)

        self.btn_refresh = QPushButton("Refresh Interfaces")
        self.btn_refresh.clicked.connect(self.refresh_interfaces)
        controls_layout.addWidget(self.btn_refresh)

        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(self.start_monitoring)
        controls_layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_monitoring)
        controls_layout.addWidget(self.btn_stop)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.setEnabled(False)
        self.btn_pause.clicked.connect(self.toggle_pause)
        controls_layout.addWidget(self.btn_pause)

        self.btn_clear = QPushButton("Clear Stats")
        self.btn_clear.clicked.connect(self.clear_statistics)
        controls_layout.addWidget(self.btn_clear)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        self.tabs = QTabWidget()
        self.dashboard = DashboardWidget()
        self.packets = PacketsWidget()

        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.packets, "Packet Logs")
        main_layout.addWidget(self.tabs)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        if not SCAPY_AVAILABLE:
            self.status_bar.showMessage("Scapy not found. Packet logging is disabled.")
        else:
            self.status_bar.showMessage("Ready.")

    def refresh_interfaces(self):
        current_name = self.interface_combo.currentData()
        self.interface_combo.clear()
        
        self.interfaces = get_network_interfaces()
        for idx, iface in enumerate(self.interfaces):
            status_symbol = "Active" if iface.status else "Inactive"
            display_str = f"{iface.display_name} ({status_symbol})"
            self.interface_combo.addItem(display_str, iface.name)
            
            if current_name and iface.name == current_name:
                self.interface_combo.setCurrentIndex(idx)

        if self.interface_combo.count() > 0 and self.interface_combo.currentIndex() == -1:
            self.interface_combo.setCurrentIndex(0)

    def on_interface_changed(self):
        index = self.interface_combo.currentIndex()
        if index < 0 or index >= len(self.interfaces):
            return
            
        selected_iface = self.interfaces[index]
        self.dashboard.update_interface_info(selected_iface)
        
        if self.monitoring_active:
            self.stop_monitoring()
            self.start_monitoring()

    def start_monitoring(self):
        index = self.interface_combo.currentIndex()
        if index < 0:
            return

        selected_iface = self.interfaces[index]
        self.monitoring_active = True
        self.monitoring_paused = False

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_pause.setEnabled(True)
        self.btn_pause.setText("Pause")
        self.interface_combo.setEnabled(False)
        self.btn_refresh.setEnabled(False)

        self.stats_worker = StatsWorker(selected_iface.name, self.config.DEFAULT_INTERVAL_MS)
        self.stats_worker.stats_updated.connect(self.on_stats_updated)
        self.stats_worker.error_occurred.connect(self.on_worker_error)
        self.stats_worker.start()

        if SCAPY_AVAILABLE:
            self.packet_worker = PacketWorker(selected_iface.name)
            self.packet_worker.packet_captured.connect(self.on_packet_captured)
            self.packet_worker.error_occurred.connect(self.on_packet_worker_error)
            self.packet_worker.start()

        self.status_bar.showMessage(f"Monitoring active on {selected_iface.display_name}...")
        logger.info(f"Started monitoring on interface: {selected_iface.name}")

    def stop_monitoring(self):
        self.monitoring_active = False
        
        if self.stats_worker:
            self.stats_worker.stop()
            self.stats_worker.wait()
            self.stats_worker = None

        if self.packet_worker:
            self.packet_worker.stop()
            self.packet_worker.wait()
            self.packet_worker = None

        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_pause.setEnabled(False)
        self.btn_pause.setText("Pause")
        self.interface_combo.setEnabled(True)
        self.btn_refresh.setEnabled(True)
        
        self.status_bar.showMessage("Monitoring stopped.")
        logger.info("Stopped monitoring.")

    def toggle_pause(self):
        if not self.monitoring_active:
            return

        if self.monitoring_paused:
            self.monitoring_paused = False
            self.btn_pause.setText("Pause")
            if self.stats_worker:
                self.stats_worker.set_paused(False)
            self.status_bar.showMessage("Monitoring resumed.")
            logger.info("Resumed monitoring.")
        else:
            self.monitoring_paused = True
            self.btn_pause.setText("Resume")
            if self.stats_worker:
                self.stats_worker.set_paused(True)
            self.status_bar.showMessage("Monitoring paused.")
            logger.info("Paused monitoring.")

    def clear_statistics(self):
        self.dashboard.clear_stats()
        self.packets.clear()
        logger.info("Cleared statistics and history.")

    @Slot(ThroughputStats)
    def on_stats_updated(self, stats: ThroughputStats):
        self.dashboard.update_stats(stats)

    @Slot(PacketSummary)
    def on_packet_captured(self, packet: PacketSummary):
        self.packets.add_packet(packet)

    @Slot(str)
    def on_worker_error(self, err_msg: str):
        logger.error(f"Stats worker error: {err_msg}")
        self.status_bar.showMessage(f"Error: {err_msg}")
        self.stop_monitoring()

    @Slot(str)
    def on_packet_worker_error(self, err_msg: str):
        logger.warning(f"Packet worker error (pcap might not be available): {err_msg}")
        self.status_bar.showMessage("Packet capture failed or needs admin rights. Only stats monitoring is active.")
        if self.packet_worker:
            self.packet_worker.stop()
            self.packet_worker = None

    def closeEvent(self, event):
        self.stop_monitoring()
        event.accept()
