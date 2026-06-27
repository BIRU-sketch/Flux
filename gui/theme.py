"""Theme manager - QSS stylesheets for dark/light mode"""

DARK_THEME = """


QWidget#sidebar {
    background-color: rgba(255, 255, 255, 10);
    border-right: 1px solid rgba(255, 255, 255, 20);
}

QPushButton#navItem {
    background-color: transparent;
    border: none;
    border-radius: 10px;
    color: rgba(255, 255, 255, 140);
    font-size: 13px;
    text-align: left;
    padding: 10px 14px;
}

QPushButton#navItem:hover {
    background-color: rgba(255, 255, 255, 15);
}

QPushButton#navItemActive {
    background-color: rgba(99, 102, 241, 40);
    border: none;
    border-radius: 10px;
    color: rgba(255, 255, 255, 240);
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    padding: 10px 14px;
}

QFrame#glassCard {
    background-color: rgba(255, 255, 255, 10);
    border: 1px solid rgba(255, 255, 255, 20);
    border-radius: 14px;
}

QLabel#titleLabel {
    color: rgba(255, 255, 255, 240);
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
}
QLabel#subtitleLabel {
    color: rgba(255, 255, 255, 100);
    font-size: 13px;
}

QLabel#statValue {
    color: rgba(255, 255, 255, 240);
    font-size: 26px;
    font-weight: 600;
}

QLabel#statLabel {
    color: rgba(255, 255, 255, 100);
    font-size: 11px;
    text-transform: uppercase;
}

QTextEdit#taskInput {
    background-color: transparent;
    border: none;
    color: rgba(255, 255, 255, 230);
    font-size: 14px;
}

QPushButton#runButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #a855f7);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 600;
    font-size: 13px;
    padding: 10px 20px;
}

QPushButton#runButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7678f5, stop:1 #b968fa);
}
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f7;
}

QWidget#sidebar {
    background-color: rgba(0, 0, 0, 5);
    border-right: 1px solid rgba(0, 0, 0, 15);
}

QPushButton#navItem {
    background-color: transparent;
    border: none;
    border-radius: 10px;
    color: rgba(0, 0, 0, 140);
    font-size: 13px;
    text-align: left;
    padding: 10px 14px;
}

QPushButton#navItem:hover {
    background-color: rgba(0, 0, 0, 10);
}

QPushButton#navItemActive {
    background-color: rgba(99, 102, 241, 30);
    border: none;
    border-radius: 10px;
    color: rgba(0, 0, 0, 220);
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    padding: 10px 14px;
}

QFrame#glassCard {
    background-color: rgba(255, 255, 255, 180);
    border: 1px solid rgba(0, 0, 0, 15);
    border-radius: 14px;
}

QLabel#titleLabel {
    color: rgba(0, 0, 0, 230);
    font-size: 24px;
    font-weight: 600;
}

QLabel#subtitleLabel {
    color: rgba(0, 0, 0, 120);
    font-size: 13px;
}

QLabel#statValue {
    color: rgba(0, 0, 0, 230);
    font-size: 26px;
    font-weight: 600;
}

QLabel#statLabel {
    color: rgba(0, 0, 0, 120);
    font-size: 11px;
    text-transform: uppercase;
}

QTextEdit#taskInput {
    background-color: transparent;
    border: none;
    color: rgba(0, 0, 0, 220);
    font-size: 14px;
}

QPushButton#runButton {
    background-color: #6366f1;
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 500;
    font-size: 13px;
    padding: 10px 18px;
}

QPushButton#runButton:hover {
    background-color: #7678f5;
}
"""


class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.current = "dark"

    def apply(self, theme_name="dark"):
        self.current = theme_name
        stylesheet = DARK_THEME if theme_name == "dark" else LIGHT_THEME
        self.app.setStyleSheet(stylesheet)

    def toggle(self):
        new_theme = "light" if self.current == "dark" else "dark"
        self.apply(new_theme)
        return new_theme