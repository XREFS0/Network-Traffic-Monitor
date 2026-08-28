from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from app.ui.chart import ThroughputChart
from app.models.traffic import InterfaceInfo, ThroughputStats
from app.utils.formatting import format_bytes_rate, format_bytes_total

class MetricCard(QFrame):
    def __init__(self, title: str, value_color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        
        self.label = QLabel(title)
        self.label.setObjectName("metric-label")
        
        self.value = QLabel("0.00 B/s")
        self.value.setObjectName("metric-value")
        self.value.setStyleSheet(f"color: {value_color};")
        
        layout.addWidget(self.label)
        layout.addWidget(self.value)

class InfoRow(QWidget):
    def __init__(self, label_text: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        
        self.label = QLabel(label_text)
        self.label.setStyleSheet("color: #a1a1aa; font-weight: 500;")
        
        self.value = QLabel("N/A")
        self.value.setAlignment(Qt.AlignRight)
        self.value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        layout.addWidget(self.label)
        layout.addWidget(self.value)

    def set_value(self, val: str):
        self.value.setText(val if val else "N/A")

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)
        
        left_layout = QVBoxLayout()
        left_layout.setSpacing(16)
        
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(12)
        
        self.dl_card = MetricCard("Download Speed", "#0ea5e9")
        self.ul_card = MetricCard("Upload Speed", "#f43f5e")
        self.total_dl_card = MetricCard("Total Downloaded", "#e4e4e7")
        self.total_ul_card = MetricCard("Total Uploaded", "#e4e4e7")
        self.pps_card = MetricCard("Packets / Sec", "#e4e4e7")
        
        metrics_grid.addWidget(self.dl_card, 0, 0)
        metrics_grid.addWidget(self.ul_card, 0, 1)
        metrics_grid.addWidget(self.total_dl_card, 0, 2)
        metrics_grid.addWidget(self.total_ul_card, 1, 0)
        metrics_grid.addWidget(self.pps_card, 1, 1)
        
        left_layout.addLayout(metrics_grid)
        
        self.chart = ThroughputChart()
        left_layout.addWidget(self.chart)
        
        main_layout.addLayout(left_layout, stretch=3)
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("panel")
        self.sidebar.setFixedWidth(260)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(8)
        
        sidebar_title = QLabel("Interface Details")
        sidebar_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #e4e4e7; margin-bottom: 8px;")
        sidebar_layout.addWidget(sidebar_title)
        
        self.info_status = InfoRow("Status")
        self.info_ipv4 = InfoRow("IPv4 Address")
        self.info_ipv6 = InfoRow("IPv6 Address")
        self.info_mac = InfoRow("MAC Address")
        self.info_speed = InfoRow("Link Speed")
        
        sidebar_layout.addWidget(self.info_status)
        sidebar_layout.addWidget(self.info_ipv4)
        sidebar_layout.addWidget(self.info_ipv6)
        sidebar_layout.addWidget(self.info_mac)
        sidebar_layout.addWidget(self.info_speed)
        
        sidebar_layout.addStretch()
        
        main_layout.addWidget(self.sidebar, stretch=1)

    def update_interface_info(self, info: InterfaceInfo):
        status_text = "Active" if info.status else "Inactive"
        self.info_status.set_value(status_text)
        self.info_ipv4.set_value(info.ipv4_address)
        self.info_ipv6.set_value(info.ipv6_address)
        self.info_mac.set_value(info.mac_address)
        
        if info.link_speed_mbps:
            self.info_speed.set_value(f"{info.link_speed_mbps} Mbps")
        else:
            self.info_speed.set_value("N/A")

    def update_stats(self, stats: ThroughputStats):
        self.dl_card.value.setText(format_bytes_rate(stats.bytes_recv_per_sec))
        self.ul_card.value.setText(format_bytes_rate(stats.bytes_sent_per_sec))
        self.total_dl_card.value.setText(format_bytes_total(stats.bytes_recv))
        self.total_ul_card.value.setText(format_bytes_total(stats.bytes_sent))
        
        total_pps = stats.packets_recv_per_sec + stats.packets_sent_per_sec
        self.pps_card.value.setText(f"{total_pps:.1f} P/s")
        
        self.chart.add_sample(stats.bytes_recv_per_sec, stats.bytes_sent_per_sec)

    def clear_stats(self):
        self.dl_card.value.setText("0.00 B/s")
        self.ul_card.value.setText("0.00 B/s")
        self.total_dl_card.value.setText("0.00 B")
        self.total_ul_card.value.setText("0.00 B")
        self.pps_card.value.setText("0.0 P/s")
        self.chart.clear_data()
