"""Seite 'Einzelne Ansagen': jede Ansage einzeln mit einer eigenen Datei belegen."""

from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Optional

from .. import audio, embedded, ffmpeg_setup, importer, official
from ..errors import DreameError
from ..i18n import t
from ..paths import data_dir, preview_dir
from ..sounds import Sound
from .state import AppState, error_text, run_async, spaeter, to_main
from .theme import Theme
from .widgets import (Card, InfoBanner, ScrollablePage, StatusBadge, show_error,
                      show_info, show_warning)


def open_folder(path: Path) -> None:
    """Öffnet einen Ordner im Explorer."""
    try:
        if sys.platform == "win32":
            os.startfile(str(path))  # noqa: S606
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError:
        pass

def _audio_filetypes() -> list:
    # Gebaut statt als Modulkonstante, damit t() erst zur Laufzeit
    # nachschaut - beim Modulimport steht die Sprache noch nicht fest.
    return [
        (t("tab_builder.filetype_audio"), "*.ogg *.wav *.mp3 *.m4a *.flac *.aac *.opus *.wma"),
        (t("tab_builder.filetype_ogg"), "*.ogg"),
        ("WAV", "*.wav"),
        ("MP3", "*.mp3"),
        (t("tab_builder.filetype_all"), "*.*"),
    ]

PAGE_SIZE = 100


def open_with_default_player(path: Path) -> None:
    """Spielt eine Datei mit dem Standardprogramm des Systems ab."""
    if sys.platform == "win32":
        os.startfile(str(path))  # noqa: S606 - gewollt: Standardplayer des Nutzers
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


#: Wie breit der Text einer Ansagezeile umbrechen darf.
#:
#: Gemessen, nicht geschätzt: Die Spalte ist 272 Pixel breit.
#: Vorher stand hier 430 - der Text lief einfach über den Rand
#: hinaus und brach mitten im Wort ab, gerade bei der englischen
#: Originalansage, die verrät, worum es überhaupt geht.
ZEILENBREITE = 262


class SoundRow(ttk.Frame):
    """Eine Zeile: Nummer, Beschreibung, Hörprobe, Dateiwahl."""

    def __init__(self, master, theme: Theme, tab: "BuilderTab", sound: Sound) -> None:
        super().__init__(master, style="Card.TFrame")
        self.theme = theme
        self.tab = tab
        self.sound = sound

        self.columnconfigure(1, weight=1)

        # Nummer
        num = ttk.Label(self, text=str(sound.id), style="Mono.TLabel",
                        width=5, anchor="e")
        num.grid(row=0, column=0, rowspan=2, sticky="ne", padx=(0, 10), pady=(4, 0))

        # Beschreibung
        # 430 war Wunschdenken: Die Spalte ist real 272 Pixel breit, und
        # sie wächst auch im Vollbild nicht mit (ScrollablePage deckelt
        # die Seite bei 940). Der Text brach dadurch mitten im Wort ab -
        # bei 28 von 43 Zeilen, ohne Auslassungspunkte.
        title = ttk.Label(self, text=sound.title, style="Surface.TLabel",
                          anchor="w", wraplength=ZEILENBREITE, justify="left")
        title.grid(row=0, column=1, sticky="ew")

        sub_parts = [sound.group]
        if sound.de and sound.en:
            sub_parts.append(f"Original (EN): {sound.en}")
        elif not sound.de and not sound.en:
            sub_parts.append(t("tab_builder.no_description"))
        subtitle = ttk.Label(self, text="  ·  ".join(sub_parts), style="Muted.TLabel",
                             anchor="w", wraplength=ZEILENBREITE, justify="left")
        subtitle.grid(row=1, column=1, sticky="ew", pady=(1, 0))

        # Bedienelemente
        controls = ttk.Frame(self, style="Card.TFrame")
        controls.grid(row=0, column=2, rowspan=2, sticky="e", padx=(12, 0))

        self.btn_preview = ttk.Button(controls, text=t("tab_builder.listen_original"),
                                      style="Small.TButton",
                                      command=self._play_original)
        self.btn_preview.pack(side="left", padx=(0, 6))

        self.var_path = tk.StringVar(value=tab.state.config.assignment(sound.id))
        self.entry = ttk.Entry(controls, textvariable=self.var_path, width=34)
        self.entry.pack(side="left", padx=(0, 6))
        self.entry.bind("<FocusOut>", lambda _e: self._store())

        ttk.Button(controls, text=t("tab_builder.browse_button"), style="Small.TButton",
                   command=self._browse).pack(side="left", padx=(0, 6))
        ttk.Button(controls, text="✕", style="Small.TButton", width=3,
                   command=self._clear).pack(side="left")

        self.hint = ttk.Label(self, text="", style="Muted.TLabel",
                              wraplength=760, justify="left")
        self.hint.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(2, 0))

        ttk.Frame(self, style="Separator.TFrame", height=1).grid(
            row=3, column=0, columnspan=3, sticky="ew", pady=(8, 8))

        self._update_preview_state()
        self._update_hint()

    # ------------------------------------------------------------------
    def _update_preview_state(self) -> None:
        available = self.sound.id in self.tab.state.previews
        self.btn_preview.configure(state="normal" if available else "disabled")
        if not available:
            self.btn_preview.configure(text=t("tab_builder.listen_original"))

    def _play_original(self) -> None:
        path = self.tab.state.previews.get(self.sound.id)
        if not path or not path.is_file():
            messagebox.showinfo(
                t("tab_builder.no_preview_title"),
                t("tab_builder.no_preview_body"),
                parent=self)
            return
        try:
            open_with_default_player(path)
        except OSError as exc:
            show_error(self, self.theme, t("tab_builder.playback_error_title"),
                       t("tab_builder.playback_error_body", path=path, exc=exc))

    def _browse(self) -> None:
        initial = (self.tab.state.config["last_audio_dir"]
                   or str(Path.home() / "Music"))
        # Der vorgeschlagene Name ist genau der, den der Ordner-Import
        # später erwartet - so passt beides zusammen.
        chosen = filedialog.askopenfilename(
            parent=self,
            title=t("tab_builder.browse_dialog_title", id=self.sound.id,
                    title=self.sound.title,
                    filename=importer.suggested_filename(self.sound.id)),
            initialdir=initial if Path(initial).is_dir() else str(Path.home()),
            initialfile=importer.suggested_filename(self.sound.id),
            filetypes=_audio_filetypes(),
        )
        if not chosen:
            return
        self.var_path.set(chosen)
        self.tab.state.config["last_audio_dir"] = str(Path(chosen).parent)
        self._store()

    def _clear(self) -> None:
        self.var_path.set("")
        self._store()

    def _store(self) -> None:
        value = self.var_path.get().strip().strip('"')
        self.var_path.set(value)
        self.tab.state.config.set_assignment(self.sound.id, value)
        # Sobald der Nutzer selbst etwas zuweist, gilt wieder sein eigenes Paket.
        self.tab.state.prebuilt = None
        self.tab.state.prebuilt_name = ""
        self.tab.state.save()
        self._update_hint()
        self.tab.refresh_counter()

    def _update_hint(self) -> None:
        value = self.var_path.get().strip()
        if not value:
            self.hint.configure(text="", style="Muted.TLabel")
            return

        path = Path(value)
        if not path.is_file():
            self.hint.configure(text=t("tab_builder.file_missing"),
                                style="Danger.TLabel")
            return

        warning = audio.check_input_file(path)
        if warning:
            self.hint.configure(text=warning, style="Warning.TLabel")
        else:
            size_kb = path.stat().st_size // 1024
            self.hint.configure(text=t("tab_builder.file_ready", name=path.name, size_kb=size_kb),
                                style="Success.TLabel")

    def refresh(self) -> None:
        self.var_path.set(self.tab.state.config.assignment(self.sound.id))
        self._update_preview_state()
        self._update_hint()


class BuilderTab(ttk.Frame):
    def __init__(self, master, theme: Theme, state: AppState) -> None:
        super().__init__(master, style="TFrame")
        self.theme = theme
        self.state = state
        self._rows: List[SoundRow] = []
        self._shown = PAGE_SIZE
        self._ffmpeg_busy = False
        self._build()
        state.subscribe("device_changed", self._on_device_changed)
        state.subscribe("base_pack_changed", self.rebuild_list)

    # ------------------------------------------------------------------
    def _build(self) -> None:
        self.page = ScrollablePage(self, self.theme)
        self.page.pack(fill="both", expand=True)
        outer = self.page.body()

        InfoBanner(
            outer, self.theme,
            t("tab_builder.info_banner"),
        ).pack(fill="x", pady=(0, 14))

        # ---- Basis -----------------------------------------------------
        base = Card(outer, self.theme, t("tab_builder.step1_title"),
                    t("tab_builder.step1_body"))
        base.pack(fill="x")

        row = ttk.Frame(base.content, style="Card.TFrame")
        row.pack(fill="x")
        ttk.Label(row, text=t("tab_builder.language_label"), style="Surface.TLabel").pack(side="left",
                                                                    padx=(0, 10))
        self.var_language = tk.StringVar(value=t("tab_builder.default_language_value"))
        self.combo_language = ttk.Combobox(row, textvariable=self.var_language,
                                           state="readonly", width=34, values=[])
        self.combo_language.pack(side="left")

        self.btn_load_base = ttk.Button(row, text=t("tab_builder.download_pack_button"),
                                        style="Accent.TButton",
                                        command=self._on_load_base)
        self.btn_load_base.pack(side="left", padx=(12, 0))

        self.base_badge = StatusBadge(row, self.theme, t("tab_builder.not_loaded_yet"))
        self.base_badge.pack(side="left", padx=(14, 0))

        self.base_progress = ttk.Progressbar(base.content, mode="determinate",
                                             maximum=100)

        # ---- ffmpeg ----------------------------------------------------
        self.ffmpeg_banner = ttk.Frame(base.content, style="Card.TFrame")
        self.ffmpeg_banner.pack(fill="x", pady=(12, 0))
        self.lbl_ffmpeg = ttk.Label(self.ffmpeg_banner, text="", style="Muted.TLabel",
                                    wraplength=820, justify="left")
        self.lbl_ffmpeg.pack(anchor="w")

        ffmpeg_actions = ttk.Frame(self.ffmpeg_banner, style="Card.TFrame")
        ffmpeg_actions.pack(anchor="w", pady=(6, 0))
        self.btn_ffmpeg = ttk.Button(ffmpeg_actions, text=t("tab_builder.ffmpeg_setup_button"),
                                     style="Small.TButton", command=self._on_setup_ffmpeg)
        self.ffmpeg_progress = ttk.Progressbar(ffmpeg_actions, mode="determinate",
                                               maximum=100, length=200)
        self._check_ffmpeg()

        # ---- Zuweisungen ------------------------------------------------
        assign = Card(outer, self.theme, t("tab_builder.step2_title"),
                      t("tab_builder.step2_body"))
        assign.pack(fill="both", expand=True, pady=(14, 0))

        filters = ttk.Frame(assign.content, style="Card.TFrame")
        filters.pack(fill="x", pady=(0, 10))

        ttk.Label(filters, text=t("tab_builder.search_label"), style="Surface.TLabel").pack(side="left")
        self.var_search = tk.StringVar()
        search_entry = ttk.Entry(filters, textvariable=self.var_search, width=26)
        search_entry.pack(side="left", padx=(8, 16))
        search_entry.bind("<KeyRelease>", lambda _e: self._debounced_rebuild())

        ttk.Label(filters, text=t("tab_builder.category_label"), style="Surface.TLabel").pack(side="left")
        self.var_group = tk.StringVar(value=t("tab_builder.all_categories"))
        self.combo_group = ttk.Combobox(filters, textvariable=self.var_group,
                                        state="readonly", width=20,
                                        values=[t("tab_builder.all_categories")])
        self.combo_group.pack(side="left", padx=(8, 16))
        self.combo_group.bind("<<ComboboxSelected>>", lambda _e: self.rebuild_list())

        # Zweite Zeile: In einer einzigen wurde es zu eng - bei der
        # Startgröße des Fensters stand dort "Alle Zuwe", der Rest
        # war abgeschnitten. Ausgerechnet bei einem Knopf, der etwas
        # löscht, muss lesbar sein, WAS er löscht.
        filter2 = ttk.Frame(assign.content, style="Card.TFrame")
        filter2.pack(fill="x", pady=(8, 0))

        self.var_common = tk.BooleanVar(value=True)
        ttk.Checkbutton(filter2, text=t("tab_builder.only_common_checkbox"),
                        variable=self.var_common,
                        command=self.rebuild_list).pack(side="left", padx=(0, 16))

        self.var_assigned = tk.BooleanVar(value=False)
        ttk.Checkbutton(filter2, text=t("tab_builder.only_assigned_checkbox"),
                        variable=self.var_assigned,
                        command=self.rebuild_list).pack(side="left")

        ttk.Button(filter2, text=t("tab_builder.clear_all_button"),
                   style="Small.TButton",
                   command=self._clear_all).pack(side="right")

        # ---- Massenzuweisung ---------------------------------------------
        bulk = ttk.Frame(assign.content, style="Card.TFrame")
        bulk.pack(fill="x", pady=(0, 10))

        ttk.Button(bulk, text=t("tab_builder.import_folder_button"),
                   style="Accent.TButton",
                   command=self._on_import_folder).pack(side="left")
        ttk.Button(bulk, text=t("tab_builder.import_archive_button"),
                   style="Small.TButton",
                   command=self._on_import_archive).pack(side="left", padx=(8, 0))
        ttk.Button(bulk, text=t("tab_builder.create_template_button"),
                   style="Small.TButton",
                   command=self._on_create_template).pack(side="left", padx=(8, 0))

        self.lbl_bulk = ttk.Label(
            bulk,
            text=t("tab_builder.bulk_hint"),
            style="Muted.TLabel", wraplength=285, justify="left")
        self.lbl_bulk.pack(side="left", padx=(14, 0))

        # Kein eigener Scrollbereich mehr: der ganze Tab scrollt. Zwei
        # ineinander liegende Bildlaufbereiche wären mit dem Mausrad kaum
        # zu bedienen.
        self.rows_frame = ttk.Frame(assign.content, style="Card.TFrame")
        self.rows_frame.pack(fill="both", expand=True)

        footer = ttk.Frame(assign.content, style="Card.TFrame")
        footer.pack(fill="x", pady=(10, 0))
        self.lbl_counter = ttk.Label(footer, text="", style="Muted.TLabel")
        self.lbl_counter.pack(side="left")
        self.btn_more = ttk.Button(footer, text=t("tab_builder.show_more_button"),
                                   style="Small.TButton", command=self._show_more)

        self._search_job: Optional[str] = None
        self.rebuild_list()

    # ------------------------------------------------------------------
    def _check_ffmpeg(self, auto_extract: bool = True) -> None:
        found = audio.find_ffmpeg()
        self.state.ffmpeg = found

        if found:
            version = audio.ffmpeg_version(found)
            self.lbl_ffmpeg.configure(
                text=t("tab_builder.ffmpeg_ready", info=version or found.name),
                style="Success.TLabel")
            self.btn_ffmpeg.pack_forget()
            return

        # In der EXE liegt ffmpeg bereits bei - dann muss nichts geladen
        # werden, es wird nur einmalig ausgepackt.
        if embedded.has_ffmpeg():
            self.btn_ffmpeg.pack_forget()
            if auto_extract and not self._ffmpeg_busy:
                self.lbl_ffmpeg.configure(
                    text=t("tab_builder.ffmpeg_unpacking"),
                    style="Muted.TLabel")
                self._extract_embedded_ffmpeg()
            return

        self.lbl_ffmpeg.configure(
            text=t("tab_builder.ffmpeg_not_found"),
            style="Warning.TLabel")
        self.btn_ffmpeg.pack(side="left")

    def _extract_embedded_ffmpeg(self) -> None:
        """Packt das mitgelieferte ffmpeg im Hintergrund aus."""
        self._ffmpeg_busy = True
        self.ffmpeg_progress.pack(side="left", padx=(10, 0))
        self.ffmpeg_progress.configure(value=0)

        def work(_task):
            return embedded.extract_ffmpeg(
                progress=lambda done, total: to_main(
                    self, self.ffmpeg_progress.configure,
                    {"value": (done / total * 100) if total else 0}))

        def ok(path):
            self._ffmpeg_busy = False
            if path:
                self._check_ffmpeg(auto_extract=False)
            else:
                self.lbl_ffmpeg.configure(
                    text=t("tab_builder.ffmpeg_unpack_failed"),
                    style="Warning.TLabel")
                self.btn_ffmpeg.pack(side="left")

        def fail(_exc):
            self._ffmpeg_busy = False
            self._check_ffmpeg(auto_extract=False)

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.ffmpeg_progress.pack_forget())

    def _on_setup_ffmpeg(self) -> None:
        if not messagebox.askyesno(t("tab_builder.ffmpeg_setup_confirm_title"),
                                   ffmpeg_setup.describe_source()
                                   + t("tab_builder.ffmpeg_setup_confirm_question"),
                                   parent=self):
            return

        self.btn_ffmpeg.configure(state="disabled")
        self.ffmpeg_progress.pack(side="left", padx=(10, 0))
        self.ffmpeg_progress.configure(value=0)
        self.lbl_ffmpeg.configure(text=t("tab_builder.ffmpeg_downloading"),
                                  style="Muted.TLabel")

        def report(done: int, total: int) -> None:
            percent = (done / total * 100) if total else 0
            to_main(self, self.ffmpeg_progress.configure, {"value": percent})
            to_main(self, self.lbl_ffmpeg.configure,
                    {"text": t("tab_builder.ffmpeg_downloading_progress",
                               done_mb=done // (1024 * 1024),
                               total_mb=(total or 1) // (1024 * 1024))})

        def work(task):
            return ffmpeg_setup.download_and_install(
                progress=report,
                log=lambda m: to_main(self, self.lbl_ffmpeg.configure, {"text": m}),
                cancelled=lambda: task.cancelled,
            )

        def ok(_path):
            self._check_ffmpeg()
            messagebox.showinfo(t("tab_builder.ffmpeg_setup_done_title"),
                                t("tab_builder.ffmpeg_setup_done_body"), parent=self)

        def fail(exc):
            message, hint = error_text(exc)
            self._check_ffmpeg()
            show_error(self, self.theme, t("tab_builder.ffmpeg_setup_failed_title"),
                       message + (f"\n\n{hint}" if hint else ""))

        def done():
            self.btn_ffmpeg.configure(state="normal")
            self.ffmpeg_progress.pack_forget()

        run_async(self, work, on_success=ok, on_error=fail, on_finally=done)

    # ------------------------------------------------------------------
    def _on_device_changed(self) -> None:
        # Das Verwerfen des alten Gerätestands passiert in AppState.notify -
        # unabhängig davon, ob diese Seite überhaupt schon gebaut wurde.
        self.base_badge.set(t("tab_builder.not_loaded_yet"), "muted")
        self.combo_language.configure(values=[])
        self._load_catalog_async()

    def _load_catalog_async(self) -> None:
        model = self.state.model
        if not model:
            return

        def work(_task):
            return official.fetch_catalog(model)

        def ok(packs):
            self.state.official_packs = packs
            labels = [p.label for p in packs]
            self.combo_language.configure(values=labels)
            preferred = self.state.config["base_language"]
            match = official.find_pack(packs, preferred) or official.find_pack(packs, "DE")
            if match:
                self.var_language.set(match.label)
            elif labels:
                self.var_language.set(labels[0])
            self.base_badge.set(t("tab_builder.languages_available", count=len(packs)), "muted")

        def fail(exc):
            message, hint = error_text(exc)
            self.base_badge.set(t("tab_builder.language_list_error"), "error")
            self.lbl_ffmpeg.configure(text=f"{message} {hint}".strip(),
                                      style="Warning.TLabel")

        run_async(self, work, on_success=ok, on_error=fail)

    def _selected_pack(self):
        label = self.var_language.get()
        for pack in self.state.official_packs:
            if pack.label == label:
                return pack
        return None

    def _on_load_base(self) -> None:
        if not self.state.model:
            messagebox.showwarning(
                t("tab_builder.no_robot_title"),
                t("tab_builder.no_robot_body"),
                parent=self)
            return

        if not self.state.official_packs:
            self._load_catalog_async()
            messagebox.showinfo(
                t("tab_builder.loading_languages_title"),
                t("tab_builder.loading_languages_body"),
                parent=self)
            return

        pack = self._selected_pack()
        if pack is None:
            messagebox.showwarning(t("tab_builder.no_language_title"),
                                   t("tab_builder.no_language_body"),
                                   parent=self)
            return

        model = self.state.model
        self.btn_load_base.configure(state="disabled")
        self.base_progress.pack(fill="x", pady=(10, 0))
        self.base_progress.configure(value=0)
        self.base_badge.set(t("tab_builder.loading_pack"), "muted")

        def report(done: int, total: int) -> None:
            percent = (done / total * 100) if total else 0
            to_main(self, self.base_progress.configure, {"value": percent})

        def work(_task):
            path = official.download_pack(pack, model, progress=report)
            to_main(self, self.base_badge.set, t("tab_builder.extracting_samples"), "muted")
            previews = official.extract_previews(
                path, preview_dir() / f"{model}_{pack.id}")
            return pack, path, previews

        def ok(result):
            selected_pack, path, previews = result
            self.state.base_pack_path = path
            self.state.base_pack_info = selected_pack
            self.state.previews = previews
            self.state.config["base_language"] = selected_pack.id
            self.state.save()

            summary = official.describe_pack(path)
            self.base_badge.set(t("tab_builder.pack_ready", summary=summary), "ok")

            # Katalog auf die IDs beschränken, die dieses Modell wirklich kennt.
            ids = sorted(previews.keys())
            if ids:
                self.state.catalog = self.state.catalog.restrict_to(ids)
            self.state.notify("base_pack_changed")
            self.rebuild_list()

        def fail(exc):
            message, hint = error_text(exc)
            self.base_badge.set(t("tab_builder.download_failed_title"), "error")
            show_error(self, self.theme, t("tab_builder.original_pack_not_loaded_title"),
                       message + (f"\n\n{hint}" if hint else ""))

        def done():
            self.btn_load_base.configure(state="normal")
            self.base_progress.pack_forget()

        run_async(self, work, on_success=ok, on_error=fail, on_finally=done)

    # ------------------------------------------------------------------
    def _debounced_rebuild(self) -> None:
        if self._search_job is not None:
            self.after_cancel(self._search_job)
        self._search_job = spaeter(self, 220, self.rebuild_list)

    def _visible_sounds(self) -> List[Sound]:
        group = self.var_group.get()
        group = "" if group == t("tab_builder.all_categories") else group
        sounds = self.state.catalog.filtered(
            group=group,
            search=self.var_search.get(),
            only_common=self.var_common.get(),
        )
        if self.var_assigned.get():
            assigned = set(self.state.assignments().keys())
            sounds = [s for s in sounds if s.id in assigned]
        return sounds

    def rebuild_list(self) -> None:
        self._search_job = None

        groups = [t("tab_builder.all_categories")] + self.state.catalog.groups()
        if list(self.combo_group.cget("values")) != groups:
            self.combo_group.configure(values=groups)
            if self.var_group.get() not in groups:
                self.var_group.set(t("tab_builder.all_categories"))

        sounds = self._visible_sounds()
        self._shown = min(max(self._shown, PAGE_SIZE), max(len(sounds), PAGE_SIZE))

        for child in self.rows_frame.winfo_children():
            child.destroy()
        self._rows = []

        if not sounds:
            ttk.Label(self.rows_frame,
                      text=t("tab_builder.no_matches"),
                      style="Muted.TLabel").pack(anchor="w", pady=20, padx=4)
        else:
            for sound in sounds[:self._shown]:
                row = SoundRow(self.rows_frame, self.theme, self, sound)
                row.pack(fill="x", padx=4)
                self._rows.append(row)

        self.page.canvas.yview_moveto(0.0)
        self._update_footer(len(sounds))
        self.refresh_counter()

    def _update_footer(self, total: int) -> None:
        if total > self._shown:
            self.btn_more.configure(
                text=t("tab_builder.show_more_count", count=min(PAGE_SIZE, total - self._shown)))
            self.btn_more.pack(side="right")
        else:
            self.btn_more.pack_forget()

    def _show_more(self) -> None:
        self._shown += PAGE_SIZE
        self.rebuild_list()

    def refresh_counter(self) -> None:
        assigned = len(self.state.assignments())
        total = len(self.state.catalog)
        missing = len(self.state.missing_assignments())

        text = t("tab_builder.counter_replaced", assigned=assigned, total=total)
        shown = len(self._rows)
        if shown:
            text += t("tab_builder.counter_shown", shown=shown)
        if missing:
            text += t("tab_builder.counter_missing", missing=missing)

        self.lbl_counter.configure(
            text=text, style="Warning.TLabel" if missing else "Muted.TLabel")
        self.state.notify("assignments_changed")

    # ------------------------------------------------------------------
    def _on_import_folder(self) -> None:
        ordner = filedialog.askdirectory(
            parent=self, title=t("tab_builder.choose_audio_folder_title"),
            initialdir=self.state.config["last_audio_dir"] or str(Path.home()))
        if ordner:
            self._import_from(lambda: importer.scan_folder(
                Path(ordner), self.state.catalog.ids()))

    def _on_import_archive(self) -> None:
        datei = filedialog.askopenfilename(
            parent=self, title=t("tab_builder.choose_archive_title"),
            initialdir=self.state.config["last_audio_dir"] or str(Path.home()),
            filetypes=[(t("tab_builder.filetype_archives"), "*.tar.gz *.tgz *.zip"),
                       (t("tab_builder.filetype_all_archive"), "*.*")])
        if datei:
            self._import_from(lambda: importer.import_archive(
                Path(datei), data_dir() / t("tab_builder.imported_folder_name"),
                self.state.catalog.ids()))

    def _import_from(self, arbeit) -> None:
        """Führt einen Import aus und meldet das Ergebnis verständlich."""
        def work(_task):
            return arbeit()

        def ok(ergebnis: importer.ImportResult) -> None:
            if not ergebnis.assigned:
                show_warning(
                    self, self.theme, t("tab_builder.import_nothing_found_title"),
                    t("tab_builder.import_nothing_found_line1"),
                    t("tab_builder.import_nothing_found_line2")
                    + self._skipped_text(ergebnis))
                return

            vorher = set(self.state.assignments())
            neu = [i for i in ergebnis.assigned if i not in vorher]
            ersetzt = [i for i in ergebnis.assigned if i in vorher]

            frage = (t("tab_builder.import_summary_header", count=len(ergebnis.assigned))
                     + t("tab_builder.import_summary_new", count=len(neu))
                     + t("tab_builder.import_summary_overwritten", count=len(ersetzt)))
            if ergebnis.unknown_ids:
                frage += t("tab_builder.import_summary_unknown", count=len(ergebnis.unknown_ids))
            if ergebnis.skipped:
                frage += t("tab_builder.import_summary_skipped", count=len(ergebnis.skipped))
            frage += t("tab_builder.import_summary_apply")

            if not messagebox.askyesno(t("tab_builder.review_import_title"), frage, parent=self):
                return

            for sound_id, pfad in ergebnis.assigned.items():
                self.state.config.set_assignment(sound_id, str(pfad))
            self.state.prebuilt = None
            self.state.prebuilt_name = ""
            self.state.config["last_audio_dir"] = str(
                Path(next(iter(ergebnis.assigned.values()))).parent)
            self.state.save()

            self.rebuild_list()
            show_info(self, self.theme, t("tab_builder.import_complete_title"),
                      ergebnis.summary(),
                      self._skipped_text(ergebnis))

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            show_error(self, self.theme, t("tab_builder.import_failed_title"), message, hint)

        run_async(self, work, on_success=ok, on_error=fail)

    @staticmethod
    def _skipped_text(ergebnis: importer.ImportResult) -> str:
        zeilen = []
        if ergebnis.unknown_ids:
            nummern = sorted(set(ergebnis.unknown_ids))
            zeilen.append(t("tab_builder.unknown_numbers_prefix")
                          + ", ".join(str(n) for n in nummern[:20])
                          + (" ..." if len(nummern) > 20 else ""))
        if ergebnis.skipped:
            zeilen.append(t("tab_builder.skipped_label"))
            zeilen += [f"   · {n}" for n in ergebnis.skipped[:15]]
            if len(ergebnis.skipped) > 15:
                zeilen.append(t("tab_builder.skipped_more", count=len(ergebnis.skipped) - 15))
        return "\n".join(zeilen)

    # ------------------------------------------------------------------
    def _on_create_template(self) -> None:
        """Legt einen Ordner mit allen Originalansagen zum Nachsprechen an."""
        if not self.state.previews:
            show_warning(
                self, self.theme, t("tab_builder.original_pack_missing_title"),
                t("tab_builder.original_pack_missing_line1"),
                t("tab_builder.original_pack_missing_line2"))
            return

        nur_wichtige = messagebox.askyesno(
            t("tab_builder.choose_scope_title"),
            t("tab_builder.choose_scope_question")
            + t("tab_builder.choose_scope_yes",
                count=len(self.state.catalog.filtered(only_common=True)))
            + t("tab_builder.choose_scope_no", count=len(self.state.previews)),
            parent=self)

        ziel = filedialog.askdirectory(
            parent=self, title=t("tab_builder.template_folder_dialog_title"),
            initialdir=self.state.config["last_audio_dir"] or str(Path.home()))
        if not ziel:
            return

        ordner = Path(ziel) / t("tab_builder.my_announcements_folder")
        ids = ([s.id for s in self.state.catalog.filtered(only_common=True)]
               if nur_wichtige else None)

        def work(_task):
            return importer.create_template_folder(
                self.state.previews, self.state.catalog, ordner, ids)

        def ok(pfad: Path) -> None:
            anzahl = len(list(pfad.glob("*.ogg")))
            self.state.config["last_audio_dir"] = str(pfad)
            self.state.save()
            show_info(
                self, self.theme, t("tab_builder.template_created_title"),
                t("tab_builder.template_created_line1", count=anzahl, path=pfad),
                t("tab_builder.template_created_line2"))
            open_folder(pfad)

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            show_error(self, self.theme, t("tab_builder.template_failed_title"),
                       message, hint)

        run_async(self, work, on_success=ok, on_error=fail)

    def _clear_all(self) -> None:
        if not self.state.config["assignments"]:
            return
        if not messagebox.askyesno(
                t("tab_builder.clear_confirm_title"),
                t("tab_builder.clear_confirm_body"),
                parent=self):
            return
        self.state.config.clear_assignments()
        self.state.save()
        self.rebuild_list()

    def refresh_rows(self) -> None:
        for row in self._rows:
            row.refresh()
