from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    DEFAULT_INTERVAL_MS: int = 1000
    CHART_HISTORY_LENGTH: int = 60
    MAX_PACKETS_HISTORY: int = 500
    APP_NAME: str = "Network Traffic Monitor"
    WINDOW_WIDTH: int = 1000
    WINDOW_HEIGHT: int = 700

    BG_COLOR: str = "#121214"
    PANEL_COLOR: str = "#1a1a1e"
    BORDER_COLOR: str = "#2d2d34"
    TEXT_PRIMARY: str = "#e4e4e7"
    TEXT_SECONDARY: str = "#a1a1aa"
    
    DOWNLOAD_COLOR: str = "#0ea5e9"
    UPLOAD_COLOR: str = "#f43f5e"
    GRID_COLOR: str = "#2a2a30"
