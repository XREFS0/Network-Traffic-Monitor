class Style:
    DARK_STYLESHEET = """
    QMainWindow {
        background-color: #121214;
    }
    
    QWidget {
        color: #e4e4e7;
        font-family: 'Segoe UI', -apple-system, Roboto, Helvetica, sans-serif;
        font-size: 13px;
    }
    
    QFrame#panel {
        background-color: #1a1a1e;
        border: 1px solid #2d2d34;
        border-radius: 4px;
    }
    
    QLabel#title {
        font-size: 18px;
        font-weight: bold;
        color: #e4e4e7;
    }
    
    QLabel#subtitle {
        font-size: 12px;
        color: #a1a1aa;
    }
    
    QLabel#metric-value {
        font-size: 22px;
        font-weight: bold;
        font-family: Consolas, monospace;
    }
    
    QLabel#metric-label {
        font-size: 11px;
        text-transform: uppercase;
        font-weight: 600;
        color: #a1a1aa;
    }
    
    QComboBox {
        background-color: #1a1a1e;
        border: 1px solid #2d2d34;
        border-radius: 4px;
        padding: 6px 12px;
        min-width: 200px;
    }
    
    QComboBox::drop-down {
        border: 0px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #1a1a1e;
        border: 1px solid #2d2d34;
        selection-background-color: #2d2d34;
    }
    
    QPushButton {
        background-color: #1a1a1e;
        border: 1px solid #2d2d34;
        border-radius: 4px;
        padding: 6px 16px;
        font-weight: 600;
    }
    
    QPushButton:hover {
        background-color: #2d2d34;
    }
    
    QPushButton:pressed {
        background-color: #27272a;
    }
    
    QPushButton:disabled {
        color: #52525b;
        border-color: #1a1a1e;
    }
    
    QTableView {
        background-color: #1a1a1e;
        border: 1px solid #2d2d34;
        gridline-color: #2a2a30;
        selection-background-color: #2d2d34;
    }
    
    QHeaderView::section {
        background-color: #161619;
        color: #a1a1aa;
        padding: 6px;
        border: 1px solid #2d2d34;
        font-weight: bold;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #121214;
        width: 10px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background: #2d2d34;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #3f3f46;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QTabWidget::pane {
        border: 1px solid #2d2d34;
        background-color: #121214;
    }
    
    QTabBar::tab {
        background-color: #1a1a1e;
        border: 1px solid #2d2d34;
        border-bottom-color: transparent;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        padding: 8px 16px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: #121214;
        border-bottom-color: #121214;
        font-weight: bold;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #27272a;
    }
    """
