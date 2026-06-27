"""Sidebar navigation widget"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt


NAV_ITEMS = [
    ("dashboard", "Dashboard"),
    ("history", "History"),
    ("templates", "Templates"),
    ("scheduled", "Scheduled"),
]

NAV_ITEMS_BOTTOM = [
    ("settings", "Settings"),
    ("about", "About"),
]


class Sidebar(QWidget):
    def __init__(self, on_nav):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self.on_nav = on_nav
        self.nav_buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(2)

        logo = QLabel("⚡ Flux")
        logo.setStyleSheet("font-size: 17px; font-weight: 600; padding: 0 8px 20px 8px;")
        layout.addWidget(logo)

        for page_id, label in NAV_ITEMS:
            btn = self._make_nav_button(page_id, label)
            layout.addWidget(btn)

        layout.addStretch()

        for page_id, label in NAV_ITEMS_BOTTOM:
            btn = self._make_nav_button(page_id, label)
            layout.addWidget(btn)

        status = QLabel("●  Agent ready")
        status.setStyleSheet("color: #4ade80; font-size: 11px; padding: 12px 8px 0 8px;")
        layout.addWidget(status)

        self.set_active("dashboard")

    def _make_nav_button(self, page_id, label):
        btn = QPushButton(label)
        btn.setObjectName("navItem")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: self._handle_click(page_id))
        self.nav_buttons[page_id] = btn
        return btn

    def _handle_click(self, page_id):
        self.set_active(page_id)
        self.on_nav(page_id)

    def set_active(self, page_id):
        for pid, btn in self.nav_buttons.items():
            btn.setObjectName("navItemActive" if pid == page_id else "navItem")
            btn.setStyleSheet("")