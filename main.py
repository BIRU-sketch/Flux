
import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Dict, List, Optional, Tuple


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FluxApp(ctk.CTk):
    """Flux UI shell built with CustomTkinter.

    Designed to be easy to integrate with an external backend:
    - set_status(text, color=None)
    - set_step(text)
    - add_history_item(title, subtitle, age_text=None, accent=None)
    - clear_history()
    - set_dashboard_stats(...)
    - set_activity_log(...)
    """

    def __init__(self):
        super().__init__()

        self.title("Flux")
        self.geometry("600x600")
        self.minsize(1200, 780)
        self.configure(fg_color="#000000")

        self._nav_buttons: Dict[str, ctk.CTkButton] = {}
        self._history_cards: List[ctk.CTkFrame] = []

        self._build_layout()
        self.show_page("automate")
        self.after(100, self._demo_seed)  # remove when connected to backend

    # -----------------------------
    # Layout
    # -----------------------------
    def _build_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_topbar()
        self._build_content()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color="#0a0a0a",
            border_width=0,
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(20, weight=1)

        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="ew", padx=22, pady=(24, 10))
        brand.grid_columnconfigure(0, weight=1)

        self.logo = ctk.CTkLabel(
            brand,
            text="Flux",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color="#f5f5f5",
        )
        self.logo.grid(row=0, column=0, sticky="w")

        self.subtitle = ctk.CTkLabel(
            brand,
            text="Automation workspace",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#8f8f8f",
        )
        self.subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(18, 10))
        nav_frame.grid_columnconfigure(0, weight=1)

        self._add_nav_button(nav_frame, "dashboard", "Dashboard", 0)
        self._add_nav_button(nav_frame, "automate", "Automate", 1)
        self._add_nav_button(nav_frame, "history", "History", 2)
        self._add_nav_button(nav_frame, "plugins", "Plugins", 3)
        self._add_nav_button(nav_frame, "settings", "Settings", 4)

        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.grid(row=21, column=0, sticky="sew", padx=18, pady=18)
        footer.grid_columnconfigure(0, weight=1)

        self.backend_status = ctk.CTkLabel(
            footer,
            text="Backend: disconnected",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="#9f9f9f",
        )
        self.backend_status.grid(row=0, column=0, sticky="ew")

        self.quick_tip = ctk.CTkLabel(
            footer,
            text="Plug your planner/executor into the page callbacks.",
            anchor="w",
            justify="left",
            wraplength=208,
            font=ctk.CTkFont(size=11),
            text_color="#6f6f6f",
        )
        self.quick_tip.grid(row=1, column=0, sticky="ew", pady=(8, 0))

    def _add_nav_button(self, parent, key: str, text: str, row: int):
        btn = ctk.CTkButton(
            parent,
            text=text,
            height=42,
            corner_radius=12,
            fg_color="#111111",
            hover_color="#1a1a1a",
            border_width=1,
            border_color="#303030",
            anchor="w",
            command=lambda k=key: self.show_page(k),
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        btn.grid(row=row, column=0, sticky="ew", pady=6)
        self._nav_buttons[key] = btn

    def _build_topbar(self):
        self.topbar = ctk.CTkFrame(
            self,
            height=78,
            corner_radius=0,
            fg_color="#000000",
        )
        self.topbar.grid(row=0, column=1, sticky="nsew")
        self.topbar.grid_propagate(False)
        self.topbar.grid_columnconfigure(0, weight=1)

        title_wrap = ctk.CTkFrame(self.topbar, fg_color="transparent")
        title_wrap.grid(row=0, column=0, sticky="w", padx=22, pady=18)

        self.page_title = ctk.CTkLabel(
            title_wrap,
            text="Dashboard",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#f0f0f0",
        )
        self.page_title.grid(row=0, column=0, sticky="w")

        self.page_subtitle = ctk.CTkLabel(
            title_wrap,
            text="Monitor your automations and jump between tools.",
            font=ctk.CTkFont(size=12),
            text_color="#8d8d8d",
        )
        self.page_subtitle.grid(row=1, column=0, sticky="w", pady=(3, 0))

        actions = ctk.CTkFrame(self.topbar, fg_color="transparent")
        actions.grid(row=0, column=1, sticky="e", padx=18, pady=18)

        self.appearance_btn = ctk.CTkButton(
            actions,
            text="Dark",
            width=120,
            height=40,
            corner_radius=14,
            fg_color="#0f0f0f",
            hover_color="#161616",
            border_width=1,
            border_color="#e9e9e9",
            text_color="#f5f5f5",
            command=self._toggle_appearance,
        )
        self.appearance_btn.grid(row=0, column=0, padx=(0, 10))

        self.settings_btn = ctk.CTkButton(
            actions,
            text="Open Settings",
            width=140,
            height=40,
            corner_radius=14,
            fg_color="#0f0f0f",
            hover_color="#161616",
            border_width=1,
            border_color="#3f77ff",
            text_color="#9ec0ff",
            command=lambda: self.show_page("settings"),
        )
        self.settings_btn.grid(row=0, column=1)

    def _build_content(self):
        self.content = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.content.grid(row=1, column=1, sticky="nsew", padx=(0, 22), pady=(0, 18))
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Scrollable page container
        self.page_container = ctk.CTkScrollableFrame(
            self.content,
            fg_color="#000000",
            border_width=0,
            scrollbar_button_color="#2b2b2b",
            scrollbar_button_hover_color="#444444",
        )
        self.page_container.grid(row=0, column=0, sticky="nsew")
        self.page_container.grid_columnconfigure(0, weight=1)

        self.pages: Dict[str, ctk.CTkFrame] = {}
        for key in ("dashboard", "automate", "history", "plugins", "settings"):
            frame = ctk.CTkFrame(self.page_container, fg_color="transparent")
            frame.grid_columnconfigure(0, weight=1)
            self.pages[key] = frame

        self._build_dashboard_page()
        self._build_automate_page()
        self._build_history_page()
        self._build_plugins_page()
        self._build_settings_page()

    # -----------------------------
    # Shared UI helpers
    # -----------------------------
    def _card(self, parent, height: int = 120, fg: str = "#262626", border: str = "#444444"):
        return ctk.CTkFrame(
            parent,
            height=height,
            corner_radius=18,
            fg_color=fg,
            border_width=1,
            border_color=border,
        )

    def _section_title(self, parent, title: str, subtitle: str = ""):
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            wrap,
            text=title,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#f2f2f2",
        ).grid(row=0, column=0, sticky="w")

        if subtitle:
            ctk.CTkLabel(
                wrap,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color="#9a9a9a",
            ).grid(row=1, column=0, sticky="w", pady=(3, 0))
        return wrap

    def _clear_page_container(self):
        for child in self.page_container.winfo_children():
            child.grid_forget()
            child.pack_forget()

    def show_page(self, key: str):
        if key not in self.pages:
            return

        self._clear_page_container()
        self.pages[key].grid(row=0, column=0, sticky="nsew")

        titles = {
            "dashboard": ("Dashboard", "Overview of your current workflows and system state."),
            "automate": ("Automate", "Describe a task and let Flux orchestrate the steps."),
            "history": ("History", "Track what Flux has done and when."),
            "plugins": ("Plugins", "Connect new capabilities to the execution engine."),
            "settings": ("Settings", "Tune the app, appearance, and integration points."),
        }
        title, subtitle = titles.get(key, ("Flux", ""))

        self.page_title.configure(text=title)
        self.page_subtitle.configure(text=subtitle)

        for btn_key, btn in self._nav_buttons.items():
            if btn_key == key:
                btn.configure(fg_color="#1a1a1a", border_color="#3f77ff", text_color="#d8e6ff")
            else:
                btn.configure(fg_color="#111111", border_color="#303030", text_color="#f0f0f0")

    def _toggle_appearance(self):
        current = ctk.get_appearance_mode().lower()
        new_mode = "Light" if current == "dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.appearance_btn.configure(text=new_mode)

    # -----------------------------
    # Dashboard page
    # -----------------------------
    def _build_dashboard_page(self):
        page = self.pages["dashboard"]
        page.grid_columnconfigure(0, weight=1)

        header = self._section_title(
            page,
            "Dashboard",
            "A quick view of Flux activity, system status, and shortcuts.",
        )
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=(10, 16))

        stats = ctk.CTkFrame(page, fg_color="transparent")
        stats.grid(row=1, column=0, sticky="ew")
        for i in range(4):
            stats.grid_columnconfigure(i, weight=1, uniform="stats")

        self.stat_cards = {}
        stat_data = [
            ("Tasks Today", "12", "Queued and completed jobs"),
            ("Running", "3", "Jobs currently active"),
            ("Success Rate", "98%", "Last 30 executions"),
            ("Connected Tools", "8", "Available actions"),
        ]
        for i, (label, value, note) in enumerate(stat_data):
            card = self._card(stats, height=130)
            card.grid(row=0, column=i, sticky="ew", padx=8, pady=8)
            card.grid_propagate(False)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=18, pady=16)

            v = ctk.CTkLabel(inner, text=value, font=ctk.CTkFont(size=30, weight="bold"))
            v.pack(anchor="w")
            l = ctk.CTkLabel(inner, text=label, font=ctk.CTkFont(size=14, weight="bold"), text_color="#cfcfcf")
            l.pack(anchor="w", pady=(6, 0))
            n = ctk.CTkLabel(inner, text=note, font=ctk.CTkFont(size=12), text_color="#8e8e8e")
            n.pack(anchor="w", pady=(3, 0))
            self.stat_cards[label] = v

        row2 = ctk.CTkFrame(page, fg_color="transparent")
        row2.grid(row=2, column=0, sticky="nsew", pady=(8, 8))
        row2.grid_columnconfigure(0, weight=3)
        row2.grid_columnconfigure(1, weight=2)

        # Quick actions
        qa = self._card(row2, height=250)
        qa.grid(row=0, column=0, sticky="nsew", padx=(8, 10))
        qa.grid_propagate(False)

        qa_inner = ctk.CTkFrame(qa, fg_color="transparent")
        qa_inner.pack(fill="both", expand=True, padx=18, pady=16)
        ctk.CTkLabel(qa_inner, text="Quick Actions", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            qa_inner,
            text="Launch common tasks and open core pages in one click.",
            font=ctk.CTkFont(size=12),
            text_color="#8e8e8e",
        ).pack(anchor="w", pady=(4, 12))

        actions = [
            ("Open Automate", lambda: self.show_page("automate")),
            ("View History", lambda: self.show_page("history")),
            ("Manage Plugins", lambda: self.show_page("plugins")),
            ("Open Settings", lambda: self.show_page("settings")),
        ]
        for text, cmd in actions:
            ctk.CTkButton(
                qa_inner,
                text=text,
                height=38,
                corner_radius=12,
                fg_color="#111111",
                hover_color="#1a1a1a",
                border_width=1,
                border_color="#383838",
                command=cmd,
            ).pack(fill="x", pady=5)

        # System health
        sh = self._card(row2, height=250)
        sh.grid(row=0, column=1, sticky="nsew", padx=(10, 8))
        sh.grid_propagate(False)

        sh_inner = ctk.CTkFrame(sh, fg_color="transparent")
        sh_inner.pack(fill="both", expand=True, padx=18, pady=16)
        ctk.CTkLabel(sh_inner, text="System Health", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        self.health_text = ctk.CTkLabel(
            sh_inner,
            text="Ready",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#65d26e",
        )
        self.health_text.pack(anchor="w", pady=(8, 0))
        self.health_detail = ctk.CTkLabel(
            sh_inner,
            text="No tasks are running right now.",
            font=ctk.CTkFont(size=12),
            text_color="#9a9a9a",
            wraplength=330,
            justify="left",
        )
        self.health_detail.pack(anchor="w", pady=(8, 0))

        self.activity_log = ctk.CTkTextbox(
            sh_inner,
            height=110,
            corner_radius=12,
            fg_color="#141414",
            border_width=1,
            border_color="#2f2f2f",
            text_color="#d9d9d9",
        )
        self.activity_log.pack(fill="both", expand=True, pady=(12, 0))
        self.activity_log.insert("end", "• Flux ready.\n• Waiting for backend events.\n")
        self.activity_log.configure(state="disabled")

        # Recent executions preview on dashboard
        preview_wrap = self._card(page, height=250)
        preview_wrap.grid(row=3, column=0, sticky="ew", padx=8, pady=(10, 4))
        preview_wrap.grid_propagate(False)

        pw = ctk.CTkFrame(preview_wrap, fg_color="transparent")
        pw.pack(fill="both", expand=True, padx=18, pady=16)
        ctk.CTkLabel(pw, text="Recent Executions", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            pw,
            text="Latest runs appear here as your backend reports them.",
            font=ctk.CTkFont(size=12),
            text_color="#8e8e8e",
        ).pack(anchor="w", pady=(4, 10))

        self.dashboard_preview_list = ctk.CTkScrollableFrame(
            pw,
            height=150,
            fg_color="#141414",
            corner_radius=12,
            border_width=1,
            border_color="#2f2f2f",
        )
        self.dashboard_preview_list.pack(fill="both", expand=True)

    # -----------------------------
    # Automate page
    # -----------------------------
    def _build_automate_page(self):
        page = self.pages["automate"]
        page.grid_columnconfigure(0, weight=1)

        header = self._section_title(
            page,
            "What do you want to automate?",
            "Describe a task in natural language and plug the execution engine into the button.",
        )
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=(10, 14))

        composer = ctk.CTkFrame(page, fg_color="transparent")
        composer.grid(row=1, column=0, sticky="ew")
        composer.grid_columnconfigure(0, weight=1)

        self.command_input = ctk.CTkTextbox(
            composer,
            height=145,
            corner_radius=16,
            fg_color="#2c2c2c",
            border_width=1,
            border_color="#505050",
            text_color="#f0f0f0",
        )
        self.command_input.grid(row=0, column=0, sticky="ew", padx=(8, 14))
        self.command_input.insert(
            "end",
            "e.g., 'Organize my Downloads folder' or 'Send me an email with system stats'"
        )

        self.execute_button = ctk.CTkButton(
            composer,
            text="Execute",
            width=180,
            height=145,
            corner_radius=16,
            fg_color="#0d0d0d",
            hover_color="#141414",
            border_width=2,
            border_color="#3f77ff",
            text_color="#9ec0ff",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.on_execute_clicked,
        )
        self.execute_button.grid(row=0, column=1, sticky="e", padx=(14, 8))

        status_row = ctk.CTkFrame(page, fg_color="transparent")
        status_row.grid(row=2, column=0, sticky="ew", pady=(18, 6))
        status_row.grid_columnconfigure((0, 1), weight=1)

        self.status_card = self._card(status_row, height=155)
        self.status_card.grid(row=0, column=0, sticky="ew", padx=(8, 10))
        self.status_card.grid_propagate(False)

        sc = ctk.CTkFrame(self.status_card, fg_color="transparent")
        sc.pack(fill="both", expand=True, padx=18, pady=16)
        ctk.CTkLabel(sc, text="Status", font=ctk.CTkFont(size=15), text_color="#bdbdbd").pack(anchor="w")
        status_line = ctk.CTkFrame(sc, fg_color="transparent")
        status_line.pack(anchor="w", pady=(12, 0))
        self.status_dot = ctk.CTkLabel(status_line, text="●", font=ctk.CTkFont(size=24), text_color="#2b7c1f")
        self.status_dot.pack(side="left", padx=(0, 10))
        self.status_label = ctk.CTkLabel(
            status_line,
            text="Ready",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#f0f0f0",
        )
        self.status_label.pack(side="left")

        self.step_card = self._card(status_row, height=155)
        self.step_card.grid(row=0, column=1, sticky="ew", padx=(10, 8))
        self.step_card.grid_propagate(False)

        st = ctk.CTkFrame(self.step_card, fg_color="transparent")
        st.pack(fill="both", expand=True, padx=18, pady=16)
        ctk.CTkLabel(st, text="Step", font=ctk.CTkFont(size=15), text_color="#bdbdbd").pack(anchor="w")
        self.step_label = ctk.CTkLabel(
            st,
            text="—",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#f0f0f0",
            wraplength=420,
            justify="left",
        )
        self.step_label.pack(anchor="w", pady=(12, 0))

        hist_hdr = ctk.CTkFrame(page, fg_color="transparent")
        hist_hdr.grid(row=3, column=0, sticky="ew", pady=(12, 8), padx=8)
        hist_hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hist_hdr,
            text="Execution history",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        clear_btn = ctk.CTkButton(
            hist_hdr,
            text="Clear",
            width=90,
            height=34,
            corner_radius=10,
            fg_color="#111111",
            hover_color="#1a1a1a",
            border_width=1,
            border_color="#383838",
            command=self.clear_history,
        )
        clear_btn.grid(row=0, column=1, sticky="e")

        self.history_list = ctk.CTkScrollableFrame(
            page,
            height=300,
            fg_color="transparent",
            corner_radius=0,
        )
        self.history_list.grid(row=4, column=0, sticky="nsew", padx=8, pady=(0, 10))
        self.history_list.grid_columnconfigure(0, weight=1)

    def on_execute_clicked(self):
        command = self.command_input.get("1.0", "end").strip()
        if not command:
            messagebox.showinfo("Flux", "Please describe what you want to automate.")
            return

        self.set_status("Queued", color="#d4a017")
        self.set_step("Sending task to backend...")
        self.append_activity(f"Queued: {command}")

        # Hook for external backend:
        # self.execute_callback(command)
        print(f"[Flux UI] Execute clicked: {command}")

    # -----------------------------
    # History page
    # -----------------------------
    def _build_history_page(self):
        page = self.pages["history"]
        page.grid_columnconfigure(0, weight=1)

        header = self._section_title(
            page,
            "History",
            "Search or review previous automations. Hook this up to your storage layer.",
        )
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=(10, 14))

        top = ctk.CTkFrame(page, fg_color="transparent")
        top.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 12))
        top.grid_columnconfigure(0, weight=1)

        self.history_search = ctk.CTkEntry(
            top,
            height=40,
            corner_radius=12,
            placeholder_text="Search history...",
            fg_color="#141414",
            border_width=1,
            border_color="#303030",
        )
        self.history_search.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.history_filter = ctk.CTkOptionMenu(
            top,
            values=["All", "Success", "Queued", "Failed"],
            height=40,
            corner_radius=12,
        )
        self.history_filter.grid(row=0, column=1, sticky="e")

        self.history_feed = ctk.CTkScrollableFrame(
            page,
            height=500,
            fg_color="transparent",
        )
        self.history_feed.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 10))
        self.history_feed.grid_columnconfigure(0, weight=1)

    # -----------------------------
    # Plugins page
    # -----------------------------
    def _build_plugins_page(self):
        page = self.pages["plugins"]
        page.grid_columnconfigure(0, weight=1)

        header = self._section_title(
            page,
            "Plugins",
            "Keep the core stable and add capabilities through modules.",
        )
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=(10, 14))

        plugins_card = self._card(page, height=480)
        plugins_card.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 12))
        plugins_card.grid_propagate(False)

        inner = ctk.CTkFrame(plugins_card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=16)
        inner.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(inner, text="Installed Modules", font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, sticky="w"
        )
        ctk.CTkLabel(
            inner,
            text="Use these cards as placeholders for your backend plugin registry.",
            font=ctk.CTkFont(size=12),
            text_color="#8e8e8e",
        ).grid(row=1, column=0, sticky="w", pady=(4, 12))

        modules = [
            ("Filesystem", "Move, rename, organize, clean up."),
            ("Email", "Send reports and alerts."),
            ("Browser", "Open pages and scrape data."),
            ("System", "Read stats and control processes."),
            ("Cloud", "Sync backups and storage."),
            ("Custom Script", "Run your own Python hooks."),
        ]
        grid = ctk.CTkFrame(inner, fg_color="transparent")
        grid.grid(row=2, column=0, sticky="nsew")
        for i in range(2):
            grid.grid_columnconfigure(i, weight=1)

        for idx, (name, desc) in enumerate(modules):
            r, c = divmod(idx, 2)
            card = self._card(grid, height=120)
            card.grid(row=r, column=c, sticky="ew", padx=6, pady=6)
            card.grid_propagate(False)

            cc = ctk.CTkFrame(card, fg_color="transparent")
            cc.pack(fill="both", expand=True, padx=16, pady=14)
            ctk.CTkLabel(cc, text=name, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(cc, text=desc, font=ctk.CTkFont(size=12), text_color="#8e8e8e").pack(anchor="w", pady=(5, 0))

    # -----------------------------
    # Settings page
    # -----------------------------
    def _build_settings_page(self):
        page = self.pages["settings"]
        page.grid_columnconfigure(0, weight=1)

        header = self._section_title(
            page,
            "Settings",
            "Appearance, execution behavior, and integration options.",
        )
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=(10, 14))

        card = self._card(page, height=560)
        card.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 12))
        card.grid_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        # Appearance
        section1 = ctk.CTkFrame(inner, fg_color="transparent")
        section1.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(section1, text="Appearance", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            section1,
            text="The top-right toggle changes between light and dark mode.",
            font=ctk.CTkFont(size=12),
            text_color="#8e8e8e",
        ).pack(anchor="w", pady=(3, 8))

        self.theme_choice = ctk.CTkOptionMenu(section1, values=["Dark", "Light"], command=self._apply_theme)
        self.theme_choice.set("Dark")
        self.theme_choice.pack(anchor="w")

        # Integration
        section2 = ctk.CTkFrame(inner, fg_color="transparent")
        section2.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(section2, text="Backend Integration", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            section2,
            text="Bind callbacks, status updates, and history events from your executor.",
            font=ctk.CTkFont(size=12),
            text_color="#8e8e8e",
        ).pack(anchor="w", pady=(3, 8))

        self.backend_url_entry = ctk.CTkEntry(
            section2,
            placeholder_text="Optional backend endpoint or local bridge name",
            height=40,
            corner_radius=12,
            fg_color="#141414",
            border_width=1,
            border_color="#303030",
        )
        self.backend_url_entry.pack(fill="x")

        # Controls
        section3 = ctk.CTkFrame(inner, fg_color="transparent")
        section3.pack(fill="x", pady=(18, 0))
        ctk.CTkLabel(section3, text="Execution Behavior", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            section3,
            text="These are UI placeholders now; wire them into your config layer later.",
            font=ctk.CTkFont(size=12),
            text_color="#8e8e8e",
        ).pack(anchor="w", pady=(3, 8))

        self.confirmation_switch = ctk.CTkSwitch(section3, text="Ask before executing dangerous actions")
        self.confirmation_switch.select()
        self.confirmation_switch.pack(anchor="w", pady=4)

        self.auto_scroll_switch = ctk.CTkSwitch(section3, text="Auto-scroll live logs")
        self.auto_scroll_switch.select()
        self.auto_scroll_switch.pack(anchor="w", pady=4)

        self.save_btn = ctk.CTkButton(
            inner,
            text="Save Settings",
            height=40,
            corner_radius=12,
            fg_color="#0f0f0f",
            hover_color="#161616",
            border_width=1,
            border_color="#3f77ff",
            text_color="#9ec0ff",
            command=self._save_settings,
        )
        self.save_btn.pack(anchor="w", pady=(22, 0))

    def _apply_theme(self, choice: str):
        ctk.set_appearance_mode(choice)

    def _save_settings(self):
        messagebox.showinfo("Flux", "Settings saved (UI placeholder).")

    # -----------------------------
    # Public API for backend integration
    # -----------------------------
    def set_backend_status(self, text: str):
        self.backend_status.configure(text=text)

    def set_status(self, text: str, color: Optional[str] = None):
        self.status_label.configure(text=text)
        if color:
            self.status_dot.configure(text_color=color)

    def set_step(self, text: str):
        self.step_label.configure(text=text)

    def set_health(self, text: str, detail: str = "", color: str = "#65d26e"):
        if hasattr(self, "health_text"):
            self.health_text.configure(text=text, text_color=color)
        if hasattr(self, "health_detail"):
            self.health_detail.configure(text=detail)

    def append_activity(self, text: str):
        if not hasattr(self, "activity_log"):
            return
        self.activity_log.configure(state="normal")
        self.activity_log.insert("end", f"• {text}\n")
        self.activity_log.see("end")
        self.activity_log.configure(state="disabled")

    def add_history_item(
        self,
        title: str,
        subtitle: str,
        age_text: str = "",
        accent: str = "#3f77ff",
        target: Optional[ctk.CTkScrollableFrame] = None,
    ):
        parent = target or self.history_list
        if parent is None:
            return

        card = ctk.CTkFrame(
            parent,
            height=88,
            corner_radius=14,
            fg_color="#2a2a2a",
            border_width=1,
            border_color="#3a3a3a",
        )
        card.pack(fill="x", padx=2, pady=8)
        card.pack_propagate(False)

        left = ctk.CTkFrame(card, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=16, pady=12)
        accent_bar = ctk.CTkFrame(left, width=4, fg_color=accent, corner_radius=4)
        accent_bar.pack(side="left", fill="y", padx=(0, 12))

        text_wrap = ctk.CTkFrame(left, fg_color="transparent")
        text_wrap.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(text_wrap, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            text_wrap,
            text=subtitle,
            font=ctk.CTkFont(size=12),
            text_color="#bfbfbf",
        ).pack(anchor="w", pady=(4, 0))

        if age_text:
            ctk.CTkLabel(
                card,
                text=age_text,
                font=ctk.CTkFont(size=12),
                text_color="#a0a0a0",
            ).pack(side="right", padx=16)

        self._history_cards.append(card)

    def clear_history(self):
        for card in self._history_cards:
            card.destroy()
        self._history_cards.clear()

        if hasattr(self, "history_list"):
            for child in self.history_list.winfo_children():
                child.destroy()

        if hasattr(self, "history_feed"):
            for child in self.history_feed.winfo_children():
                child.destroy()

    def set_dashboard_stats(
        self,
        tasks_today: Optional[str] = None,
        running: Optional[str] = None,
        success_rate: Optional[str] = None,
        connected_tools: Optional[str] = None,
    ):
        mapping = {
            "Tasks Today": tasks_today,
            "Running": running,
            "Success Rate": success_rate,
            "Connected Tools": connected_tools,
        }
        for key, value in mapping.items():
            if value is not None and key in self.stat_cards:
                self.stat_cards[key].configure(text=value)

    def add_dashboard_preview(self, title: str, subtitle: str, accent: str = "#3f77ff"):
        if not hasattr(self, "dashboard_preview_list"):
            return

        card = ctk.CTkFrame(
            self.dashboard_preview_list,
            height=72,
            corner_radius=12,
            fg_color="#171717",
            border_width=1,
            border_color="#2d2d2d",
        )
        card.pack(fill="x", padx=4, pady=6)
        card.pack_propagate(False)

        accent_bar = ctk.CTkFrame(card, width=4, fg_color=accent, corner_radius=4)
        accent_bar.pack(side="left", fill="y", padx=(8, 10), pady=10)

        text = ctk.CTkFrame(card, fg_color="transparent")
        text.pack(side="left", fill="both", expand=True, pady=10)

        ctk.CTkLabel(text, text=title, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(text, text=subtitle, font=ctk.CTkFont(size=11), text_color="#a0a0a0").pack(anchor="w")

    def set_connection_state(self, connected: bool):
        if connected:
            self.set_backend_status("Backend: connected")
            self.quick_tip.configure(text="Backend is connected. Ready for live events.")
        else:
            self.set_backend_status("Backend: disconnected")
            self.quick_tip.configure(text="Plug your planner/executor into the page callbacks.")

    def _demo_seed(self):
        # Safe placeholder demo content; remove once backend feeds real data.
        self.set_dashboard_stats("12", "3", "98%", "8")
        self.add_dashboard_preview("Organized Downloads", "Moved 23 files into folders", "#4caf50")
        self.add_dashboard_preview("Send email report", "1 recipient, 2 attachments", "#d4a017")
        self.add_dashboard_preview("Download backup", "3.2 GB from cloud storage", "#4c8df6")

        self.add_history_item("Organized Downloads", "Moved 23 files into folders", "2m ago", "#4caf50")
        self.add_history_item("Send email report", "1 recipient, 2 attachments", "15m ago", "#d4a017")
        self.add_history_item("Download backup", "3.2 GB from cloud storage", "1h ago", "#4c8df6")


def main():
    app = FluxApp()
    app.mainloop()


if __name__ == "__main__":
    main()
