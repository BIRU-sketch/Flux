"""Reusable widgets used across pages"""

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsBlurEffect
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QFormLayout, QDateTimeEdit, QDialogButtonBox,QPushButton
from PyQt5.QtCore import QDateTime
class GlassCard(QFrame):
    """A translucent rounded card with depth - the base building block for glass UI"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

class StatCard(GlassCard):
    def __init__(self, label, value, value_color=None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        label_widget = QLabel(label.upper())
        label_widget.setObjectName("statLabel")
        layout.addWidget(label_widget)

        value_widget = QLabel(value)
        value_widget.setObjectName("statValue")
        if value_color:
            value_widget.setStyleSheet(f"color: {value_color}; font-size: 26px; font-weight: 600;")
        layout.addWidget(value_widget)


class StatusPill(QLabel):
    """Small rounded badge for status (done/running/failed/pending)"""

    COLORS = {
        "done": ("#4ade80", "rgba(74, 222, 128, 0.15)"),
        "running": ("#facc15", "rgba(250, 204, 21, 0.15)"),
        "failed": ("#f87171", "rgba(248, 113, 113, 0.15)"),
        "pending": ("#a5b4fc", "rgba(165, 180, 252, 0.15)"),
    }

    def __init__(self, status="pending"):
        super().__init__(status)
        self.set_status(status)
        self.setAlignment(Qt.AlignCenter)

    def set_status(self, status):
        text_color, bg_color = self.COLORS.get(status, self.COLORS["pending"])
        self.setText(status)
        self.setStyleSheet(f"""
            color: {text_color};
            background-color: {bg_color};
            border-radius: 10px;
            padding: 2px 10px;
            font-size: 11px;
            font-weight: 500;
        """)


class HistoryRow(GlassCard):
    """One compact row for a history/recent-task entry"""
    def __init__(self, title, status="done", time_ago="now"):
        super().__init__()
        self.setStyleSheet("QFrame#glassCard { padding: 0px; }")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.85);")
        layout.addWidget(title_label)

        layout.addStretch()

        pill = StatusPill(status)
        layout.addWidget(pill)

        time_label = QLabel(time_ago)
        time_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.35);")
        layout.addWidget(time_label)
class GlowBlob(QWidget):
    """Soft colored glow circle for ambient background depth"""
    def __init__(self, color="#6366f1", size=300, opacity=60, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: {size // 2}px;
        """)

        blur = QGraphicsBlurEffect(self)
        blur.setBlurRadius(80)
        self.setGraphicsEffect(blur)

        # apply opacity via stylesheet rgba instead for reliability
        from PyQt5.QtGui import QColor
        c = QColor(color)
        self.setStyleSheet(f"""
            background-color: rgba({c.red()}, {c.green()}, {c.blue()}, {opacity});
            border-radius: {size // 2}px;
        """)
        self.lower()  # send behind other widgets
from PyQt5.QtWidgets import QLineEdit, QComboBox, QCheckBox


class SettingsSection(GlassCard):
    """A glass card with a title + vertical content area, used in Settings"""
    def __init__(self, title):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 16, 18, 16)
        self.layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.85);")
        self.layout.addWidget(title_label)

    def add_widget(self, widget):
        self.layout.addWidget(widget)


def styled_input(placeholder="", is_password=False):
    field = QLineEdit()
    field.setPlaceholderText(placeholder)
    if is_password:
        field.setEchoMode(QLineEdit.Password)
    field.setStyleSheet("""
        QLineEdit {
            background-color: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 9px 12px;
            color: rgba(255,255,255,0.85);
            font-size: 13px;
        }
        QLineEdit:focus {
            border: 1px solid #6366f1;
        }
    """)
    return field


def styled_combobox(options):
    box = QComboBox()
    box.addItems(options)
    box.setStyleSheet("""
        QComboBox {
            background-color: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 9px 12px;
            color: rgba(255,255,255,0.85);
            font-size: 13px;
        }
        QComboBox::drop-down { border: none; }
    """)
    return box


def styled_checkbox(label, checked=True):
    box = QCheckBox(label)
    box.setChecked(checked)
    box.setStyleSheet("""
        QCheckBox {
            color: rgba(255,255,255,0.7);
            font-size: 13px;
            spacing: 8px;
        }
    """)
    return box
class TaskListItem(GlassCard):
    """Single scheduled task row with toggle + delete"""
    def __init__(self, task, on_toggle, on_delete):
        super().__init__()
        self.task = task

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)

        info_layout = QVBoxLayout()
        name_label = QLabel(task["name"])
        name_label.setStyleSheet("font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.85);")
        info_layout.addWidget(name_label)

        meta_text = f"{task['time']}  ·  {task['recurrence']}"
        meta_label = QLabel(meta_text)
        meta_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.4);")
        info_layout.addWidget(meta_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        toggle = styled_checkbox("", checked=task.get("enabled", True))
        toggle.stateChanged.connect(lambda state: on_toggle(task["id"], state))
        layout.addWidget(toggle)

        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(26, 26)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(248,113,113,0.1);
                color: #f87171;
                border: none;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: rgba(248,113,113,0.2); }
        """)
        delete_btn.clicked.connect(lambda: on_delete(task["id"]))
        layout.addWidget(delete_btn)


class AddTaskDialog(QDialog):
    """Popup form to create a new scheduled task"""
    def __init__(self, parent=None, default_date=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule a Task")
        self.setFixedWidth(380)
        self.setStyleSheet("""
            QDialog { background-color: #131b2e; }
            QLabel { color: rgba(255,255,255,0.7); font-size: 12px; }
        """)

        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.name_input = styled_input("e.g. Backup my files")
        layout.addRow("Task", self.name_input)

        self.prompt_input = styled_input("Natural language instruction for Flux")
        layout.addRow("Instruction", self.prompt_input)

        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(default_date or QDateTime.currentDateTime())
        self.datetime_input.setCalendarPopup(True)
        self.datetime_input.setStyleSheet("""
            QDateTimeEdit {
                background-color: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 6px 10px;
                color: rgba(255,255,255,0.85);
            }
        """)
        layout.addRow("Date & time", self.datetime_input)

        self.recurrence_select = styled_combobox(["Once", "Daily", "Weekly", "Monthly"])
        layout.addRow("Repeat", self.recurrence_select)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border-radius: 8px;
                padding: 6px 16px;
            }
        """)
        layout.addRow(buttons)

    def get_data(self):
        return {
            "name": self.name_input.text() or "Untitled task",
            "prompt": self.prompt_input.text(),
            "time": self.datetime_input.dateTime().toString("MMM d, yyyy hh:mm AP"),
            "recurrence": self.recurrence_select.currentText(),
        }
class TemplateCard(GlassCard):
    """Card for a saved task template with run/edit/delete actions"""
    def __init__(self, template, on_run, on_edit, on_delete):
        super().__init__()
        self.template = template

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        # Top row: name + category tag
        top_row = QHBoxLayout()
        name_label = QLabel(template["name"])
        name_label.setStyleSheet("font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.9);")
        top_row.addWidget(name_label)
        top_row.addStretch()

        tag = QLabel(template["category"])
        tag.setStyleSheet("""
            background-color: rgba(99,102,241,0.18);
            color: #a5b4fc;
            border-radius: 10px;
            padding: 2px 10px;
            font-size: 10.5px;
            font-weight: 500;
        """)
        top_row.addWidget(tag)
        layout.addLayout(top_row)

        # Prompt preview
        prompt_label = QLabel(template["prompt"])
        prompt_label.setWordWrap(True)
        prompt_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.45); line-height: 1.4;")
        prompt_label.setMaximumHeight(40)
        layout.addWidget(prompt_label)

        # Bottom row: usage count + actions
        bottom_row = QHBoxLayout()
        usage_label = QLabel(f"Used {template.get('usage_count', 0)} times")
        usage_label.setStyleSheet("font-size: 10.5px; color: rgba(255,255,255,0.3);")
        bottom_row.addWidget(usage_label)
        bottom_row.addStretch()

        run_btn = QPushButton("Run")
        run_btn.setCursor(Qt.PointingHandCursor)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #a855f7);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 5px 14px;
                font-size: 11.5px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #7678f5; }
        """)
        run_btn.clicked.connect(lambda: on_run(template))
        bottom_row.addWidget(run_btn)

        edit_btn = QPushButton("✎")
        edit_btn.setFixedSize(24, 24)
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.06);
                color: rgba(255,255,255,0.7);
                border: none;
                border-radius: 12px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.12); }
        """)
        edit_btn.clicked.connect(lambda: on_edit(template))
        bottom_row.addWidget(edit_btn)

        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(248,113,113,0.1);
                color: #f87171;
                border: none;
                border-radius: 12px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: rgba(248,113,113,0.2); }
        """)
        delete_btn.clicked.connect(lambda: on_delete(template["id"]))
        bottom_row.addWidget(delete_btn)

        layout.addLayout(bottom_row)


class AddTemplateDialog(QDialog):
    """Popup form to create/edit a template"""
    def __init__(self, parent=None, template=None):
        super().__init__(parent)
        self.setWindowTitle("Save Template" if not template else "Edit Template")
        self.setFixedWidth(380)
        self.setStyleSheet("""
            QDialog { background-color: #131b2e; }
            QLabel { color: rgba(255,255,255,0.7); font-size: 12px; }
        """)

        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.name_input = styled_input("e.g. Organize Downloads")
        self.prompt_input = styled_input("The instruction Flux will run")
        self.category_select = styled_combobox(["File Management", "Email", "System", "Web", "Custom"])

        if template:
            self.name_input.setText(template["name"])
            self.prompt_input.setText(template["prompt"])
            idx = self.category_select.findText(template["category"])
            if idx >= 0:
                self.category_select.setCurrentIndex(idx)

        layout.addRow("Name", self.name_input)
        layout.addRow("Instruction", self.prompt_input)
        layout.addRow("Category", self.category_select)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border-radius: 8px;
                padding: 6px 16px;
            }
        """)
        layout.addRow(buttons)

    def get_data(self):
        return {
            "name": self.name_input.text() or "Untitled template",
            "prompt": self.prompt_input.text(),
            "category": self.category_select.currentText(),
        }