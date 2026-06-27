import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from gui.sidebar import Sidebar
from gui.theme import ThemeManager
from gui.backend_bridge import BackendBridge
from gui.pages import DashboardPage
from gui.pages import HistoryPage
from gui.pages import DashboardPage, HistoryPage, SettingsPage, ScheduledPage, TemplatesPage
class MainWindow(QMainWindow):
    def __init__(self, theme_manager, backend):
        super().__init__()
        self.setWindowTitle("Flux")
        self.resize(1100, 720)

        self.theme_manager = theme_manager
        self.backend = backend

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar(on_nav=self.switch_page)
        layout.addWidget(self.sidebar)

        self.pages_stack = QStackedWidget()
        layout.addWidget(self.pages_stack)

        self.pages = {}
        self._register_pages()

        self.setCentralWidget(central)
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor(10, 14, 26))
        gradient.setColorAt(0.5, QColor(19, 27, 46))
        gradient.setColorAt(1.0, QColor(13, 18, 32))
        painter.fillRect(self.rect(), gradient)
        super().paintEvent(event)
    def _register_pages(self):

        self.pages["dashboard"] = DashboardPage(self.backend)
        self.pages_stack.addWidget(self.pages["dashboard"])
        self.pages["history"] = HistoryPage(self.backend)
        self.pages_stack.addWidget(self.pages["history"])
        self.pages["settings"] = SettingsPage(self.backend, self.theme_manager)
        self.pages_stack.addWidget(self.pages["settings"])
        self.pages["scheduled"] = ScheduledPage(self.backend)
        self.pages_stack.addWidget(self.pages["scheduled"])
        self.pages["templates"] = TemplatesPage(self.backend)
        self.pages_stack.addWidget(self.pages["templates"])
        # Pages will be added here one at a time as we build them
        pass

    def switch_page(self, page_id):
        if page_id in self.pages:
            self.pages_stack.setCurrentWidget(self.pages[page_id])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    theme_manager = ThemeManager(app)
    theme_manager.apply("dark")

    backend = BackendBridge()
    window = MainWindow(theme_manager, backend)
    window.show()

    sys.exit(app.exec())