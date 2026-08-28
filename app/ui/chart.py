from collections import deque
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath
from PySide6.QtCore import Qt
from app.config import AppConfig
from app.utils.formatting import format_bytes_rate

class ThroughputChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = AppConfig()
        self.history_len = self.config.CHART_HISTORY_LENGTH
        self.download_history = deque([0.0] * self.history_len, maxlen=self.history_len)
        self.upload_history = deque([0.0] * self.history_len, maxlen=self.history_len)
        self.setMinimumHeight(220)

    def add_sample(self, download_bps: float, upload_bps: float):
        self.download_history.append(download_bps)
        self.upload_history.append(upload_bps)
        self.update()

    def clear_data(self):
        self.download_history = deque([0.0] * self.history_len, maxlen=self.history_len)
        self.upload_history = deque([0.0] * self.history_len, maxlen=self.history_len)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        padding_left = 60
        padding_right = 20
        padding_top = 20
        padding_bottom = 30

        chart_width = width - padding_left - padding_right
        chart_height = height - padding_top - padding_bottom

        painter.fillRect(0, 0, width, height, QColor(self.config.PANEL_COLOR))

        painter.setPen(QPen(QColor(self.config.BORDER_COLOR), 1))
        painter.drawRect(padding_left, padding_top, chart_width, chart_height)

        max_val = max(max(self.download_history), max(self.upload_history), 1024.0)

        grid_lines = 4
        painter.setFont(QFont("Consolas", 8))
        for i in range(grid_lines + 1):
            y = padding_top + chart_height - int((i / grid_lines) * chart_height)
            
            painter.setPen(QPen(QColor(self.config.GRID_COLOR), 1, Qt.DashLine))
            painter.drawLine(padding_left, y, padding_left + chart_width, y)

            val = (i / grid_lines) * max_val
            label = format_bytes_rate(val)
            painter.setPen(QColor(self.config.TEXT_SECONDARY))
            painter.drawText(10, y + 4, label)

        num_samples = self.history_len
        col_width = chart_width / (num_samples - 1)

        dl_path = QPainterPath()
        ul_path = QPainterPath()

        for idx in range(num_samples):
            x = padding_left + int(idx * col_width)
            
            dl_y_val = self.download_history[idx]
            dl_norm = dl_y_val / max_val
            dl_y = padding_top + chart_height - int(dl_norm * chart_height)

            ul_y_val = self.upload_history[idx]
            ul_norm = ul_y_val / max_val
            ul_y = padding_top + chart_height - int(ul_norm * chart_height)

            if idx == 0:
                dl_path.moveTo(x, dl_y)
                ul_path.moveTo(x, ul_y)
            else:
                dl_path.lineTo(x, dl_y)
                ul_path.lineTo(x, ul_y)

        painter.setPen(QPen(QColor(self.config.DOWNLOAD_COLOR), 2, Qt.SolidLine))
        painter.drawPath(dl_path)

        painter.setPen(QPen(QColor(self.config.UPLOAD_COLOR), 2, Qt.SolidLine))
        painter.drawPath(ul_path)
