# TEST ECRITURE CODEX

import contextlib
import io
import os
import queue
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from agent.collectors.system import is_admin
from expert.rule_catalog import RULE_CATEGORIES, RULES
from shared.i18n import tr
from shared.version import DTLKNOWSWHY_VERSION


COLORS = {
    "bg": "#f3f6fa",
    "surface": "#ffffff",
    "surface_alt": "#eef3f8",
    "border": "#c8d4e3",
    "text": "#1f2937",
    "muted": "#5f6b7a",
    "accent": "#0078d4",
    "accent_dark": "#005a9e",
    "ok": "#107c10",
    "warn": "#ca5010",
    "fail": "#d13438",
    "info": "#0078d4",
}


LEVEL_COLORS = {
    "OK": COLORS["ok"],
    "WARN": COLORS["warn"],
    "FAIL": COLORS["fail"],
    "INFO": COLORS["info"],
    "CAUSE CERTAINE": COLORS["fail"],
    "CAUSE PROBABLE": COLORS["fail"],
    "CAUSE POSSIBLE": COLORS["warn"],
    "À VÉRIFIER": COLORS["info"],
    "A VÉRIFIER": COLORS["info"],
    "OBSERVE": COLORS["ok"],
    "CONFIRMED CAUSE": COLORS["fail"],
    "PROBABLE CAUSE": COLORS["fail"],
    "POSSIBLE CAUSE": COLORS["warn"],
    "TO CHECK": COLORS["info"],
    "OBSERVED": COLORS["ok"],
    "MISSING INFORMATION": COLORS["warn"],
}


class QueueWriter(io.TextIOBase):
    def __init__(self, output_queue):
        self.output_queue = output_queue

    def write(self, text):
        if text:
            self.output_queue.put(("log", text))
        return len(text)

    def flush(self):
        return None


class DTLknowsWhyGui:
    def __init__(self, create_snapshot, initial_target=None, auto_start=False, lang="en"):
        self.create_snapshot = create_snapshot
        self.initial_target = initial_target
        self.auto_start = auto_start
        self.lang = lang if lang in ("fr", "en") else "en"
        self.output_queue = queue.Queue()
        self.latest_snapshot = None
        self.selected_vars = {}
        self.situation_widgets = []
        self.category_widgets = []
        self.summary_rows = {}

        self.root = tk.Tk()
        self.root.title("DTLknowsWhy")
        self.root.geometry("1080x760")
        self.root.minsize(920, 660)
        self.root.configure(bg=COLORS["bg"])

        self._build_styles()
        self._build_layout()
        self._apply_language()
        self._apply_startup_options()
        self.root.after(100, self._poll_queue)

    def _t(self, key):
        return tr(key, self.lang)

    def _format(self, key, **values):
        return self._t(key).format(**values)

    def _language_label_to_code(self, label):
        return "fr" if label == self._t("gui_lang_fr") else "en"

    def _language_code_to_label(self, lang):
        return tr("gui_lang_fr", lang) if lang == "fr" else tr("gui_lang_en", lang)

    def _build_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(".", font=("Segoe UI", 10), background=COLORS["bg"])
        style.configure("App.TFrame", background=COLORS["bg"])
        style.configure("Surface.TFrame", background=COLORS["surface"])
        style.configure("Banner.TFrame", background=COLORS["accent_dark"])
        style.configure(
            "BannerTitle.TLabel",
            background=COLORS["accent_dark"],
            foreground="#ffffff",
            font=("Segoe UI Semibold", 22),
        )
        style.configure(
            "BannerSubtitle.TLabel",
            background=COLORS["accent_dark"],
            foreground="#dceeff",
            font=("Segoe UI", 11),
        )
        style.configure(
            "BannerVersion.TLabel",
            background=COLORS["accent_dark"],
            foreground="#ffffff",
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "Section.TLabelframe",
            background=COLORS["surface"],
            bordercolor=COLORS["border"],
            relief="solid",
        )
        style.configure(
            "Section.TLabelframe.Label",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "Card.TFrame",
            background=COLORS["surface"],
            bordercolor=COLORS["border"],
            relief="solid",
        )
        style.configure(
            "CardTitle.TCheckbutton",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            font=("Segoe UI Semibold", 10),
            focuscolor=COLORS["surface"],
        )
        style.map(
            "CardTitle.TCheckbutton",
            background=[("active", COLORS["surface_alt"])],
            foreground=[("active", COLORS["text"])],
        )
        style.configure(
            "CardText.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "Badge.TLabel",
            background=COLORS["surface_alt"],
            foreground=COLORS["accent_dark"],
            font=("Segoe UI Semibold", 8),
            padding=(6, 2),
        )
        style.configure(
            "Hint.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "Run.TButton",
            font=("Segoe UI Semibold", 10),
            foreground="#ffffff",
            background=COLORS["accent"],
            bordercolor=COLORS["accent"],
            padding=(10, 8),
        )
        style.map(
            "Run.TButton",
            background=[("active", COLORS["accent_dark"]), ("disabled", "#9ebbd6")],
        )
        style.configure("TButton", padding=(10, 7))
        style.configure("TEntry", fieldbackground="#ffffff", padding=(6, 4))
        style.configure("TPanedwindow", background=COLORS["bg"])

    def _build_layout(self):
        container = ttk.Frame(self.root, padding=18, style="App.TFrame")
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(3, weight=1)

        banner = ttk.Frame(container, padding=(18, 14), style="Banner.TFrame")
        banner.grid(row=0, column=0, sticky="ew")
        banner.columnconfigure(0, weight=1)

        self.banner_title_label = ttk.Label(
            banner,
            text="DTLknowsWhy",
            style="BannerTitle.TLabel",
        )
        self.banner_title_label.grid(row=0, column=0, sticky="w")

        self.banner_subtitle_label = ttk.Label(
            banner,
            style="BannerSubtitle.TLabel",
        )
        self.banner_subtitle_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.version_label = ttk.Label(
            banner,
            text=f"Version {DTLKNOWSWHY_VERSION}",
            style="BannerVersion.TLabel",
        )
        self.version_label.grid(row=0, column=1, rowspan=2, sticky="e")

        self.intro_label = ttk.Label(
            container,
            background=COLORS["bg"],
            foreground=COLORS["muted"],
            wraplength=920,
        )
        self.intro_label.grid(row=1, column=0, sticky="w", pady=(12, 14))

        top = ttk.Frame(container, style="App.TFrame")
        top.grid(row=2, column=0, sticky="nsew")
        top.columnconfigure(0, weight=2)
        top.columnconfigure(1, weight=1)

        self.situations_frame = ttk.LabelFrame(
            top,
            padding=12,
            style="Section.TLabelframe",
        )
        self.situations_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.situations_frame.columnconfigure(0, weight=1)

        for row, category in enumerate(RULE_CATEGORIES):
            expanded = tk.BooleanVar(value=True)
            category_frame = ttk.Frame(
                self.situations_frame,
                padding=(10, 8),
                style="Card.TFrame",
            )
            category_frame.grid(row=row, column=0, sticky="ew", pady=(0, 8))
            category_frame.columnconfigure(0, weight=1)

            header = ttk.Checkbutton(
                category_frame,
                variable=expanded,
                command=lambda cat=category["id"]: self._toggle_rule_category(cat),
                style="CardTitle.TCheckbutton",
            )
            header.grid(row=0, column=0, sticky="w")

            rules_frame = ttk.Frame(
                category_frame,
                padding=(10, 6),
                style="Card.TFrame",
            )
            rules_frame.grid(row=1, column=0, sticky="ew", pady=(4, 0))
            rules_frame.columnconfigure(0, weight=1)

            self.category_widgets.append({
                "category": category,
                "expanded": expanded,
                "header": header,
                "rules_frame": rules_frame,
            })

            for rule_row, rule in enumerate(category["rules"]):
                var = tk.BooleanVar(value=False)
                self.selected_vars[rule["id"]] = var

                title = ttk.Checkbutton(
                    rules_frame,
                    variable=var,
                    command=self._refresh_target_hint,
                    style="CardTitle.TCheckbutton",
                )
                title.grid(row=rule_row * 2, column=0, sticky="w", padx=(12, 0))

                description = ttk.Label(
                    rules_frame,
                    wraplength=520,
                    style="CardText.TLabel",
                )
                description.grid(
                    row=rule_row * 2 + 1,
                    column=0,
                    sticky="w",
                    padx=(36, 0),
                    pady=(2, 7),
                )

                badge = None
                if rule["requires_target"]:
                    badge = ttk.Label(
                        rules_frame,
                        style="Badge.TLabel",
                    )
                    badge.grid(row=rule_row * 2, column=1, sticky="ne", padx=(8, 0))

                self.situation_widgets.append({
                    "situation": rule,
                    "title": title,
                    "description": description,
                    "badge": badge,
                })

        self.target_frame = ttk.LabelFrame(
            top,
            padding=12,
            style="Section.TLabelframe",
        )
        self.target_frame.grid(row=0, column=1, sticky="nsew")
        self.target_frame.columnconfigure(0, weight=1)

        self.language_label = ttk.Label(
            self.target_frame,
            background=COLORS["surface"],
            foreground=COLORS["text"],
        )
        self.language_label.grid(row=0, column=0, sticky="w")

        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(
            self.target_frame,
            textvariable=self.language_var,
            state="readonly",
            values=("English", "Français"),
        )
        self.language_combo.grid(row=1, column=0, sticky="ew", pady=(4, 10))
        self.language_combo.bind("<<ComboboxSelected>>", self._on_language_changed)

        self.target_label = ttk.Label(
            self.target_frame,
            background=COLORS["surface"],
            foreground=COLORS["text"],
        )
        self.target_label.grid(row=2, column=0, sticky="w")

        self.target_var = tk.StringVar()
        ttk.Entry(
            self.target_frame,
            textvariable=self.target_var,
        ).grid(row=3, column=0, sticky="ew", pady=(4, 8))

        self.target_hint = ttk.Label(
            self.target_frame,
            wraplength=260,
            style="Hint.TLabel",
        )
        self.target_hint.grid(row=4, column=0, sticky="w")

        self.summary_frame = ttk.LabelFrame(
            self.target_frame,
            padding=10,
            style="Section.TLabelframe",
        )
        self.summary_frame.grid(row=5, column=0, sticky="ew", pady=(14, 0))
        self.summary_frame.columnconfigure(0, weight=1)

        self.summary_items = {
            "local": self._build_summary_row(0, "gui_summary_local", "gui_status_waiting"),
            "dns": self._build_summary_row(1, "gui_summary_dns", "gui_status_waiting"),
            "smb": self._build_summary_row(2, "gui_summary_smb", "gui_status_waiting"),
            "target": self._build_summary_row(3, "gui_summary_target", "gui_status_not_tested"),
        }

        self.run_button = ttk.Button(
            self.target_frame,
            style="Run.TButton",
            command=self._start_diagnosis,
        )
        self.run_button.grid(row=6, column=0, sticky="ew", pady=(14, 6))

        self.open_report_button = ttk.Button(
            self.target_frame,
            command=self._open_latest_html_report,
            state="disabled",
        )
        self.open_report_button.grid(row=7, column=0, sticky="ew")

        results = ttk.PanedWindow(container, orient="horizontal")
        results.grid(row=3, column=0, sticky="nsew", pady=(14, 0))

        self.log_frame = ttk.LabelFrame(
            results,
            padding=8,
            style="Section.TLabelframe",
        )
        self.log_text = tk.Text(
            self.log_frame,
            height=10,
            wrap="word",
            bg="#0f1720",
            fg="#dce7f3",
            insertbackground="#ffffff",
            relief="flat",
            font=("Cascadia Mono", 9),
        )
        self.log_text.pack(fill="both", expand=True)
        results.add(self.log_frame, weight=1)

        self.findings_frame = ttk.LabelFrame(
            results,
            padding=8,
            style="Section.TLabelframe",
        )
        self.findings_text = tk.Text(
            self.findings_frame,
            height=10,
            wrap="word",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=10,
        )
        self._configure_finding_tags()
        self.findings_text.pack(fill="both", expand=True)
        results.add(self.findings_frame, weight=2)

    def _build_summary_row(self, row, label_key, value_key):
        label = ttk.Label(
            self.summary_frame,
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=("Segoe UI Semibold", 9),
        )
        label.grid(row=row, column=0, sticky="w", pady=2)

        value_label = ttk.Label(
            self.summary_frame,
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=("Segoe UI", 9),
        )
        value_label.grid(row=row, column=1, sticky="e", pady=2)
        self.summary_rows[label_key] = label
        value_label.value_key = value_key

        return value_label

    def _configure_finding_tags(self):
        self.findings_text.tag_configure(
            "heading",
            foreground=COLORS["muted"],
            font=("Segoe UI Semibold", 9),
            spacing3=8,
        )
        self.findings_text.tag_configure(
            "message",
            foreground=COLORS["text"],
            lmargin1=6,
            lmargin2=6,
            spacing3=4,
        )
        self.findings_text.tag_configure(
            "remediation",
            foreground=COLORS["text"],
            lmargin1=22,
            lmargin2=22,
            spacing3=12,
        )

        for level, color in LEVEL_COLORS.items():
            self.findings_text.tag_configure(
                level,
                foreground=color,
                font=("Segoe UI Semibold", 10),
                spacing1=8,
            )

    def _apply_language(self):
        self.banner_subtitle_label.configure(text=self._t("gui_subtitle"))
        self.version_label.configure(text=f"Version {DTLKNOWSWHY_VERSION}")
        self.intro_label.configure(text=self._t("gui_intro"))
        self.situations_frame.configure(text=self._t("gui_known_situations"))
        self.target_frame.configure(text=self._t("gui_target"))
        self.language_label.configure(text=self._t("gui_preferred_language"))
        self.target_label.configure(text=self._t("gui_target_label"))
        self.summary_frame.configure(text=self._t("gui_summary"))
        self.run_button.configure(text=self._t("gui_run"))
        self.open_report_button.configure(text=self._t("gui_open_html"))
        self.log_frame.configure(text=self._t("gui_progress"))
        self.findings_frame.configure(text=self._t("gui_findings"))

        language_values = (
            self._t("gui_lang_en"),
            self._t("gui_lang_fr"),
        )
        self.language_combo.configure(values=language_values)
        self.language_var.set(self._language_code_to_label(self.lang))

        for item in self.category_widgets:
            category = item["category"]
            prefix = "▼" if item["expanded"].get() else "▶"
            item["header"].configure(text=f"{prefix} {self._t(category['title_key'])}")

        for item in self.situation_widgets:
            situation = item["situation"]
            label = self._t(situation["title_key"])

            if situation["requires_target"]:
                label += self._t("gui_target_required_suffix")

            item["title"].configure(text=label)
            item["description"].configure(text=self._t(situation["description_key"]))

            if item["badge"] is not None:
                item["badge"].configure(text=self._t("gui_target_badge"))

        summary_label_keys = (
            "gui_summary_local",
            "gui_summary_dns",
            "gui_summary_smb",
            "gui_summary_target",
        )
        for key in summary_label_keys:
            self.summary_rows[key].configure(text=self._t(key))

        for label in self.summary_items.values():
            value_key = getattr(label, "value_key", None)
            if value_key:
                label.configure(text=self._t(value_key))

        self._refresh_target_hint()

        if self.latest_snapshot:
            self._show_findings(
                self.latest_snapshot,
                getattr(self, "latest_selected_ids", []),
            )

    def _on_language_changed(self, _event=None):
        selected = self.language_var.get()
        self.lang = "fr" if selected == self._t("gui_lang_fr") else "en"
        self._apply_language()

    def _toggle_rule_category(self, category_id):
        for item in self.category_widgets:
            if item["category"]["id"] != category_id:
                continue

            if item["expanded"].get():
                item["rules_frame"].grid()
            else:
                item["rules_frame"].grid_remove()

            self._apply_language()
            break

    def run(self):
        self.root.mainloop()

    def _apply_startup_options(self):
        if not self.initial_target:
            return

        self.target_var.set(self.initial_target)

        for situation in RULES:
            if situation["requires_target"]:
                self.selected_vars[situation["id"]].set(True)

        self._refresh_target_hint()

        if self.auto_start:
            self.root.after(300, self._start_diagnosis)

    def _selected_situations(self):
        return [
            situation
            for situation in RULES
            if self.selected_vars[situation["id"]].get()
        ]

    def _refresh_target_hint(self):
        requires_target = any(
            situation["requires_target"]
            for situation in self._selected_situations()
        )

        if requires_target:
            text = self._t("gui_target_required_hint")
        else:
            text = self._t("gui_target_optional")

        self.target_hint.configure(text=text)

    def _start_diagnosis(self):
        selected = self._selected_situations()

        if not selected:
            messagebox.showwarning(
                self._t("gui_missing_situation_title"),
                self._t("gui_missing_situation_message"),
            )
            return

        target = self.target_var.get().strip() or None

        if any(situation["requires_target"] for situation in selected) and not target:
            messagebox.showwarning(
                self._t("gui_missing_target_title"),
                self._t("gui_missing_target_message"),
            )
            return

        if not is_admin():
            continue_without_admin = messagebox.askyesno(
                self._t("gui_admin_title"),
                self._t("gui_admin_message"),
            )

            if not continue_without_admin:
                return

        self.run_button.configure(state="disabled")
        self.open_report_button.configure(state="disabled")
        self.log_text.delete("1.0", "end")
        self.findings_text.delete("1.0", "end")
        self._reset_summary()
        self.output_queue.put(("log", f"{self._t('gui_diagnosis_running')}\n"))

        worker = threading.Thread(
            target=self._run_diagnosis,
            args=(target, [situation["id"] for situation in selected], self.lang),
            daemon=True,
        )
        worker.start()

    def _run_diagnosis(self, target, selected_ids, lang):
        writer = QueueWriter(self.output_queue)

        try:
            with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                snapshot = self.create_snapshot(target=target, lang=lang)

            self.output_queue.put(("done", snapshot, selected_ids))
        except Exception as exc:
            self.output_queue.put(("error", str(exc)))

    def _poll_queue(self):
        try:
            while True:
                item = self.output_queue.get_nowait()
                kind = item[0]

                if kind == "log":
                    self._append_log(item[1])
                elif kind == "done":
                    self.latest_snapshot = item[1]
                    self.latest_selected_ids = item[2]
                    self._show_findings(item[1], item[2])
                    self.run_button.configure(state="normal")
                    self.open_report_button.configure(state="normal")
                elif kind == "error":
                    self.run_button.configure(state="normal")
                    messagebox.showerror(self._t("gui_diagnosis_failed"), item[1])
        except queue.Empty:
            pass

        self.root.after(100, self._poll_queue)

    def _append_log(self, text):
        for part in text.splitlines(keepends=True):
            if part.startswith("\r"):
                self.log_text.delete("end-1c linestart", "end-1c lineend")
                part = part[1:]

            self.log_text.insert("end", part.replace("\r", "\n"))

        self.log_text.see("end")

    def _show_findings(self, snapshot, selected_ids):
        diagnosis = snapshot.get("diagnosis", [])
        self._show_summary(snapshot)

        focused = [
            item
            for item in diagnosis
            if item.get("case") in selected_ids
            or (not item.get("case") and item.get("level") in {"FAIL", "WARN"})
        ]

        if not focused:
            focused = diagnosis

        self.findings_text.delete("1.0", "end")
        self.findings_text.insert("end", self._t("gui_selected_situations"), "heading")
        self.findings_text.insert("end", ", ".join(selected_ids), "heading")
        self.findings_text.insert("end", "\n\n")

        if not focused:
            self.findings_text.insert(
                "end",
                f"{self._t('gui_no_significant_issue')}\n",
                "message",
            )
            return

        for item in focused:
            level = item.get("level", "INFO")
            case = f" {item.get('case')}" if item.get("case") else ""
            self.findings_text.insert(
                "end",
                f"[{level}]{case}\n",
                level if level in LEVEL_COLORS else "INFO",
            )
            self.findings_text.insert(
                "end",
                f"{item.get('message')}\n",
                "message",
            )

            for evidence in item.get("evidence", []):
                self.findings_text.insert(
                    "end",
                    f"- {evidence}\n",
                    "message",
                )

            if item.get("remediation"):
                self.findings_text.insert(
                    "end",
                    f"{self._t('gui_check_action')} : {item.get('remediation')}\n",
                    "remediation",
                )

            self.findings_text.insert("end", "\n")

    def _reset_summary(self):
        self._set_summary("local", self._t("gui_status_running"), "INFO")
        self._set_summary("dns", self._t("gui_status_running"), "INFO")
        self._set_summary("smb", self._t("gui_status_running"), "INFO")
        self._set_summary("target", self._t("gui_status_running"), "INFO")

    def _show_summary(self, snapshot):
        network = snapshot.get("network", {})
        services = snapshot.get("services", {})
        tests = snapshot.get("tests", {})
        remote = snapshot.get("remote_tests", {})

        self._set_summary(
            "local",
            "OK" if tests.get("ping_gateway") else self._t("gui_status_check"),
            "OK" if tests.get("ping_gateway") else "WARN",
        )
        self._set_summary(
            "dns",
            self._t("gui_status_configured") if network.get("dns_servers") else self._t("gui_status_incomplete"),
            "OK" if network.get("dns_servers") else "WARN",
        )

        smb_ok = (
            services.get("LanmanServer") == "Running"
            and services.get("LanmanWorkstation") == "Running"
        )
        self._set_summary(
            "smb",
            self._t("gui_status_operational") if smb_ok else self._t("gui_status_check"),
            "OK" if smb_ok else "FAIL",
        )

        if remote:
            self._set_summary(
                "target",
                self._t("gui_status_reachable") if remote.get("ping_target") else self._t("gui_status_unreachable"),
                "OK" if remote.get("ping_target") else "FAIL",
            )
        else:
            self._set_summary("target", self._t("gui_status_not_tested"), "INFO")

    def _set_summary(self, key, text, level):
        color = LEVEL_COLORS.get(level, COLORS["muted"])
        self.summary_items[key].value_key = None
        self.summary_items[key].configure(text=text, foreground=color)

    def _open_latest_html_report(self):
        reports = sorted(
            (
                name
                for name in os.listdir(".")
                if name.lower().endswith(".html") and "_report_" in name
            ),
            key=lambda name: os.path.getmtime(name),
            reverse=True,
        )

        if not reports:
            messagebox.showinfo(
                self._t("gui_report_missing_title"),
                self._t("gui_report_missing_message"),
            )
            return

        os.startfile(os.path.abspath(reports[0]))


def run_gui(create_snapshot, initial_target=None, auto_start=False, lang="en"):
    app = DTLknowsWhyGui(
        create_snapshot,
        initial_target=initial_target,
        auto_start=auto_start,
        lang=lang,
    )
    app.run()
