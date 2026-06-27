"""All pages live here - add more classes as we build them"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
)
from PyQt5.QtCore import Qt

from gui.components import GlassCard, StatCard, HistoryRow
from gui.components import GlassCard, StatCard, HistoryRow, GlowBlob
from gui.components import (
    GlassCard, StatCard, HistoryRow, GlowBlob,
    SettingsSection, styled_input, styled_combobox, styled_checkbox,
    TaskListItem, AddTaskDialog,
    TemplateCard, AddTemplateDialog
)
from PyQt5.QtWidgets import QGridLayout, QScrollArea
from PyQt5.QtWidgets import QCalendarWidget, QListWidget
from PyQt5.QtCore import QDate
import uuid

from gui.components import (
    GlassCard, StatCard, HistoryRow, GlowBlob,
    SettingsSection, styled_input, styled_combobox, styled_checkbox,
    TaskListItem, AddTaskDialog
)
class SettingsPage(QWidget):
    def __init__(self, backend, theme_manager):
        super().__init__()
        self.backend = backend
        self.theme_manager = theme_manager

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 32, 36, 32)
        layout.setSpacing(18)

        title = QLabel("Settings")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        subtitle = QLabel("Configure AI, email, safety and appearance")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)

        content = QVBoxLayout()
        content.setSpacing(14)
        content.setContentsMargins(0, 8, 0, 0)

        # --- AI Model section ---
        ai_section = SettingsSection("AI Model")
        self.model_select = styled_combobox(["Local model (offline)", "Google Generative AI", "OpenRouter"])
        ai_section.add_widget(self.model_select)
        self.api_key_input = styled_input("API key (if using cloud)", is_password=True)
        ai_section.add_widget(self.api_key_input)
        content.addWidget(ai_section)

        # --- Email section ---
        email_section = SettingsSection("Email")
        self.email_input = styled_input("your@email.com")
        email_section.add_widget(self.email_input)
        self.email_password_input = styled_input("App password", is_password=True)
        email_section.add_widget(self.email_password_input)
        content.addWidget(email_section)

        # --- Safety & Permissions ---
        safety_section = SettingsSection("Safety & Permissions")
        self.confirm_destructive = styled_checkbox("Confirm before destructive actions (delete, overwrite)", checked=True)
        safety_section.add_widget(self.confirm_destructive)
        self.whitelist_only = styled_checkbox("Restrict to whitelisted bash commands", checked=True)
        safety_section.add_widget(self.whitelist_only)
        content.addWidget(safety_section)

        # --- Theme ---
        theme_section = SettingsSection("Theme")
        self.dark_mode_toggle = styled_checkbox("Dark mode", checked=True)
        self.dark_mode_toggle.stateChanged.connect(self.handle_theme_toggle)
        theme_section.add_widget(self.dark_mode_toggle)
        content.addWidget(theme_section)

        # --- Save button ---
        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("runButton")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.handle_save)
        content.addWidget(save_btn, alignment=Qt.AlignLeft)

        layout.addLayout(content)
        layout.addStretch()

    def handle_theme_toggle(self, state):
        new_theme = "dark" if state == Qt.Checked else "light"
        self.theme_manager.apply(new_theme)

    def handle_save(self):
        # TODO: wire this to backend_bridge to persist settings
        settings = {
            "ai_model": self.model_select.currentText(),
            "api_key": self.api_key_input.text(),
            "email": self.email_input.text(),
            "email_password": self.email_password_input.text(),
            "confirm_destructive": self.confirm_destructive.isChecked(),
            "whitelist_only": self.whitelist_only.isChecked(),
        }
        print("Settings saved:", settings)  # placeholder until persistence is built
class DashboardPage(QWidget):
    def __init__(self, backend):
        super().__init__()
        from gui.components import GlowBlob
        # Ambient glow blobs (positioned behind content)
        self.glow1 = GlowBlob(color="#6366f1", size=350, opacity=50, parent=self)
        self.glow1.move(-100, -100)
        self.glow2 = GlowBlob(color="#a855f7", size=400, opacity=30, parent=self)
        self.glow2.move(700, 400)
        self.backend = backend

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 32, 36, 32)
        layout.setSpacing(22)

        # --- Header ---
        header_row = QHBoxLayout()
        header_text = QVBoxLayout()

        title = QLabel("Welcome back")
        title.setObjectName("titleLabel")
        header_text.addWidget(title)

        subtitle = QLabel("What should Flux take care of today?")
        subtitle.setObjectName("subtitleLabel")
        header_text.addWidget(subtitle)

        header_row.addLayout(header_text)
        header_row.addStretch()
        layout.addLayout(header_row)

        # --- Task input card ---
        input_card = GlassCard()
        input_layout = QHBoxLayout(input_card)
        input_layout.setContentsMargins(16, 16, 16, 16)

        self.task_input = QTextEdit()
        self.task_input.setObjectName("taskInput")
        self.task_input.setPlaceholderText(
            "Ask Flux to do something... e.g. 'organize my downloads' "
            "or 'schedule a backup every night at 2am'"
        )
        self.task_input.setFixedHeight(70)
        input_layout.addWidget(self.task_input)

        run_button = QPushButton("Run")
        run_button.setObjectName("runButton")
        run_button.setCursor(Qt.PointingHandCursor)
        run_button.clicked.connect(self.handle_submit)
        input_layout.addWidget(run_button, alignment=Qt.AlignBottom)

        layout.addWidget(input_card)

        # --- Stats row ---
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        stats_row.addWidget(StatCard("Tasks today", "12"))
        stats_row.addWidget(StatCard("Success rate", "98%", value_color="#4ade80"))
        stats_row.addWidget(StatCard("Time saved", "8h 24m"))
        layout.addLayout(stats_row)

        # --- Execution status card ---
        self.status_card = GlassCard()
        status_layout = QVBoxLayout(self.status_card)
        status_layout.setContentsMargins(18, 16, 18, 16)

        status_header = QHBoxLayout()
        status_label = QLabel("Live execution")
        status_label.setStyleSheet("font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.8);")
        status_header.addWidget(status_label)
        status_header.addStretch()

        self.status_pill = QLabel("Idle")
        self.status_pill.setStyleSheet("""
            color: #4ade80; background-color: rgba(74,222,128,0.15);
            border-radius: 10px; padding: 3px 10px; font-size: 11.5px; font-weight: 500;
        """)
        status_header.addWidget(self.status_pill)
        status_layout.addLayout(status_header)

        self.plan_steps_label = QLabel("No active task. Submit one above to get started.")
        self.plan_steps_label.setWordWrap(True)
        self.plan_steps_label.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.5); margin-top: 8px;")
        status_layout.addWidget(self.plan_steps_label)

        layout.addWidget(self.status_card)

        # --- Recent tasks ---
        recent_label = QLabel("Recent")
        recent_label.setStyleSheet("font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.6);")
        layout.addWidget(recent_label)

        self.recent_list_layout = QVBoxLayout()
        self.recent_list_layout.setSpacing(6)
        layout.addLayout(self.recent_list_layout)

        layout.addStretch()

        self.refresh_recent()

    def handle_submit(self):
        prompt = self.task_input.toPlainText().strip()
        if not prompt:
            return

        self.status_pill.setText("Running")
        self.status_pill.setStyleSheet("""
            color: #facc15; background-color: rgba(250,204,21,0.15);
            border-radius: 10px; padding: 3px 10px; font-size: 11.5px; font-weight: 500;
        """)
        self.plan_steps_label.setText("Planning task...")

        result = self.backend.submit_task(prompt)

        if result.get("success"):
            self.status_pill.setText("Idle")
            self.status_pill.setStyleSheet("""
                color: #4ade80; background-color: rgba(74,222,128,0.15);
                border-radius: 10px; padding: 3px 10px; font-size: 11.5px; font-weight: 500;
            """)
            self.plan_steps_label.setText("Task completed.")
            self.task_input.clear()
            self.refresh_recent()
        else:
            self.status_pill.setText("Failed")
            self.status_pill.setStyleSheet("""
                color: #f87171; background-color: rgba(248,113,113,0.15);
                border-radius: 10px; padding: 3px 10px; font-size: 11.5px; font-weight: 500;
            """)
            self.plan_steps_label.setText(f"Error: {result.get('error', 'Unknown error')}")

    def refresh_recent(self):
        # Clear existing rows
        while self.recent_list_layout.count():
            item = self.recent_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        history = self.backend.get_history()
        recent = history[-5:][::-1]  # last 5, newest first

        if not recent:
            placeholder = QLabel("No tasks yet.")
            placeholder.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 13px;")
            self.recent_list_layout.addWidget(placeholder)
            return

        for entry in recent:
            row = HistoryRow(entry["prompt"], status="done", time_ago="just now")
            self.recent_list_layout.addWidget(row)
class HistoryPage(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 32, 36, 32)
        layout.setSpacing(18)

        title = QLabel("History")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        subtitle = QLabel("All tasks Flux has run")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)

        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(6)
        layout.addLayout(self.list_layout)

        layout.addStretch()

        self.refresh()

    def refresh(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        history = self.backend.get_history()

        if not history:
            placeholder = QLabel("No tasks yet.")
            placeholder.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 13px;")
            self.list_layout.addWidget(placeholder)
            return

        for entry in reversed(history):
            status = "done" if entry.get("results") else "pending"
            row = HistoryRow(entry["prompt"], status=status, time_ago="recently")
            self.list_layout.addWidget(row)

    def showEvent(self, event):
        # Refresh every time the page becomes visible
        self.refresh()
        super().showEvent(event)
class ScheduledPage(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.tasks = []  # each: {id, name, prompt, time, recurrence, enabled, date(QDate)}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 32, 36, 32)
        layout.setSpacing(18)

        # --- Header ---
        header_row = QHBoxLayout()
        header_text = QVBoxLayout()
        title = QLabel("Scheduled Tasks")
        title.setObjectName("titleLabel")
        header_text.addWidget(title)
        subtitle = QLabel("Automate Flux to run on its own")
        subtitle.setObjectName("subtitleLabel")
        header_text.addWidget(subtitle)
        header_row.addLayout(header_text)
        header_row.addStretch()

        add_btn = QPushButton("+ New Task")
        add_btn.setObjectName("runButton")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.open_add_dialog)
        header_row.addWidget(add_btn, alignment=Qt.AlignVCenter)

        layout.addLayout(header_row)

        # --- Filters ---
        filter_row = QHBoxLayout()
        self.filter_buttons = {}
        for f in ["All", "Today", "Upcoming", "Recurring"]:
            btn = QPushButton(f)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.05);
                    color: rgba(255,255,255,0.6);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 16px;
                    padding: 5px 14px;
                    font-size: 12px;
                }
                QPushButton:checked {
                    background-color: rgba(99,102,241,0.25);
                    color: white;
                    border: 1px solid #6366f1;
                }
            """)
            btn.clicked.connect(lambda checked, name=f: self.apply_filter(name))
            self.filter_buttons[f] = btn
            filter_row.addWidget(btn)
        filter_row.addStretch()
        self.filter_buttons["All"].setChecked(True)
        self.active_filter = "All"
        layout.addLayout(filter_row)

        # --- Main content: calendar + task list ---
        content_row = QHBoxLayout()
        content_row.setSpacing(16)

        # Calendar card
        calendar_card = GlassCard()
        calendar_layout = QVBoxLayout(calendar_card)
        calendar_layout.setContentsMargins(12, 12, 12, 12)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.clicked.connect(self.on_date_selected)
        self.calendar.setStyleSheet("""
    QCalendarWidget {
        background-color: transparent;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 6px;
    }
    QCalendarWidget QToolButton {
        color: rgba(255,255,255,0.85);
        background-color: transparent;
        font-size: 13px;
        font-weight: 600;
        border-radius: 8px;
        padding: 6px 10px;
        margin: 2px;
    }
    QCalendarWidget QToolButton:hover {
        background-color: rgba(99,102,241,0.25);
    }
    QCalendarWidget QToolButton::menu-indicator { image: none; width:0; }
    QCalendarWidget QMenu {
        background-color: #1a2238;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    QCalendarWidget QSpinBox {
        color: white;
        background-color: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 6px;
        padding: 2px 6px;
    }
    QCalendarWidget QAbstractItemView {
        background-color: #131b2e;
        alternate-background-color: #131b2e;
        color: rgba(255,255,255,0.75);
        selection-background-color: #6366f1;
        selection-color: white;
        outline: none;
        font-size: 12.5px;
        border-radius: 12px;
    }
    QCalendarWidget QAbstractItemView:disabled {
        color: rgba(255,255,255,0.15);
    }
    QCalendarWidget QWidget {
        background-color: #131b2e;
    }    """)
        from PyQt5.QtGui import QTextCharFormat, QColor, QFont
        weekday_format = QTextCharFormat()
        weekday_format.setForeground(QColor("rgba(255,255,255,0.5)" if False else "#8b93b8"))
        for day in [Qt.Monday, Qt.Tuesday, Qt.Wednesday, Qt.Thursday, Qt.Friday, Qt.Saturday, Qt.Sunday]:
            self.calendar.setWeekdayTextFormat(day, weekday_format)
        today_format = QTextCharFormat()
        today_format.setForeground(QColor("#a5b4fc"))
        today_format.setFontWeight(QFont.Bold)
        self.calendar.setDateTextFormat(QDate.currentDate(), today_format)
        calendar_layout.addWidget(self.calendar)
        content_row.addWidget(calendar_card, stretch=3)

        # Task list panel for selected date
        self.tasks_panel = GlassCard()
        tasks_panel_layout = QVBoxLayout(self.tasks_panel)
        tasks_panel_layout.setContentsMargins(16, 16, 16, 16)
        tasks_panel_layout.setSpacing(10)

        self.selected_date_label = QLabel("Today")
        self.selected_date_label.setStyleSheet("font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.85);")
        tasks_panel_layout.addWidget(self.selected_date_label)

        self.task_list_layout = QVBoxLayout()
        self.task_list_layout.setSpacing(6)
        tasks_panel_layout.addLayout(self.task_list_layout)
        tasks_panel_layout.addStretch()

        content_row.addWidget(self.tasks_panel, stretch=2)
        layout.addLayout(content_row)

        self.selected_date = QDate.currentDate()
        self.refresh_task_list()

    def open_add_dialog(self):
        from PyQt5.QtCore import QDateTime
        dialog = AddTaskDialog(self, default_date=QDateTime(self.selected_date))
        if dialog.exec_():
            data = dialog.get_data()
            task = {
                "id": str(uuid.uuid4()),
                "name": data["name"],
                "prompt": data["prompt"],
                "time": data["time"],
                "recurrence": data["recurrence"],
                "enabled": True,
                "date": self.selected_date,
            }
            self.tasks.append(task)
            self.refresh_task_list()
            self.update_calendar_marks()

    def on_date_selected(self, date):
        self.selected_date = date
        self.selected_date_label.setText(date.toString("MMMM d, yyyy"))
        self.refresh_task_list()

    def apply_filter(self, name):
        self.active_filter = name
        for fname, btn in self.filter_buttons.items():
            btn.setChecked(fname == name)
        self.refresh_task_list()

    def get_filtered_tasks(self):
        if self.active_filter == "Today":
            return [t for t in self.tasks if t["date"] == QDate.currentDate()]
        elif self.active_filter == "Upcoming":
            return [t for t in self.tasks if t["date"] >= QDate.currentDate()]
        elif self.active_filter == "Recurring":
            return [t for t in self.tasks if t["recurrence"] != "Once"]
        else:
            return [t for t in self.tasks if t["date"] == self.selected_date]

    def refresh_task_list(self):
        while self.task_list_layout.count():
            item = self.task_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        tasks = self.get_filtered_tasks()

        if not tasks:
            placeholder = QLabel("No tasks for this view.")
            placeholder.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 12px;")
            self.task_list_layout.addWidget(placeholder)
            return

        for task in tasks:
            row = TaskListItem(task, self.handle_toggle, self.handle_delete)
            self.task_list_layout.addWidget(row)

    def handle_toggle(self, task_id, state):
        for t in self.tasks:
            if t["id"] == task_id:
                t["enabled"] = bool(state)

    def handle_delete(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.refresh_task_list()
        self.update_calendar_marks()

    def update_calendar_marks(self):
        # Placeholder for future: paint colored dots on dates with tasks
        pass
class TemplatesPage(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.templates = [
            {"id": str(uuid.uuid4()), "name": "Organize Downloads", "prompt": "Organize my Downloads folder by file type into subfolders", "category": "File Management", "usage_count": 14},
            {"id": str(uuid.uuid4()), "name": "Daily System Report", "prompt": "Send me an email with CPU, RAM and disk usage", "category": "Email", "usage_count": 7},
            {"id": str(uuid.uuid4()), "name": "Clean Temp Files", "prompt": "Delete temp files older than 7 days", "category": "System", "usage_count": 3},
        ]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 32, 36, 32)
        layout.setSpacing(18)

        self.glow1 = GlowBlob(color="#6366f1", size=320, opacity=30, parent=self)
        self.glow1.move(-100, -80)
        self.glow2 = GlowBlob(color="#a855f7", size=360, opacity=25, parent=self)
        self.glow2.move(800, 450)

        # --- Header ---
        header_row = QHBoxLayout()
        header_text = QVBoxLayout()
        title = QLabel("Templates")
        title.setObjectName("titleLabel")
        header_text.addWidget(title)
        subtitle = QLabel("Save and reuse your favorite automations")
        subtitle.setObjectName("subtitleLabel")
        header_text.addWidget(subtitle)
        header_row.addLayout(header_text)
        header_row.addStretch()

        add_btn = QPushButton("+ New Template")
        add_btn.setObjectName("runButton")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.open_add_dialog)
        header_row.addWidget(add_btn, alignment=Qt.AlignVCenter)
        layout.addLayout(header_row)

        # --- Search bar ---
        self.search_input = styled_input("Search templates...")
        self.search_input.textChanged.connect(self.refresh_grid)
        layout.addWidget(self.search_input)

        # --- Category filter pills ---
        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)
        self.filter_buttons = {}
        for f in ["All", "File Management", "Email", "System", "Web", "Custom"]:
            btn = QPushButton(f)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.05);
                    color: rgba(255,255,255,0.6);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 14px;
                    padding: 6px 16px;
                    font-size: 12px;
                }
                QPushButton:hover { background-color: rgba(255,255,255,0.1); }
                QPushButton:checked {
                    background-color: rgba(99,102,241,0.25);
                    color: white;
                    border: 1px solid #6366f1;
                }
            """)
            btn.clicked.connect(lambda checked, name=f: self.apply_filter(name))
            self.filter_buttons[f] = btn
            filter_row.addWidget(btn)
        filter_row.addStretch()
        self.filter_buttons["All"].setChecked(True)
        self.active_filter = "All"
        layout.addLayout(filter_row)

        # --- Scrollable grid of template cards ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        grid_container = QWidget()
        grid_container.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setSpacing(12)
        scroll.setWidget(grid_container)

        layout.addWidget(scroll)

        self.refresh_grid()

    def apply_filter(self, name):
        self.active_filter = name
        for fname, btn in self.filter_buttons.items():
            btn.setChecked(fname == name)
        self.refresh_grid()

    def get_filtered_templates(self):
        templates = self.templates
        if self.active_filter != "All":
            templates = [t for t in templates if t["category"] == self.active_filter]
        search_text = self.search_input.text().strip().lower()
        if search_text:
            templates = [t for t in templates if search_text in t["name"].lower() or search_text in t["prompt"].lower()]
        return templates

    def refresh_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        templates = self.get_filtered_templates()

        if not templates:
            placeholder = QLabel("No templates found.")
            placeholder.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 13px;")
            self.grid_layout.addWidget(placeholder, 0, 0)
            return

        columns = 2
        for i, template in enumerate(templates):
            card = TemplateCard(template, self.handle_run, self.handle_edit, self.handle_delete)
            row, col = divmod(i, columns)
            self.grid_layout.addWidget(card, row, col)

    def open_add_dialog(self):
        dialog = AddTemplateDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            template = {
                "id": str(uuid.uuid4()),
                "name": data["name"],
                "prompt": data["prompt"],
                "category": data["category"],
                "usage_count": 0,
            }
            self.templates.append(template)
            self.refresh_grid()

    def handle_run(self, template):
        result = self.backend.submit_task(template["prompt"])
        if result.get("success"):
            template["usage_count"] = template.get("usage_count", 0) + 1
            self.refresh_grid()

    def handle_edit(self, template):
        dialog = AddTemplateDialog(self, template=template)
        if dialog.exec_():
            data = dialog.get_data()
            template["name"] = data["name"]
            template["prompt"] = data["prompt"]
            template["category"] = data["category"]
            self.refresh_grid()

    def handle_delete(self, template_id):
        self.templates = [t for t in self.templates if t["id"] != template_id]
        self.refresh_grid()