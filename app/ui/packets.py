from collections import deque
from datetime import datetime
from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from app.models.traffic import PacketSummary
from app.config import AppConfig

class PacketTableModel(QAbstractTableModel):
    def __init__(self, max_rows: int = 500, parent=None):
        super().__init__(parent)
        self.packets = deque(maxlen=max_rows)
        self.headers = ["Time", "Protocol", "Source", "Port", "Destination", "Port", "Size (B)"]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.packets)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.packets)):
            return None

        packet: PacketSummary = self.packets[index.row()]

        if role == Qt.DisplayRole:
            col = index.column()
            if col == 0:
                dt = datetime.fromtimestamp(packet.timestamp)
                return dt.strftime("%H:%M:%S.%f")[:-3]
            elif col == 1:
                return packet.protocol
            elif col == 2:
                return packet.source_ip
            elif col == 3:
                return str(packet.source_port) if packet.source_port is not None else "-"
            elif col == 4:
                return packet.dest_ip
            elif col == 5:
                return str(packet.dest_port) if packet.dest_port is not None else "-"
            elif col == 6:
                return str(packet.size)
        elif role == Qt.TextAlignmentRole:
            col = index.column()
            if col in (3, 5, 6):
                return int(Qt.AlignRight | Qt.AlignVCenter)
            return int(Qt.AlignLeft | Qt.AlignVCenter)

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def add_packet(self, packet: PacketSummary):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.packets.appendleft(packet)
        self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self.packets.clear()
        self.endResetModel()

class PacketsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = AppConfig()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table_view = QTableView()
        self.model = PacketTableModel(max_rows=self.config.MAX_PACKETS_HISTORY)
        self.table_view.setModel(self.model)
        
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(3, QHeaderView.Interactive)
        header.setSectionResizeMode(5, QHeaderView.Interactive)
        header.setSectionResizeMode(6, QHeaderView.Interactive)
        
        self.table_view.setColumnWidth(0, 120)
        self.table_view.setColumnWidth(3, 80)
        self.table_view.setColumnWidth(5, 80)
        self.table_view.setColumnWidth(6, 80)
        
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setShowGrid(True)
        self.table_view.setAlternatingRowColors(False)
        
        layout.addWidget(self.table_view)

    def add_packet(self, packet: PacketSummary):
        self.model.add_packet(packet)

    def clear(self):
        self.model.clear()
