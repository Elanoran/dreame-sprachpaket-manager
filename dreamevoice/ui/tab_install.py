"""Seite 'Bauen und Aufspielen': der ausführliche Weg mit allen Schaltern."""

from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from .. import installer, library, official, packer, server
from ..paths import build_dir
from .state import (AppState, Task, error_text, run_async, spaeter,
                    to_main)
from .theme import Theme
from .widgets import (Card, InfoBanner, LogView, ScrollablePage, StatusBadge,
                      labeled_value, show_error, show_info, show_warning)


APP_HINWEIS = (
    "Important regarding the Dreamehome app: your pack will NOT show up "
    "there under 'Voice'. The app only lists languages from Dreame's own "
    "catalog, and a self-assigned identifier isn't in it.\n\n"
    "So if the app reports on opening that the robot and app have "
    "different language settings, that's exactly the expected sign that "
    "your pack is running.\n\n"
    "Don't pick a language in the Dreamehome app now - that would make the "
    "robot re-download the official pack and overwrite yours.\n\n"
    "You can go back to the original voice any time via "
    "'Restore Original Voice'."
)


def open_folder(path: Path) -> None:
    try:
        if sys.platform == "win32":
            os.startfile(str(path))  # noqa: S606
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError:
        pass


class InstallTab(ttk.Frame):
    def __init__(self, master, theme: Theme, state: AppState) -> None:
        super().__init__(master, style="TFrame")
        self.theme = theme
        self.state = state
        self._task: Optional[Task] = None
        self._build()

        state.subscribe("device_changed", self.refresh_summary)
        state.subscribe("base_pack_changed", self.refresh_summary)
        state.subscribe("assignments_changed", self.refresh_summary)

    # ------------------------------------------------------------------
    def _build(self) -> None:
        self.page = page = ScrollablePage(self, self.theme)
        page.pack(fill="both", expand=True)
        outer = page.body()

        InfoBanner(
            outer, self.theme,
            "How the install works: the app builds the pack, briefly starts "
            "a small web server on this PC, and tells the robot via the "
            "Dreame cloud to fetch it there. The robot checks the checksum "
            "itself - if it doesn't match, it discards the pack and keeps "
            "its current voice.\n"
            "Your pack will NOT appear in the Dreamehome app under "
            "'Voice' afterward - that only shows Dreame's own languages. "
            "The 'Check Voice Pack on Robot' button tells you whether it's "
            "running.",
        ).pack(fill="x", pady=(0, 14))

        top = ttk.Frame(outer, style="TFrame")
        top.pack(fill="x")
        top.columnconfigure(0, weight=3, uniform="cols")
        top.columnconfigure(1, weight=2, uniform="cols")

        # ---- Zusammenfassung -------------------------------------------
        summary = Card(top, self.theme, "Summary")
        summary.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        self.val_device = labeled_value(summary.content, self.theme, "Robot")
        self.val_base = labeled_value(summary.content, self.theme, "Original Pack")
        self.val_count = labeled_value(summary.content, self.theme, "Custom Announcements")
        self.val_pack = labeled_value(summary.content, self.theme, "Built Pack")
        self.val_md5 = labeled_value(summary.content, self.theme, "MD5 Checksum")

        self.prebuilt_row = ttk.Frame(summary.content, style="Card.TFrame")
        self.lbl_prebuilt = ttk.Label(self.prebuilt_row, text="", style="Warning.TLabel",
                                      wraplength=430, justify="left")
        self.lbl_prebuilt.pack(anchor="w")
        ttk.Button(self.prebuilt_row, text="Build My Own Pack Instead",
                   style="Small.TButton",
                   command=self._clear_prebuilt).pack(anchor="w", pady=(6, 0))

        # ---- Gespeicherte Pakete ---------------------------------------
        # Wer mehrere Fassungen desselben Dialekts gebaut hat - eine mit der
        # bezahlten ElevenLabs-Stimme, eine zum Ausprobieren mit Windows -
        # muss hier sehen und wählen können, welche installiert wird.
        self.pack_row = ttk.Frame(summary.content, style="Card.TFrame")
        self.pack_row.pack(fill="x", pady=(12, 0))
        ttk.Label(self.pack_row, text="Saved Packs",
                  style="Surface.TLabel").pack(anchor="w")
        self.var_saved = tk.StringVar()
        self.combo_saved = ttk.Combobox(self.pack_row, textvariable=self.var_saved,
                                        state="readonly", width=52)
        self.combo_saved.pack(fill="x", pady=(4, 0))
        self.combo_saved.bind("<<ComboboxSelected>>", self._on_pick_saved)
        self.lbl_saved = ttk.Label(self.pack_row, text="", style="Muted.TLabel",
                                   wraplength=430, justify="left")
        self.lbl_saved.pack(anchor="w", pady=(4, 0))
        self._saved: list = []

        # ---- Einstellungen ---------------------------------------------
        settings = Card(top, self.theme, "Settings")
        settings.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        body = settings.content
        body.columnconfigure(1, weight=1)

        ttk.Label(body, text="Identifier", style="Surface.TLabel").grid(
            row=0, column=0, sticky="w", pady=4, padx=(0, 8))
        # Fest, siehe installer.install_pack: Der Roboter legt je Kennung
        # einen Ordner an, den man über die Cloud nicht mehr löschen
        # kann. Eine einzige Kennung überschreibt sich selbst.
        ttk.Label(body, text=installer.DEFAULT_CUSTOM_LANG_ID,
                  style="Surface.TLabel").grid(
            row=0, column=1, sticky="w", pady=4)

        ttk.Label(body, text="PC Address", style="Surface.TLabel").grid(
            row=1, column=0, sticky="w", pady=4, padx=(0, 8))
        self.var_ip = tk.StringVar(value=self.state.config["host_ip"])
        self.combo_ip = ttk.Combobox(body, textvariable=self.var_ip, width=18,
                                     values=server.candidate_ips())
        self.combo_ip.grid(row=1, column=1, sticky="w", pady=4)
        if not self.var_ip.get():
            ips = server.candidate_ips()
            if ips:
                self.var_ip.set(ips[0])

        ttk.Label(body, text="Port", style="Surface.TLabel").grid(
            row=2, column=0, sticky="w", pady=4, padx=(0, 8))
        self.var_port = tk.StringVar(value=str(self.state.config["serve_port"] or ""))
        ttk.Entry(body, textvariable=self.var_port, width=10).grid(
            row=2, column=1, sticky="w", pady=4)
        ttk.Label(body, text="empty = automatic", style="Muted.TLabel").grid(
            row=3, column=1, sticky="w")

        ttk.Label(body, text="Custom URL", style="Surface.TLabel").grid(
            row=4, column=0, sticky="w", pady=(10, 4), padx=(0, 8))
        self.var_url = tk.StringVar()
        ttk.Entry(body, textvariable=self.var_url).grid(
            row=4, column=1, sticky="ew", pady=(10, 4))
        ttk.Label(body,
                  text=("only needed if the robot can't reach this PC "
                        "(then upload the pack yourself)"),
                  style="Muted.TLabel", wraplength=230,
                  justify="left").grid(row=5, column=1, sticky="w")

        # ---- Aktionen ---------------------------------------------------
        actions = Card(outer, self.theme, "Step 3: Transfer to the Robot")
        actions.pack(fill="x", pady=(14, 0))

        button_row = ttk.Frame(actions.content, style="Card.TFrame")
        button_row.pack(fill="x")

        self.btn_install = ttk.Button(
            button_row, text="Install Voice Pack on Robot",
            style="Big.TButton", command=self._on_install)
        self.btn_install.pack(side="left")

        self.btn_build_only = ttk.Button(
            button_row, text="Build Only", command=self._on_build_only)
        self.btn_build_only.pack(side="left", padx=(10, 0))

        self.btn_cancel = ttk.Button(button_row, text="Cancel",
                                     command=self._on_cancel, state="disabled")
        self.btn_cancel.pack(side="left", padx=(10, 0))

        ttk.Button(button_row, text="Open Pack Folder", style="Small.TButton",
                   command=lambda: open_folder(build_dir())).pack(side="right")
        # Bewusst "Gebautes Paket": unter 'Eigene Stimmen' gibt es einen Knopf zum Einlesen
        # von Aufnahmen, und "Fertiges Paket" hat für beides gepasst.
        ttk.Button(button_row, text="Choose Ready-Made Pack ...",
                   style="Small.TButton",
                   command=self._on_pick_pack).pack(side="right", padx=(0, 8))

        self.progress = ttk.Progressbar(actions.content, mode="determinate",
                                        maximum=100)
        self.progress.pack(fill="x", pady=(14, 6))

        status_row = ttk.Frame(actions.content, style="Card.TFrame")
        status_row.pack(fill="x")
        self.badge = StatusBadge(status_row, self.theme, "Ready")
        self.badge.pack(side="left")
        self.btn_status = ttk.Button(
            status_row, text="Check Voice Pack on Robot",
            style="Small.TButton", command=self._on_query_status)
        self.btn_status.pack(side="right")

        self.log = LogView(actions.content, self.theme, height=13)
        self.log.pack(fill="both", expand=True, pady=(12, 0))

        # ---- Wiederherstellen -------------------------------------------
        self.karte_notausgang = restore = Card(
            outer, self.theme, "Emergency Exit: Restore Original Voice",
                       "Installs the official Dreame voice pack again - the "
                       "robot loads it directly from the manufacturer, this "
                       "PC isn't involved at all.")
        restore.pack(fill="x", pady=(14, 0))

        restore_row = ttk.Frame(restore.content, style="Card.TFrame")
        restore_row.pack(fill="x")
        ttk.Label(restore_row, text="Language", style="Surface.TLabel").pack(
            side="left", padx=(0, 10))
        self.var_restore = tk.StringVar()
        self.combo_restore = ttk.Combobox(restore_row, textvariable=self.var_restore,
                                          state="readonly", width=34, values=[])
        self.combo_restore.pack(side="left")
        self.btn_restore = ttk.Button(restore_row, text="Restore Original Voice",
                                      command=self._on_restore)
        self.btn_restore.pack(side="left", padx=(12, 0))

        self.refresh_summary()

    # ------------------------------------------------------------------
    def refresh_saved_packs(self) -> None:
        """Liest die gebauten Pakete neu ein und füllt die Auswahl."""
        try:
            self._saved = library.list_packs()
        except OSError:
            self._saved = []

        beschriftungen = [i.label for i in self._saved]
        self.combo_saved.configure(values=beschriftungen)

        if not self._saved:
            self.var_saved.set("")
            self.lbl_saved.configure(
                text=("No packs built yet. 'Custom Voices' creates a dialect "
                      "pack, 'Individual Announcements' a custom one."))
            self.combo_saved.configure(state="disabled")
            return

        self.combo_saved.configure(state="readonly")
        aktuell = self.state.last_build
        if aktuell is not None:
            for i, info in enumerate(self._saved):
                if info.path == aktuell.path:
                    self.var_saved.set(beschriftungen[i])
                    break
        self.lbl_saved.configure(
            text=(f"{len(self._saved)} saved packs. Each voice lives in its "
                  f"own file - a new version never overwrites an older one."))

    def _on_pick_saved(self, _event=None) -> None:
        """Ein gespeichertes Paket zum Installieren auswählen."""
        wahl = self.var_saved.get()
        info = next((i for i in self._saved if i.label == wahl), None)
        if info is None:
            return

        try:
            build = packer.load_existing(info.path)
        except Exception as exc:                       # noqa: BLE001
            self._on_error(exc)
            return

        self.state.prebuilt = build
        self.state.prebuilt_name = info.dialect or info.path.name
        self.state.last_build = build
        self.refresh_summary()
        self.log.append(f"Selected: {info.path.name}", "ok")
        if info.voice:
            self.log.append(f"Voice: {info.voice}", "muted")

    def refresh_summary(self) -> None:
        self.refresh_saved_packs()
        device = self.state.device
        self.val_device.configure(
            text=f"{device.name} ({device.model})" if device else "not selected")

        if self.state.base_pack_info and self.state.has_base_pack:
            info = self.state.base_pack_info
            self.val_base.configure(
                text=f"{info.label} - {info.size / (1024 * 1024):.1f} MB")
        else:
            self.val_base.configure(text="not loaded yet")

        assigned = len(self.state.assignments())
        missing = len(self.state.missing_assignments())
        text = str(assigned)
        if missing:
            text += f"  ({missing} file(s) missing!)"
        self.val_count.configure(text=text)

        build = self.state.last_build
        if build:
            self.val_pack.configure(
                text=f"{build.path.name} - {build.size_mb:.1f} MB")
            self.val_md5.configure(text=build.md5)
        else:
            self.val_pack.configure(text="not built yet")
            self.val_md5.configure(text="-")

        if self.state.prebuilt is not None:
            self.lbl_prebuilt.configure(
                text=(f"The ready-made pack '{self.state.prebuilt_name}' is "
                      f"queued for install. Your own assignments stay saved "
                      f"but aren't being used right now."))
            self.prebuilt_row.pack(fill="x", pady=(10, 0))
        else:
            self.prebuilt_row.pack_forget()

        packs = self.state.official_packs
        labels = [p.label for p in packs]
        if list(self.combo_restore.cget("values")) != labels:
            self.combo_restore.configure(values=labels)
            match = official.find_pack(packs, "DE")
            if match:
                self.var_restore.set(match.label)
            elif labels:
                self.var_restore.set(labels[0])

    # ------------------------------------------------------------------
    def _on_query_status(self) -> None:
        """Fragt den Roboter, welches Sprachpaket er gerade benutzt.

        Die Dreamehome-App kann eigene Pakete nicht anzeigen - hier kommt
        die Antwort direkt vom Roboter.
        """
        if not self.state.connected:
            show_warning(self, self.theme, "No Robot Selected",
                         "Sign in under 'Connection' first.")
            return

        cloud, device = self.state.cloud, self.state.device
        self.btn_status.configure(state="disabled")
        self.badge.set("Asking the robot ...", "muted")

        def work(_task):
            return (cloud.current_voice_pack(device),
                    cloud.voice_change_status(device))

        def ok(antwort) -> None:
            aktiv, zustand = antwort
            self.log.append(f"Active voice pack per the robot: {aktiv or 'unknown'}",
                            "ok" if aktiv else "warn")
            if zustand:
                self.log.append(f"State: {zustand}", "info")

            offiziell = {p.id for p in self.state.official_packs}
            if not aktiv:
                self.badge.set("No Response - Robot Asleep?", "warn")
                show_warning(
                    self, self.theme, "No Response",
                    "The robot didn't respond.",
                    "Wake it in the Dreamehome app and try again.")
                return

            self.badge.set(f"Active: {aktiv}", "ok")
            if str(aktiv).upper() in offiziell:
                show_info(
                    self, self.theme, "Official Pack Active",
                    f"The robot is currently using '{aktiv}' - a pack from Dreame.",
                    "Your custom pack isn't active as a result. This happens "
                    "when a language was selected in the Dreamehome app: the "
                    "robot then re-downloads it and overwrites the custom "
                    "pack. Just install it again.")
            else:
                show_info(
                    self, self.theme, "Your Pack Is Active",
                    f"The robot is currently using '{aktiv}' - that's your "
                    f"own identifier, not a pack from Dreame.",
                    APP_HINWEIS)

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            self.badge.set("Check Failed", "error")
            show_error(self, self.theme, "Check Failed", message, hint)

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_status.configure(state="normal"))

    def _on_pick_pack(self) -> None:
        """Ein bereits gebautes Sprachpaket von der Festplatte übernehmen."""
        chosen = filedialog.askopenfilename(
            parent=self,
            title="Choose a Built Voice Pack (.tar.gz)",
            initialdir=str(build_dir()),
            filetypes=[("Built voice pack", "*.tar.gz *.tgz"),
                       ("All files", "*.*")],
        )
        if not chosen:
            return

        # Die Aufnahmen-Archive aus dem Projekt sind ZIPs und gehören nach
        # 'Eigene Stimmen' - hier würden sie nur mit einer Formatmeldung scheitern.
        if Path(chosen).suffix.lower() == ".zip":
            show_warning(
                self, self.theme, "That's Recordings, Not a Ready-Made Pack",
                f"{Path(chosen).name} contains individual voice files. This "
                f"expects an already-built pack - a .tar.gz file.",
                "How to proceed: if these are the recordings from the "
                "project page, they're already ready to go. Use the "
                "'Ready-Made Voices' sidebar item instead - choose, "
                "preview, install there.\n\n"
                "If these are your own recordings, use 'Custom Voices' and "
                "click 'Import Recordings ...' there. The app builds the "
                "pack for your model from them; it then shows up here too. "
                "You don't need to unpack anything.")
            return

        try:
            build = packer.load_existing(Path(chosen))
        except Exception as exc:
            self._on_error(exc)
            return

        self.state.prebuilt = build
        self.state.prebuilt_name = Path(chosen).name
        self.state.last_build = build
        self.refresh_summary()

        self.log.clear()
        self.log.append(f"Loaded: {build.path.name}", "ok")
        self.log.append(f"{len(build.replaced)} announcements, {build.size_mb:.1f} MB, "
                        f"MD5 {build.md5}", "info")
        for warning in build.warnings:
            self.log.append(warning, "warn")
        self.badge.set("Pack Loaded - Ready to Install", "ok")

    def _clear_prebuilt(self) -> None:
        self.state.prebuilt = None
        self.state.prebuilt_name = ""
        self.state.last_build = None
        self.refresh_summary()

    def zeige_notausgang(self) -> None:
        """Rollt zum Abschnitt "Originalstimme zurückholen".

        Wer von der Startseite kommt, will genau dorthin - nicht an
        den Anfang der Seite, wo als größter Knopf "Sprachpaket auf
        Roboter installieren" steht.
        """
        spaeter(self, 60, lambda: self.page.scrolle_zu(self.karte_notausgang))

    def _busy(self, active: bool, abbrechbar: bool = True) -> None:
        """Knöpfe während eines Vorgangs sperren.

        `abbrechbar` steuert nur den Abbruchknopf. Beim Wiederherstellen
        der Originalstimme gibt es nichts abzubrechen - der Roboter lädt
        dabei direkt bei Dreame, ohne dass wir dazwischenstehen. Ein
        Knopf, der bis zu sieben Minuten lang nichts tut, ist schlimmer
        als ein grauer Knopf.
        """
        state = "disabled" if active else "normal"
        self.btn_install.configure(state=state)
        self.btn_build_only.configure(state=state)
        self.btn_restore.configure(state=state)
        self.btn_cancel.configure(
            state="normal" if (active and abbrechbar) else "disabled")

    def _log(self, message: str, kind: str = "info") -> None:
        to_main(self, self.log.append, message, kind)

    def _step(self, message: str, fraction: float) -> None:
        def apply() -> None:
            self.progress.configure(value=max(0.0, min(1.0, fraction)) * 100)
            self.badge.set(message, "muted")
        to_main(self, apply)

    def _on_cancel(self) -> None:
        if self._task:
            self._task.cancel()
            self.log.append("Cancellation requested ...", "warn")

    # ------------------------------------------------------------------
    def _preflight(self, need_device: bool = True) -> bool:
        if need_device and not self.state.connected:
            messagebox.showwarning(
                "No Robot Selected",
                "Sign in under 'Connection' and choose your robot.",
                parent=self)
            return False

        if not self.state.has_base_pack:
            messagebox.showwarning(
                "Original Pack Missing",
                "First download your robot's official voice pack under "
                "'Individual Announcements'. It's the foundation for your "
                "own pack.",
                parent=self)
            return False

        if self.state.prebuilt is not None:
            # Fertiges Community-Paket - es muss nichts gebaut werden.
            return True

        if not self.state.assignments():
            messagebox.showwarning(
                "Nothing to Do",
                "Not a single announcement has been replaced yet. Assign at "
                "least one announcement an audio file under 'Individual "
                "Announcements' - or get a ready-made pack under 'Custom "
                "Voices'.",
                parent=self)
            return False

        missing = self.state.missing_assignments()
        if missing:
            preview = "\n".join(f"  Announcement {i}: {p}" for i, p in missing[:6])
            more = f"\n  ... and {len(missing) - 6} more" if len(missing) > 6 else ""
            if not messagebox.askyesno(
                    "Files Missing",
                    f"{len(missing)} assigned file(s) no longer exist:\n\n"
                    f"{preview}{more}\n\nThese announcements will stay on the "
                    f"original voice. Continue anyway?",
                    parent=self):
                return False
        return True

    def _build_pack(self, task: Task):
        prebuilt = self.state.prebuilt
        if prebuilt is not None and prebuilt.path.is_file():
            self._log(f"Using the prepared pack '{self.state.prebuilt_name}'.",
                      "info")
            self._log("It's already adapted to your model - nothing needs "
                      "to be built again.", "info")
            return prebuilt

        return packer.build_pack(
            base_pack=self.state.base_pack_path,
            assignments=self.state.assignments(),
            out_name="mein_sprachpaket.tar.gz",
            ffmpeg=self.state.ffmpeg,
            mapping=self.state.voice_mapping(),
            log=lambda m: self._log(m),
            progress=lambda done, total: self._step(
                "Building pack", 0.05 + 0.35 * (done / total if total else 0)),
        )

    # ------------------------------------------------------------------
    def _on_build_only(self) -> None:
        if not self._preflight(need_device=False):
            return

        self.log.clear()
        self.log.append("Building pack (without installing) ...", "step")
        self._busy(True)
        self.progress.configure(value=0)

        def work(task):
            return self._build_pack(task)

        def ok(build):
            self.state.last_build = build
            self.refresh_summary()
            self.progress.configure(value=100)
            self.badge.set("Pack Built", "ok")
            self.log.append(build.summary(), "ok")
            for warning in build.warnings:
                self.log.append(warning, "warn")
            self.log.append(f"Saved to: {build.path}", "info")

        run_async(self, work, on_success=ok, on_error=self._on_error,
                  on_finally=lambda: self._busy(False))

    def _on_install(self) -> None:
        if not self._preflight():
            return

        lang_id = installer.DEFAULT_CUSTOM_LANG_ID

        try:
            port = int(self.var_port.get().strip() or 0)
        except ValueError:
            messagebox.showwarning("Invalid Port",
                                   "The port must be a number (or left empty).",
                                   parent=self)
            return

        self.state.config["custom_lang_id"] = lang_id
        self.state.config["host_ip"] = self.var_ip.get().strip()
        self.state.config["serve_port"] = port
        self.state.save()

        cloud, device = self.state.cloud, self.state.device
        public_url = self.var_url.get().strip()
        host_ip = self.var_ip.get().strip()

        self.log.clear()
        self.log.append("Starting installation", "step")
        self._busy(True)
        self.progress.configure(value=0)

        def work(task):
            build = self._build_pack(task)
            self.state.last_build = build
            to_main(self, self.refresh_summary)
            for warning_text in build.warnings:
                self._log(warning_text, "warn")

            self._log("", "info")
            self._log("Transferring to the robot", "step")
            return installer.install_pack(
                cloud=cloud, device=device, build=build,
                port=port, host_ip=host_ip, public_url=public_url,
                log=lambda m: self._log(m),
                step=self._step,
                cancelled=lambda: task.cancelled,
            )

        def ok(outcome: installer.InstallOutcome) -> None:
            if outcome.success:
                self.progress.configure(value=100)
                # Belegt oder nur wahrscheinlich - der Unterschied gehört
                # in die Plakette und ins Fenster, nicht nur ins Protokoll.
                if outcome.bestaetigt:
                    self.badge.set("Installed Successfully", "ok")
                else:
                    self.badge.set("Transferred, Not Confirmed", "warn")
                self.log.append(outcome.message,
                                "ok" if outcome.bestaetigt else "warn")
                if outcome.hint:
                    self.log.append(outcome.hint, "warn")
                self.log.append(APP_HINWEIS, "warn")
                show_info(
                    self, self.theme,
                    "Done" if outcome.bestaetigt else "Transferred",
                    outcome.message + "\n\nTry it out: have the robot start "
                    "a cleaning run - it should sound different now.",
                    (f"{outcome.hint}\n\n{APP_HINWEIS}" if outcome.hint
                     else APP_HINWEIS))
            else:
                self.badge.set(outcome.message, "error")
                self.log.append(outcome.message, "error")
                if outcome.hint:
                    self.log.append(outcome.hint, "warn")
                messagebox.showwarning(
                    "Not Completed",
                    outcome.message + (f"\n\n{outcome.hint}" if outcome.hint else ""),
                    parent=self)

        self._task = run_async(self, work, on_success=ok, on_error=self._on_error,
                               on_finally=self._install_done)

    def _install_done(self) -> None:
        self._busy(False)
        self._task = None

    # ------------------------------------------------------------------
    def _on_restore(self) -> None:
        if not self.state.connected:
            messagebox.showwarning("No Robot Selected",
                                   "Sign in under 'Connection' first.",
                                   parent=self)
            return

        pack = next((p for p in self.state.official_packs
                     if p.label == self.var_restore.get()), None)
        if pack is None:
            messagebox.showwarning("No Language Chosen",
                                   "Please choose the pack to restore.",
                                   parent=self)
            return

        if not messagebox.askyesno(
                "Restore Original Voice",
                f"The robot will load '{pack.label}' directly from Dreame, "
                f"restoring the original voice.\n\nContinue?",
                parent=self):
            return

        cloud, device = self.state.cloud, self.state.device
        self.log.clear()
        self.log.append("Restoring original voice", "step")
        self._busy(True, abbrechbar=False)
        self.progress.configure(value=0)

        def work(_task):
            return installer.restore_official(
                cloud=cloud, device=device, pack=pack,
                log=lambda m: self._log(m), step=self._step)

        def ok(outcome: installer.InstallOutcome) -> None:
            # Auch der Notausgang muss zwischen belegt und nur
            # wahrscheinlich unterscheiden. Er ist der Weg, den jemand
            # geht, WEIL etwas kaputt ist - ein grünes "wieder aktiv"
            # ohne Nachweis wäre hier am schädlichsten.
            kind = "ok" if (outcome.success and outcome.bestaetigt) else "warn"
            self.badge.set(outcome.message, kind)
            self.log.append(outcome.message, kind)
            if outcome.hint:
                self.log.append(outcome.hint, "warn")
            self.progress.configure(value=100 if outcome.success else 0)

        run_async(self, work, on_success=ok, on_error=self._on_error,
                  on_finally=lambda: self._busy(False))

    # ------------------------------------------------------------------
    def _on_error(self, exc: Exception) -> None:
        message, hint = error_text(exc)
        self.badge.set("Failed", "error")
        self.log.append(message, "error")
        if hint:
            self.log.append(hint, "warn")
        show_error(self, self.theme, "Error",
                       message + (f"\n\n{hint}" if hint else ""))
