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
}


SITUATIONS = [
    {
        "id": "SMB-001",
        "title": "Le poste n'apparaît pas dans Réseau",
        "description": (
            "La machine peut être invisible dans le voisinage réseau alors "
            "que les accès SMB fonctionnent."
        ),
        "requires_target": False,
    },
    {
        "id": "SMB-002",
        "title": "\\\\IP fonctionne mais \\\\NOM_MACHINE échoue",
        "description": (
            "SMB peut fonctionner tandis que la résolution du nom de la "
            "machine est défaillante."
        ),
        "requires_target": True,
    },
    {
        "id": "SMB-003",
        "title": "Les partages sont visibles mais l'accès est refusé",
        "description": (
            "Vérifier si le compte SMB utilisé correspond au compte réel "
            "retourné par WHOAMI sur la cible."
        ),
        "requires_target": True,
    },
    {
        "id": "LOCAL-NETWORK",
        "title": "Le réseau local ne répond pas",
        "description": (
            "Vérifier la passerelle, l'adresse IP, le DHCP et la "
            "configuration réseau locale."
        ),
        "requires_target": False,
    },
    {
        "id": "LOCAL-SMB",
        "title": "Le partage Windows local ne fonctionne pas",
        "description": (
            "Vérifier les services LanmanServer et LanmanWorkstation, "
            "le profil réseau et les partages visibles."
        ),
        "requires_target": False,
    },
    {
        "id": "REMOTE-WINDOWS",
        "title": "Une cible Windows est inaccessible",
        "description": (
            "Tester ping, ports SMB 139/445, pare-feu et service de partage "
            "sur la cible."
        ),
        "requires_target": True,
    },
    {
        "id": "REMOTE-DEVICE",
        "title": "Identifier une cible du réseau",
        "description": (
            "Classer la cible : poste Windows probable, mobile, équipement "
            "réseau ou hôte inconnu."
        ),
        "requires_target": True,
    },
]


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
    def __init__(self, create_snapshot, initial_target=None, auto_start=False):
        self.create_snapshot = create_snapshot
        self.initial_target = initial_target
        self.auto_start = auto_start
        self.output_queue = queue.Queue()
        self.latest_snapshot = None
        self.selected_vars = {}

        self.root = tk.Tk()
        self.root.title("DTLknowsWhy")
        self.root.geometry("1080x760")
        self.root.minsize(920, 660)
        self.root.configure(bg=COLORS["bg"])

        self._build_styles()
        self._build_layout()
        self._apply_startup_options()
        self.root.after(100, self._poll_queue)

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

        ttk.Label(
            banner,
            text="DTLknowsWhy",
            style="BannerTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            banner,
            text="Assistant de diagnostic réseau Windows",
            style="BannerSubtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        ttk.Label(
            banner,
            text=f"Version {DTLKNOWSWHY_VERSION}",
            style="BannerVersion.TLabel",
        ).grid(row=0, column=1, rowspan=2, sticky="e")

        ttk.Label(
            container,
            text=(
                "Sélectionnez la ou les situations rencontrées, indiquez la "
                "cible si besoin, puis lancez le diagnostic."
            ),
            background=COLORS["bg"],
            foreground=COLORS["muted"],
            wraplength=920,
        ).grid(row=1, column=0, sticky="w", pady=(12, 14))

        top = ttk.Frame(container, style="App.TFrame")
        top.grid(row=2, column=0, sticky="nsew")
        top.columnconfigure(0, weight=2)
        top.columnconfigure(1, weight=1)

        situations_frame = ttk.LabelFrame(
            top,
            text="Situations connues dans la KB",
            padding=12,
            style="Section.TLabelframe",
        )
        situations_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        situations_frame.columnconfigure(0, weight=1)

        for row, situation in enumerate(SITUATIONS):
            var = tk.BooleanVar(value=False)
            self.selected_vars[situation["id"]] = var
            label = situation["title"]

            if situation["requires_target"]:
                label += "  (cible requise)"

            card = ttk.Frame(
                situations_frame,
                padding=(10, 8),
                style="Card.TFrame",
            )
            card.grid(row=row, column=0, sticky="ew", pady=(0, 8))
            card.columnconfigure(0, weight=1)

            ttk.Checkbutton(
                card,
                text=label,
                variable=var,
                command=self._refresh_target_hint,
                style="CardTitle.TCheckbutton",
            ).grid(row=0, column=0, sticky="w")

            ttk.Label(
                card,
                text=situation["description"],
                wraplength=560,
                style="CardText.TLabel",
            ).grid(row=1, column=0, sticky="w", padx=(24, 0), pady=(3, 0))

            if situation["requires_target"]:
                ttk.Label(
                    card,
                    text="CIBLE",
                    style="Badge.TLabel",
                ).grid(row=0, column=1, sticky="ne", padx=(8, 0))

        target_frame = ttk.LabelFrame(
            top,
            text="Cible",
            padding=12,
            style="Section.TLabelframe",
        )
        target_frame.grid(row=0, column=1, sticky="nsew")
        target_frame.columnconfigure(0, weight=1)

        ttk.Label(
            target_frame,
            text="Nom ou adresse IP de la machine à tester",
            background=COLORS["surface"],
            foreground=COLORS["text"],
        ).grid(row=0, column=0, sticky="w")

        self.target_var = tk.StringVar()
        ttk.Entry(
            target_frame,
            textvariable=self.target_var,
        ).grid(row=1, column=0, sticky="ew", pady=(4, 8))

        self.target_hint = ttk.Label(
            target_frame,
            text="Optionnel pour un diagnostic local.",
            wraplength=260,
            style="Hint.TLabel",
        )
        self.target_hint.grid(row=2, column=0, sticky="w")

        self.summary_frame = ttk.LabelFrame(
            target_frame,
            text="Résumé du diagnostic",
            padding=10,
            style="Section.TLabelframe",
        )
        self.summary_frame.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        self.summary_frame.columnconfigure(0, weight=1)

        self.summary_items = {
            "local": self._build_summary_row(0, "Réseau local", "En attente"),
            "dns": self._build_summary_row(1, "DNS", "En attente"),
            "smb": self._build_summary_row(2, "SMB local", "En attente"),
            "target": self._build_summary_row(3, "Cible", "Non testee"),
        }

        self.run_button = ttk.Button(
            target_frame,
            text="Lancer le diagnostic",
            style="Run.TButton",
            command=self._start_diagnosis,
        )
        self.run_button.grid(row=4, column=0, sticky="ew", pady=(14, 6))

        self.open_report_button = ttk.Button(
            target_frame,
            text="Ouvrir le rapport HTML",
            command=self._open_latest_html_report,
            state="disabled",
        )
        self.open_report_button.grid(row=5, column=0, sticky="ew")

        results = ttk.PanedWindow(container, orient="horizontal")
        results.grid(row=3, column=0, sticky="nsew", pady=(14, 0))

        log_frame = ttk.LabelFrame(
            results,
            text="Avancement",
            padding=8,
            style="Section.TLabelframe",
        )
        self.log_text = tk.Text(
            log_frame,
            height=10,
            wrap="word",
            bg="#0f1720",
            fg="#dce7f3",
            insertbackground="#ffffff",
            relief="flat",
            font=("Cascadia Mono", 9),
        )
        self.log_text.pack(fill="both", expand=True)
        results.add(log_frame, weight=1)

        findings_frame = ttk.LabelFrame(
            results,
            text="Constats et vérifications",
            padding=8,
            style="Section.TLabelframe",
        )
        self.findings_text = tk.Text(
            findings_frame,
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
        results.add(findings_frame, weight=2)

    def _build_summary_row(self, row, label, value):
        ttk.Label(
            self.summary_frame,
            text=label,
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=("Segoe UI Semibold", 9),
        ).grid(row=row, column=0, sticky="w", pady=2)

        value_label = ttk.Label(
            self.summary_frame,
            text=value,
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=("Segoe UI", 9),
        )
        value_label.grid(row=row, column=1, sticky="e", pady=2)

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

    def run(self):
        self.root.mainloop()

    def _apply_startup_options(self):
        if not self.initial_target:
            return

        self.target_var.set(self.initial_target)

        for situation in SITUATIONS:
            if situation["requires_target"]:
                self.selected_vars[situation["id"]].set(True)

        self._refresh_target_hint()

        if self.auto_start:
            self.root.after(300, self._start_diagnosis)

    def _selected_situations(self):
        return [
            situation
            for situation in SITUATIONS
            if self.selected_vars[situation["id"]].get()
        ]

    def _refresh_target_hint(self):
        requires_target = any(
            situation["requires_target"]
            for situation in self._selected_situations()
        )

        if requires_target:
            text = "Une cible est nécessaire pour les situations sélectionnées."
        else:
            text = "Optionnel pour un diagnostic local."

        self.target_hint.configure(text=text)

    def _start_diagnosis(self):
        selected = self._selected_situations()

        if not selected:
            messagebox.showwarning(
                "Situation manquante",
                "Sélectionnez au moins une situation à diagnostiquer.",
            )
            return

        target = self.target_var.get().strip() or None

        if any(situation["requires_target"] for situation in selected) and not target:
            messagebox.showwarning(
                "Cible manquante",
                "Indiquez le nom ou l'adresse IP de la cible.",
            )
            return

        if not is_admin():
            continue_without_admin = messagebox.askyesno(
                "Droits administrateur",
                (
                    "DTLknowsWhy n'est pas lancé en administrateur. "
                    "Certaines vérifications peuvent être incomplètes.\n\n"
                    "Voulez-vous continuer quand même ?"
                ),
            )

            if not continue_without_admin:
                return

        self.run_button.configure(state="disabled")
        self.open_report_button.configure(state="disabled")
        self.log_text.delete("1.0", "end")
        self.findings_text.delete("1.0", "end")
        self._reset_summary()
        self.output_queue.put(("log", "Diagnostic en cours...\n"))

        worker = threading.Thread(
            target=self._run_diagnosis,
            args=(target, [situation["id"] for situation in selected]),
            daemon=True,
        )
        worker.start()

    def _run_diagnosis(self, target, selected_ids):
        writer = QueueWriter(self.output_queue)

        try:
            with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                snapshot = self.create_snapshot(target=target, lang="fr")

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
                    self._show_findings(item[1], item[2])
                    self.run_button.configure(state="normal")
                    self.open_report_button.configure(state="normal")
                elif kind == "error":
                    self.run_button.configure(state="normal")
                    messagebox.showerror("Diagnostic impossible", item[1])
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
        self.findings_text.insert("end", "Situations sélectionnées : ", "heading")
        self.findings_text.insert("end", ", ".join(selected_ids), "heading")
        self.findings_text.insert("end", "\n\n")

        if not focused:
            self.findings_text.insert(
                "end",
                "Aucune anomalie significative détectée.\n",
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

            if item.get("remediation"):
                self.findings_text.insert(
                    "end",
                    f"Vérification / action : {item.get('remediation')}\n",
                    "remediation",
                )

            self.findings_text.insert("end", "\n")

    def _reset_summary(self):
        self._set_summary("local", "En cours", "INFO")
        self._set_summary("dns", "En cours", "INFO")
        self._set_summary("smb", "En cours", "INFO")
        self._set_summary("target", "En cours", "INFO")

    def _show_summary(self, snapshot):
        network = snapshot.get("network", {})
        services = snapshot.get("services", {})
        tests = snapshot.get("tests", {})
        remote = snapshot.get("remote_tests", {})

        self._set_summary(
            "local",
            "OK" if tests.get("ping_gateway") else "À vérifier",
            "OK" if tests.get("ping_gateway") else "WARN",
        )
        self._set_summary(
            "dns",
            "Configure" if network.get("dns_servers") else "Incomplet",
            "OK" if network.get("dns_servers") else "WARN",
        )

        smb_ok = (
            services.get("LanmanServer") == "Running"
            and services.get("LanmanWorkstation") == "Running"
        )
        self._set_summary(
            "smb",
            "Opérationnel" if smb_ok else "À vérifier",
            "OK" if smb_ok else "FAIL",
        )

        if remote:
            self._set_summary(
                "target",
                "Joignable" if remote.get("ping_target") else "Injoignable",
                "OK" if remote.get("ping_target") else "FAIL",
            )
        else:
            self._set_summary("target", "Non testee", "INFO")

    def _set_summary(self, key, text, level):
        color = LEVEL_COLORS.get(level, COLORS["muted"])
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
            messagebox.showinfo("Rapport introuvable", "Aucun rapport HTML trouve.")
            return

        os.startfile(os.path.abspath(reports[0]))


def run_gui(create_snapshot, initial_target=None, auto_start=False):
    app = DTLknowsWhyGui(
        create_snapshot,
        initial_target=initial_target,
        auto_start=auto_start,
    )
    app.run()
