"""Seite 'Eigene Stimmen': Dialekte, eigene Pakete und Sprachsynthese."""

from __future__ import annotations

import hashlib
import shutil
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Optional

from .. import (community, custom, dialect, elevenlabs, importer, installer,
                library, packer, textfiles, tts)
from ..community import CommunityPack
from ..config import Config
from ..i18n import t
from ..paths import build_dir
from .state import AppState, error_text, run_async, to_main
from .tab_builder import open_with_default_player
from .theme import Theme
from .widgets import (Card, InfoBanner, LogView, ScrollableList, ScrollablePage,
                      StatusBadge, show_error, show_info, show_warning)


class PackCard(ttk.Frame):
    """Ein Community-Paket als Kachel."""

    def __init__(self, master, theme: Theme, tab: "StoreTab",
                 pack: CommunityPack) -> None:
        super().__init__(master, style="Card.TFrame")
        self.theme = theme
        self.tab = tab
        self.pack_info = pack

        self.columnconfigure(0, weight=1)

        head = ttk.Frame(self, style="Card.TFrame")
        head.grid(row=0, column=0, sticky="ew")
        ttk.Label(head, text=pack.name, style="Heading.TLabel").pack(side="left")

        meta = t("tab_store.pack_card_meta", language=pack.language,
                 count=pack.approx_sounds)
        if pack.size_mb:
            meta += f"  ·  {pack.size_mb:.1f} MB"
        ttk.Label(head, text=meta, style="Muted.TLabel").pack(side="left", padx=(12, 0))

        ttk.Label(self, text=pack.description, style="Surface.TLabel",
                  wraplength=700, justify="left").grid(row=1, column=0, sticky="ew",
                                                       pady=(4, 0))

        source = t("tab_store.pack_card_source", author=pack.author,
                   license=pack.license)
        ttk.Label(self, text=source, style="Muted.TLabel").grid(
            row=2, column=0, sticky="w", pady=(4, 0))

        if pack.notes:
            ttk.Label(self, text=pack.notes, style="Warning.TLabel",
                      wraplength=700, justify="left").grid(row=3, column=0,
                                                           sticky="ew", pady=(4, 0))

        buttons = ttk.Frame(self, style="Card.TFrame")
        buttons.grid(row=4, column=0, sticky="w", pady=(10, 0))

        self.btn_use = ttk.Button(buttons, text=t("tab_store.download_and_adapt_button"),
                                  style="Accent.TButton",
                                  command=lambda: tab.use_pack(pack))
        self.btn_use.pack(side="left")

        ttk.Button(buttons, text=t("tab_store.view_project_page_button"), style="Small.TButton",
                   command=lambda: webbrowser.open(pack.project_url)).pack(
            side="left", padx=(8, 0))

        ttk.Frame(self, style="Separator.TFrame", height=1).grid(
            row=5, column=0, sticky="ew", pady=(14, 12))


class StoreTab(ttk.Frame):
    def __init__(self, master, theme: Theme, state: AppState) -> None:
        super().__init__(master, style="TFrame")
        self.theme = theme
        self.state = state
        self._dialect_buttons: list[ttk.Button] = []
        self._build()

    # ------------------------------------------------------------------
    def _build(self) -> None:
        self.page = ScrollablePage(self, self.theme)
        self.page.pack(fill="both", expand=True)
        outer = self.page.body()

        InfoBanner(
            outer, self.theme,
            t("tab_store.store_disclaimer"),
        ).pack(fill="x", pady=(0, 14))

        self._build_dialect_card(outer)

        listing = Card(outer, self.theme, t("tab_store.available_packs_heading"))
        listing.pack(fill="both", expand=True, pady=(14, 0))

        # Der ganze Tab scrollt bereits - hier kein zweiter Bildlaufbereich.
        self.list_frame = ttk.Frame(listing.content, style="Card.TFrame")
        self.list_frame.pack(fill="both", expand=True)

        for pack in community.PACKS:
            card = PackCard(self.list_frame, self.theme, self, pack)
            card.pack(fill="x", padx=4)

        status = ttk.Frame(listing.content, style="Card.TFrame")
        status.pack(fill="x", pady=(10, 0))
        self.badge = StatusBadge(status, self.theme, t("tab_store.status_ready"))
        self.badge.pack(side="left")
        self.progress = ttk.Progressbar(status, mode="determinate", maximum=100,
                                        length=220)

        self.log = LogView(listing.content, self.theme, height=8)
        self.log.pack(fill="both", expand=False, pady=(10, 0))

    # ------------------------------------------------------------------
    def _build_dialect_card(self, outer) -> None:
        """Dialektpakete, die die App selbst spricht."""
        umfaenge = sorted(p.count for p in dialect.DIALECTS)
        spanne = (f"{umfaenge[0]} bis {umfaenge[-1]}" if umfaenge[0] != umfaenge[-1]
                  else str(umfaenge[0]))
        card = Card(outer, self.theme, t("tab_store.dialect_card_title"),
                    t("tab_store.dialect_card_subtitle",
                      count=len(dialect.DIALECTS), span=spanne))
        card.pack(fill="x")

        ttk.Label(
            card.content,
            text=t("tab_store.dialect_intro"),
            style="Surface.TLabel", wraplength=820, justify="left").pack(anchor="w")

        # --- Dialektauswahl ---------------------------------------------
        picker = ttk.Frame(card.content, style="Card.TFrame")
        picker.pack(fill="x", pady=(14, 0))
        ttk.Label(picker, text=t("tab_store.dialect_label"), style="Surface.TLabel").pack(side="left")

        self.var_dialect = tk.StringVar()
        self.combo_dialect = ttk.Combobox(
            picker, textvariable=self.var_dialect, state="readonly", width=34)
        self.combo_dialect.pack(side="left", padx=(8, 0))
        self.combo_dialect.bind("<<ComboboxSelected>>",
                                lambda _e: self._on_dialect_changed())

        self.lbl_dialect_meta = ttk.Label(picker, text="", style="Muted.TLabel")
        self.lbl_dialect_meta.pack(side="left", padx=(14, 0))

        # --- Eigene Pakete verwalten ------------------------------------
        eigene = ttk.Frame(card.content, style="Card.TFrame")
        eigene.pack(fill="x", pady=(8, 0))
        ttk.Button(eigene, text=t("tab_store.create_pack_button"),
                   style="Small.TButton",
                   command=self._on_new_custom).pack(side="left")
        self.btn_rename = ttk.Button(eigene, text=t("tab_store.rename_button"),
                                     style="Small.TButton",
                                     command=self._on_rename_custom)
        self.btn_rename.pack(side="left", padx=(8, 0))
        self.btn_delete_custom = ttk.Button(eigene, text=t("tab_store.delete_button"),
                                            style="Small.TButton",
                                            command=self._on_delete_custom)
        self.btn_delete_custom.pack(side="left", padx=(8, 0))
        ttk.Button(eigene, text=t("tab_store.import_recordings_button"),
                   style="Small.TButton",
                   command=self._on_import_ready).pack(side="left", padx=(8, 0))

        ttk.Label(card.content,
                  text=t("tab_store.custom_pack_intro"),
                  style="Muted.TLabel", wraplength=820,
                  justify="left").pack(anchor="w", pady=(6, 0))

        self.lbl_dialect_desc = ttk.Label(card.content, text="",
                                          style="Surface.TLabel",
                                          wraplength=800, justify="left")
        self.lbl_dialect_desc.pack(anchor="w", pady=(8, 0))

        self.lbl_samples = ttk.Label(card.content, text="", style="Muted.TLabel",
                                     justify="left")
        self.lbl_samples.pack(anchor="w", pady=(6, 0))

        # Zwischenstand: wie weit ein früherer Lauf gekommen ist.
        fortschritt = ttk.Frame(card.content, style="Card.TFrame")
        fortschritt.pack(fill="x", pady=(10, 0))
        self.lbl_fortschritt = ttk.Label(fortschritt, text="",
                                         style="Muted.TLabel",
                                         wraplength=700, justify="left")
        self.lbl_fortschritt.pack(side="left")
        self.btn_verwerfen = ttk.Button(
            fortschritt, text=t("tab_store.discard_progress_button"), style="Small.TButton",
            command=self._on_discard_progress)

        self._build_engine_chooser(card.content)

        # --- Aktionen ----------------------------------------------------
        actions = ttk.Frame(card.content, style="Card.TFrame")
        actions.pack(fill="x", pady=(14, 0))

        self.btn_preview = ttk.Button(actions, text=t("tab_store.listen_sample_button"),
                                      command=self._on_preview_dialect)
        self.btn_preview.pack(side="left")
        self._dialect_buttons.append(self.btn_preview)

        self.btn_texts = ttk.Button(actions, text=t("tab_store.view_edit_texts_button"),
                                    command=self._on_show_texts)
        self.btn_texts.pack(side="left", padx=(8, 0))

        self.btn_generate = ttk.Button(actions, text=t("tab_store.generate_pack_button"),
                                       style="Accent.TButton",
                                       command=self._on_generate_selected)
        self.btn_generate.pack(side="left", padx=(8, 0))
        self._dialect_buttons.append(self.btn_generate)

        # Absichtlich NICHT in _dialect_buttons: dieser Knopf muss genau
        # dann bedienbar sein, wenn alle anderen gesperrt sind.
        self.btn_abbrechen = ttk.Button(actions, text=t("tab_store.cancel_button"),
                                        command=self._on_cancel_work,
                                        state="disabled")
        self.btn_abbrechen.pack(side="left", padx=(8, 0))

        # --- Textdateien --------------------------------------------------
        dateien = ttk.Frame(card.content, style="Card.TFrame")
        dateien.pack(fill="x", pady=(8, 0))

        ttk.Button(dateien, text=t("tab_store.export_texts_button"),
                   style="Small.TButton",
                   command=self._on_export_texts).pack(side="left")
        ttk.Button(dateien, text=t("tab_store.import_texts_button"),
                   style="Small.TButton",
                   command=self._on_import_texts).pack(side="left", padx=(8, 0))
        ttk.Button(dateien, text=t("tab_store.open_folder_button"), style="Small.TButton",
                   command=self._on_open_text_folder).pack(side="left", padx=(8, 0))

        ttk.Label(card.content,
                  text=t("tab_store.sample_texts_info"),
                  style="Muted.TLabel", wraplength=800,
                  justify="left").pack(anchor="w", pady=(6, 0))

        # Erst hier: die Auswahlliste füllt auch die Beschriftungen, die es
        # weiter oben noch gar nicht gibt.
        self._refill_dialect_picker()

        ttk.Label(
            card.content,
            text=t("tab_store.voice_cloning_legal_notice"),
            style="Muted.TLabel", wraplength=820, justify="left").pack(anchor="w",
                                                                       pady=(10, 0))

    # ------------------------------------------------------------------
    # Auswahlliste: mitgelieferte Dialekte und eigene Pakete
    # ------------------------------------------------------------------
    def _all_packs(self) -> list:
        """Alle wählbaren Pakete: erst die Dialekte, dann die eigenen."""
        try:
            eigene = custom.list_packs()
        except OSError:
            eigene = []
        return list(dialect.DIALECTS) + eigene

    def _label_for(self, pack) -> str:
        vorsatz = (t("tab_store.prefix_custom") if self._is_custom(pack)
                   else t("tab_store.prefix_dialect"))
        return f"{vorsatz}{pack.name}"

    def _is_custom(self, pack) -> bool:
        return not any(d.key == pack.key for d in dialect.DIALECTS)

    def _refill_dialect_picker(self, auswahl: str = "") -> None:
        """Baut die Auswahlliste neu auf und hält die Auswahl fest."""
        self._packs = self._all_packs()
        beschriftungen = [self._label_for(p) for p in self._packs]
        self.combo_dialect.configure(values=beschriftungen)

        vorher = auswahl or self.var_dialect.get()
        if vorher in beschriftungen:
            self.combo_dialect.set(vorher)
        elif beschriftungen:
            self.combo_dialect.set(beschriftungen[0])

        eigene = sum(1 for p in self._packs if self._is_custom(p))
        for knopf in (getattr(self, "btn_rename", None),
                      getattr(self, "btn_delete_custom", None)):
            if knopf is not None:
                knopf.configure(state="normal" if eigene else "disabled")

        self._on_dialect_changed()

    def _selected_dialect(self):
        """Das gewählte Paket mit seinen mitgelieferten Texten."""
        wahl = self.var_dialect.get()
        for pack in getattr(self, "_packs", None) or self._all_packs():
            if self._label_for(pack) == wahl:
                return pack
        # Ältere Fassungen hatten den blanken Namen in der Liste.
        return next((p for p in self._all_packs() if p.name == wahl), None)

    def _effective_dialect(self, pack=None):
        """Der Dialekt so, wie er wirklich gesprochen wird - mit eigenen Texten."""
        pack = pack or self._selected_dialect()
        if pack is None:
            return None
        return dialect.with_overrides(
            pack, self.state.config.dialect_overrides(pack.key))

    def _on_dialect_changed(self) -> None:
        pack = self._selected_dialect()
        if pack is None:
            return
        aktuell = self._effective_dialect(pack)
        eigene = len(dialect.changed_ids(
            pack, self.state.config.dialect_overrides(pack.key)))

        meta = t("tab_store.dialect_meta", count=aktuell.count, lang_id=pack.lang_id)
        if eigene:
            meta += t("tab_store.dialect_meta_custom_edited", count=eigene)
        self.lbl_dialect_meta.configure(text=meta)
        self.lbl_dialect_desc.configure(text=pack.description)
        samples = "\n".join(f"   {line}"
                            for line in dialect.preview_texts(aktuell, 6))
        self.lbl_samples.configure(text=t("tab_store.sample_prefix") + samples)
        self.refresh_progress()

    def _work_dir(self, pack=None) -> Path:
        """Ablageort der Aufnahmen für die aktuelle Stimme und Einstellung."""
        pack = pack or self._selected_dialect()
        if pack is None:
            return build_dir() / "_dialekt" / "unbekannt"

        engine = self.var_engine.get()
        if engine == dialect.ENGINE_ELEVENLABS:
            gewaehlt = self._selected_eleven_voice()
            stimme = gewaehlt.voice_id if gewaehlt else (
                self.state.config["elevenlabs_voice_id"] or "standard")
        else:
            stimme = self._selected_win_voice() or "standard"

        modell, klang, eigene = self._eleven_klang()
        tempo, hoehe = self._win_klang()
        fingerabdruck = hashlib.md5(
            f"{modell}|{eigene}|{sorted((klang or {}).items())}|{tempo}|{hoehe}"
            .encode("utf-8")).hexdigest()[:8]
        kennung = str(stimme).replace(" ", "_")[:40]
        return build_dir() / "_dialekt" / f"{pack.key}_{engine}_{kennung}_{fingerabdruck}"

    def refresh_progress(self) -> None:
        """Zeigt, wie weit ein früherer Lauf gekommen ist."""
        pack = self._effective_dialect()
        if pack is None:
            return

        try:
            ordner = self._work_dir()
            passend, uebernommen, veraltet = dialect.classify_recordings(
                pack, ordner)
        except Exception:
            self.lbl_fortschritt.configure(text="")
            self.btn_verwerfen.pack_forget()
            return

        fertig = len(passend) + len(uebernommen)
        if fertig == 0 and not veraltet:
            self.lbl_fortschritt.configure(
                text=t("tab_store.progress_nothing_yet"),
                style="Muted.TLabel")
            self.btn_verwerfen.pack_forget()
            return

        teile = [t("tab_store.progress_summary", done=fertig, total=pack.count)]
        if uebernommen:
            teile.append(t("tab_store.progress_taken_over", count=len(uebernommen)))
        if veraltet:
            teile.append(t("tab_store.progress_outdated", count=len(veraltet)))
        offen = pack.count - fertig
        if offen > 0:
            teile.append(t("tab_store.progress_remaining", count=offen))
        else:
            teile.append(t("tab_store.progress_complete"))

        self.lbl_fortschritt.configure(
            text="  ·  ".join(teile),
            style="Success.TLabel" if offen == 0 else "Muted.TLabel")
        self.btn_verwerfen.pack(side="right")

    def _on_discard_progress(self) -> None:
        """Wirft die zwischengespeicherten Aufnahmen weg."""
        pack = self._effective_dialect()
        if pack is None:
            return
        ordner = self._work_dir()
        fertig = dialect.spoken_count(ordner)
        if not fertig:
            return

        if not messagebox.askyesno(
                t("tab_store.discard_progress_confirm_title"),
                t("tab_store.discard_progress_confirm_message", count=fertig),
                parent=self):
            return

        try:
            shutil.rmtree(ordner / "gesprochen", ignore_errors=True)
            shutil.rmtree(ordner / "umgewandelt", ignore_errors=True)
        except OSError:
            pass
        self.refresh_progress()
        self.log.append(t("tab_store.progress_discarded_log", count=fertig), "warn")

    # ------------------------------------------------------------------
    # Eigene Pakete anlegen, umbenennen, löschen
    # ------------------------------------------------------------------
    def _on_new_custom(self) -> None:
        """Legt eine eigene Textsammlung an - meist als Kopie eines Dialekts."""
        name = simpledialog.askstring(
            t("tab_store.new_custom_title"),
            t("tab_store.new_custom_prompt"),
            parent=self)
        if not name or not name.strip():
            return

        vorlagen = [t("tab_store.copy_of_template", name=p.name) for p in dialect.DIALECTS]
        vorlagen.append(t("tab_store.start_empty_option"))

        wahl = self._ask_choice(
            t("tab_store.start_with_what_title"),
            t("tab_store.start_with_what_prompt"),
            vorlagen, vorlagen[0])
        if wahl is None:
            return

        texte = {}
        if wahl != t("tab_store.start_empty_option"):
            quelle = next((p for p in dialect.DIALECTS
                           if t("tab_store.copy_of_template", name=p.name) == wahl), None)
            if quelle is not None:
                # Bewusst die wirksamen Texte: eigene Änderungen am Dialekt
                # sollen in der Kopie erhalten bleiben.
                texte = dict(self._effective_dialect(quelle).texts)

        vergeben = [p.lang_id for p in self._all_packs()]
        neu = custom.create(name.strip(), texte, vergeben=vergeben)
        try:
            custom.save(neu)
        except OSError as exc:
            show_error(self, self.theme, t("tab_store.custom_not_saved_title"),
                       t("tab_store.custom_pack_not_created_message"),
                       t("tab_store.technical_details_new_custom", error=exc))
            return

        self.log.append(t("tab_store.custom_pack_created_log", name=neu.name,
                          count=neu.count, lang_id=neu.lang_id), "ok")
        self._refill_dialect_picker(self._label_for(neu))
        show_info(
            self, self.theme, t("tab_store.pack_created_title"),
            t("tab_store.pack_created_message", name=neu.name),
            t("tab_store.pack_created_hint", count=neu.count, lang_id=neu.lang_id,
              filename=custom.path_for(neu.key).name, folder=custom.ORDNER))

    def _on_rename_custom(self) -> None:
        pack = self._selected_dialect()
        if pack is None or not self._is_custom(pack):
            show_warning(self, self.theme, t("tab_store.no_custom_pack_title"),
                         t("tab_store.no_custom_pack_rename_message"),
                         t("tab_store.no_custom_pack_hint"))
            return
        neu = simpledialog.askstring(t("tab_store.rename_dialog_title"),
                                     t("tab_store.rename_dialog_prompt"),
                                     initialvalue=pack.name, parent=self)
        if not neu or not neu.strip():
            return
        custom.rename(pack, neu)
        try:
            custom.save(pack)
        except OSError as exc:
            show_error(self, self.theme, t("tab_store.rename_not_saved_title"), str(exc))
            return
        self._refill_dialect_picker(self._label_for(pack))
        self.log.append(t("tab_store.renamed_log", name=pack.name), "ok")

    def _on_delete_custom(self) -> None:
        pack = self._selected_dialect()
        if pack is None or not self._is_custom(pack):
            show_warning(self, self.theme, t("tab_store.no_custom_pack_title"),
                         t("tab_store.no_custom_pack_delete_message"),
                         t("tab_store.no_custom_pack_hint"))
            return
        if not messagebox.askyesno(
                t("tab_store.really_delete_title"),
                t("tab_store.really_delete_message", name=pack.name, count=pack.count),
                parent=self):
            return
        custom.delete(pack.key)
        self.log.append(t("tab_store.pack_deleted_log", name=pack.name), "warn")
        self._refill_dialect_picker()

    def _on_import_ready(self) -> None:
        """Ein fertiges Paket oder einen Ordner voller Aufnahmen übernehmen."""
        WAHL_ARCHIV = t("tab_store.choice_archive")
        WAHL_ORDNER = t("tab_store.choice_folder")
        WAHL_DANEBEN = t("tab_store.choice_save_alongside")
        WAHL_ERSETZEN = t("tab_store.choice_replace_existing")

        if not self.state.has_base_pack:
            show_warning(
                self, self.theme, t("tab_store.original_pack_missing_title"),
                t("tab_store.original_pack_missing_import_message"),
                t("tab_store.original_pack_missing_import_hint"))
            return

        art = self._ask_choice(
            t("tab_store.what_import_title"),
            t("tab_store.what_import_prompt"),
            [WAHL_ARCHIV, WAHL_ORDNER],
            WAHL_ARCHIV)
        if art is None:
            return

        bekannt = self.state.catalog.ids() if self.state.catalog else None
        start = self.state.config["last_audio_dir"] or str(
            Path.home() / "Downloads")

        if art == WAHL_ARCHIV:
            quelle = filedialog.askopenfilename(
                parent=self, title=t("tab_store.choose_zip_title"),
                initialdir=start if Path(start).is_dir() else str(Path.home()),
                filetypes=[(t("tab_store.filetype_recordings_packs"),
                            "*.zip *.tar.gz *.tgz *.tar"),
                           (t("tab_store.filetype_all_files"), "*.*")])
            if not quelle:
                return
            try:
                gefunden = importer.import_archive(
                    Path(quelle), build_dir() / "_import",
                    known_ids=bekannt, log=lambda m: self._log(m))
            except Exception as exc:                   # noqa: BLE001
                self._on_import_error(exc)
                return
        else:
            quelle = filedialog.askdirectory(
                parent=self, title=t("tab_store.choose_folder_recordings_title"),
                initialdir=start if Path(start).is_dir() else str(Path.home()),
                mustexist=True)
            if not quelle:
                return
            try:
                gefunden = importer.scan_folder(
                    Path(quelle), known_ids=bekannt, log=lambda m: self._log(m))
            except Exception as exc:                   # noqa: BLE001
                self._on_import_error(exc)
                return

        # Beim nächsten Mal dort weitermachen, wo zuletzt etwas lag.
        merken = Path(quelle)
        self.state.config["last_audio_dir"] = str(
            merken if merken.is_dir() else merken.parent)

        zuordnung = gefunden.assigned
        if not zuordnung:
            show_warning(
                self, self.theme, t("tab_store.nothing_found_title"),
                t("tab_store.nothing_found_import_message", name=Path(quelle).name),
                t("tab_store.nothing_found_import_hint"))
            return

        name = simpledialog.askstring(
            t("tab_store.name_for_pack_title"),
            t("tab_store.name_for_pack_import_prompt", count=len(zuordnung)),
            initialvalue=library.safe_name(Path(quelle).stem or "custom_pack"),
            parent=self)
        if name is None:
            return

        # Gibt es den Namen schon, wird gefragt statt stillschweigend eine
        # zweite Fassung danebenzulegen - wer neuere Aufnahmen einliest,
        # will meist die alten ersetzen. Vorgabe bleibt trotzdem das
        # Danebenlegen: ein mit bezahltem Kontingent erzeugtes Paket darf
        # nicht aus Versehen verschwinden.
        sicher = library.safe_name(name)
        schon_da = library.existing_pack(build_dir(), sicher)
        if schon_da is None:
            ziel = build_dir() / f"{sicher}.tar.gz"
        else:
            alt = library.read_info(schon_da)
            wahl = self._ask_choice(
                t("tab_store.pack_exists_title"),
                t("tab_store.pack_exists_message", label=alt.label),
                [WAHL_DANEBEN, WAHL_ERSETZEN], WAHL_DANEBEN)
            if wahl is None:
                return
            if wahl == WAHL_ERSETZEN:
                ziel = schon_da
                self.log.append(t("tab_store.replacing_log", name=schon_da.name), "warn")
            else:
                ziel = library.unique_path(build_dir(), sicher)

        # Früher wurde hier nach einer Kennung gefragt. Die Antwort
        # hatte aufs Aufspielen längst keine Wirkung mehr - eine
        # Frage ohne Folgen ist für Laien nur eine Hürde.
        kennung = installer.DEFAULT_CUSTOM_LANG_ID

        base = self.state.base_pack_path
        ffmpeg = self.state.ffmpeg
        mapping = self.state.voice_mapping()

        self.log.clear()
        self.log.append(t("tab_store.building_pack_log", count=len(zuordnung)), "step")
        self._busy(True)
        self.badge.set(t("tab_store.converting_building_badge"), "muted")

        def work_fn(_task):
            return packer.build_pack(
                base_pack=Path(base), assignments=zuordnung,
                out_name=ziel.name, ffmpeg=ffmpeg,
                work_dir=build_dir() / "_import_arbeit",
                mapping=mapping, log=lambda m: self._log(m))

        def ok(build) -> None:
            library.write_info(build.path, dialect=name.strip() or ziel.stem,
                               engine=t("tab_store.engine_custom_recordings"),
                               voice=Path(quelle).name,
                               lang_id=(kennung or "CUSTOM").strip().upper(),
                               replaced=len(build.replaced),
                               total=len(zuordnung))
            self.state.prebuilt = build
            self.state.prebuilt_name = name.strip() or ziel.stem
            self.state.last_build = build
            self.state.config["custom_lang_id"] = (kennung or "CUSTOM").strip().upper()
            self.state.save()
            self.state.notify("assignments_changed")
            self.badge.set(t("tab_store.import_done_badge", count=len(build.replaced)), "ok")
            self.log.append(build.summary(), "ok")
            for warnung in build.warnings:
                self.log.append(warnung, "warn")
            show_info(self, self.theme, t("tab_store.pack_ready_title"),
                      t("tab_store.pack_ready_message", count=len(build.replaced)),
                      t("tab_store.pack_ready_hint", filename=build.path.name))

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            self.badge.set(t("tab_store.import_failed_badge"), "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, t("tab_store.pack_not_built_title"), message, hint)

        run_async(self, work_fn, on_success=ok, on_error=fail,
                  on_finally=lambda: self._busy(False))

    def _on_import_error(self, exc: Exception) -> None:
        message, hint = error_text(exc)
        self.log.append(message, "error")
        show_error(self, self.theme, t("tab_store.import_failed_title"), message, hint)

    def _ask_choice(self, titel: str, frage: str, optionen: list,
                    vorgabe: str = "") -> Optional[str]:
        """Kleiner Auswahldialog - tkinter bringt keinen mit."""
        fenster = tk.Toplevel(self)
        fenster.title(titel)
        fenster.configure(bg=self.theme.color("bg"))
        fenster.transient(self.winfo_toplevel())
        fenster.grab_set()

        card = Card(fenster, self.theme, titel)
        card.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(card.content, text=frage, style="Surface.TLabel",
                  wraplength=420, justify="left").pack(anchor="w")

        var = tk.StringVar(value=vorgabe or (optionen[0] if optionen else ""))
        # Breit genug für die längste Wahl ("Daneben speichern - ...").
        breite = max(40, *(len(o) for o in optionen)) if optionen else 40
        combo = ttk.Combobox(card.content, textvariable=var, state="readonly",
                             values=optionen, width=min(breite + 2, 60))
        combo.pack(anchor="w", pady=(12, 0))

        ergebnis = {"wert": None}

        def uebernehmen() -> None:
            ergebnis["wert"] = var.get()
            fenster.destroy()

        knoepfe = ttk.Frame(card.content, style="Card.TFrame")
        knoepfe.pack(fill="x", pady=(16, 0))
        ttk.Button(knoepfe, text=t("tab_store.ask_choice_apply_button"), style="Accent.TButton",
                   command=uebernehmen).pack(side="left")
        ttk.Button(knoepfe, text=t("tab_store.ask_choice_cancel_button"),
                   command=fenster.destroy).pack(side="left", padx=(8, 0))

        fenster.wait_window()
        return ergebnis["wert"]

    # ------------------------------------------------------------------
    # Dialekttexte als Datei
    # ------------------------------------------------------------------
    def _on_export_texts(self) -> None:
        """Schreibt alle sieben Dialekte als Textdatei in den Datenordner."""
        try:
            pfade = textfiles.write_all(self.state.config.dialect_overrides)
        except OSError as exc:
            show_error(self, self.theme, t("tab_store.files_not_written_title"),
                       t("tab_store.text_files_not_created_message"),
                       t("tab_store.technical_details_export", error=exc))
            return

        self.log.append(t("tab_store.dialect_files_written_log", count=len(pfade)), "ok")
        show_info(
            self, self.theme, t("tab_store.text_files_created_title"),
            t("tab_store.text_files_created_message", count=len(pfade),
              folder=textfiles.folder()),
            t("tab_store.text_files_created_hint"))

    def _on_open_text_folder(self) -> None:
        try:
            open_with_default_player(textfiles.folder())
        except Exception as exc:                       # noqa: BLE001
            show_error(self, self.theme, t("tab_store.folder_not_opened_title"),
                       str(exc), t("tab_store.folder_here_hint", folder=textfiles.folder()))

    def _on_import_texts(self) -> None:
        """Liest eine überarbeitete Textdatei ein."""
        pack = self._selected_dialect()
        vorschlag = textfiles.file_for(pack.key) if pack else None

        pfad = filedialog.askopenfilename(
            parent=self,
            title=t("tab_store.import_revised_texts_title"),
            initialdir=str(textfiles.folder()),
            initialfile=vorschlag.name if vorschlag else "",
            filetypes=[(t("tab_store.filetype_text_files"), "*.txt"),
                       (t("tab_store.filetype_all_files"), "*.*")])
        if not pfad:
            return

        pfad = Path(pfad)
        # Der Dialekt richtet sich nach dem Dateinamen, nicht nach der
        # Auswahl im Fenster - sonst landen kölsche Texte beim Bayerischen.
        ziel = next((p for p in self._all_packs() if p.key == pfad.stem), None)
        if ziel is None:
            show_warning(
                self, self.theme, t("tab_store.pack_not_recognized_title"),
                t("tab_store.pack_not_recognized_message", name=pfad.name),
                t("tab_store.pack_not_recognized_hint"))
            return

        try:
            ergebnis = textfiles.read_one(pfad, ziel)
        except (OSError, UnicodeError) as exc:
            show_error(self, self.theme, t("tab_store.file_not_readable_title"),
                       t("tab_store.file_not_readable_message", name=pfad.name),
                       t("tab_store.technical_details_import_texts", error=exc))
            return

        if not ergebnis.gelesen:
            show_warning(
                self, self.theme, t("tab_store.nothing_found_title"),
                t("tab_store.nothing_found_lines_message", name=pfad.name),
                t("tab_store.nothing_found_lines_hint"))
            return

        hinweise = []
        if ergebnis.unbekannt:
            zeige = ", ".join(str(i) for i in ergebnis.unbekannt[:8])
            if len(ergebnis.unbekannt) > 8:
                zeige += " ..."
            hinweise.append(
                t("tab_store.unknown_numbers_hint", count=len(ergebnis.unbekannt),
                  list=zeige))
        if ergebnis.leer:
            hinweise.append(
                t("tab_store.empty_lines_hint", count=ergebnis.leer))

        if not messagebox.askyesno(
                t("tab_store.apply_texts_title"),
                f"{pfad.name}\n\n{ergebnis.summary()}\n\n"
                + ("\n".join(hinweise) + "\n\n" if hinweise else "")
                + t("tab_store.apply_texts_question", name=ziel.name),
                parent=self):
            return

        alt = self.state.config.dialect_overrides(ziel.key)
        geaendert = dialect.changed_ids(ziel, ergebnis.overrides)
        # Nur das neu sprechen, was sich wirklich geändert hat.
        wirklich_neu = {i for i in geaendert
                        if alt.get(i, ziel.texts.get(i, "")) !=
                        ergebnis.overrides.get(i, ziel.texts.get(i, ""))}
        verworfen = dialect.forget_cached_audio(ziel, wirklich_neu)

        self.state.config.set_dialect_overrides(ziel.key, ergebnis.overrides)
        self.state.save()
        self._on_dialect_changed()

        self.log.append(
            t("tab_store.texts_taken_over_log", name=ziel.name,
              count=ergebnis.geaendert, filename=pfad.name), "ok")

        zusatz = ""
        if verworfen:
            zusatz = t("tab_store.discarded_recordings_note", count=verworfen)
        show_info(self, self.theme, t("tab_store.texts_applied_title"),
                  t("tab_store.texts_applied_message", count=ergebnis.geaendert,
                    total=ziel.count),
                  t("tab_store.changes_kept_note")
                  + zusatz)

    def _on_show_texts(self) -> None:
        """Öffnet den Texteditor für den gewählten Dialekt."""
        pack = self._selected_dialect()
        if pack is None:
            return

        basis = pack                      # mitgelieferte Texte
        aktuell = self._effective_dialect(pack)   # mit eigenen Änderungen

        window = tk.Toplevel(self)
        window.title(t("tab_store.edit_texts_window_title", name=pack.name, count=pack.count))
        window.configure(bg=self.theme.color("bg"))
        window.geometry("900x700")
        window.transient(self.winfo_toplevel())

        card = Card(window, self.theme, t("tab_store.customize_pack_title", name=pack.name),
                    t("tab_store.customize_pack_subtitle"))
        card.pack(fill="both", expand=True, padx=16, pady=16)

        suche_zeile = ttk.Frame(card.content, style="Card.TFrame")
        suche_zeile.pack(fill="x", pady=(0, 8))
        ttk.Label(suche_zeile, text=t("tab_store.search_label"), style="Surface.TLabel").pack(side="left")
        var_suche = tk.StringVar()
        eingabe = ttk.Entry(suche_zeile, textvariable=var_suche, width=30)
        eingabe.pack(side="left", padx=(8, 0))
        lbl_zahl = ttk.Label(suche_zeile, text="", style="Muted.TLabel")
        lbl_zahl.pack(side="left", padx=(14, 0))

        liste = ScrollableList(card.content, self.theme)
        liste.pack(fill="both", expand=True)

        felder: dict[int, tk.StringVar] = {}
        katalog = self.state.catalog

        def aufbauen() -> None:
            # Fast 600 Zeilen mit je vier Bausteinen brauchen gut zwei
            # Sekunden. Ohne Rückmeldung wirkt das wie ein Absturz.
            lbl_zahl.configure(text=t("tab_store.building_list_status"))
            window.configure(cursor="watch")
            window.update_idletasks()
            try:
                _aufbauen()
            finally:
                window.configure(cursor="")

        def _aufbauen() -> None:
            liste.clear()
            felder.clear()
            begriff = var_suche.get().strip().lower()
            gezeigt = 0

            for sound_id in sorted(basis.texts):
                text_jetzt = aktuell.texts.get(sound_id, "")
                eintrag = katalog.get(sound_id)
                bedeutung = eintrag.title if eintrag else ""

                if begriff and not (begriff in text_jetzt.lower()
                                    or begriff in bedeutung.lower()
                                    or begriff == str(sound_id)):
                    continue

                zeile = ttk.Frame(liste.inner, style="Card.TFrame")
                zeile.pack(fill="x", padx=4, pady=(0, 2))
                zeile.columnconfigure(1, weight=1)

                ttk.Label(zeile, text=str(sound_id), style="Mono.TLabel",
                          width=5, anchor="e").grid(row=0, column=0, rowspan=2,
                                                    sticky="ne", padx=(0, 8))
                var = tk.StringVar(value=text_jetzt)
                felder[sound_id] = var
                ttk.Entry(zeile, textvariable=var).grid(row=0, column=1, sticky="ew")

                # Sofort hören, wie der geänderte Satz klingt.
                ttk.Button(zeile, text="▶", width=3, style="Small.TButton",
                           command=lambda v=var: self._speak_text(v.get())
                           ).grid(row=0, column=2, sticky="e", padx=(6, 0))

                geaendert = text_jetzt != basis.texts.get(sound_id, "")
                hinweis = bedeutung + (t("tab_store.edited_marker") if geaendert else "")
                ttk.Label(zeile, text=hinweis, style="Muted.TLabel",
                          anchor="w").grid(row=1, column=1, sticky="ew",
                                           pady=(1, 4))
                gezeigt += 1

            liste.scroll_to_top()
            lbl_zahl.configure(text=t("tab_store.shown_count", shown=gezeigt, total=basis.count))

        eingabe.bind("<KeyRelease>", lambda _e: aufbauen())
        aufbauen()

        # ---- Knöpfe ------------------------------------------------------
        knoepfe = ttk.Frame(window, style="TFrame")
        knoepfe.pack(fill="x", padx=16, pady=(0, 16))

        def speichern() -> None:
            abweichungen = {}
            for sound_id, var in felder.items():
                wert = var.get().strip()
                if wert and wert != basis.texts.get(sound_id, ""):
                    abweichungen[sound_id] = wert

            # Änderungen außerhalb der aktuellen Suchansicht behalten
            alt = self.state.config.dialect_overrides(pack.key)
            for sound_id, wert in alt.items():
                if sound_id not in felder:
                    abweichungen[sound_id] = wert

            geaendert = dialect.changed_ids(basis, abweichungen)
            verworfen = dialect.forget_cached_audio(basis, geaendert)

            self.state.config.set_dialect_overrides(pack.key, abweichungen)
            self.state.save()
            window.destroy()

            self._on_dialect_changed()
            zusatz = ""
            if verworfen:
                zusatz = t("tab_store.discarded_recordings_note_own_text", count=verworfen)
            show_info(self, self.theme, t("tab_store.texts_saved_title"),
                      t("tab_store.texts_saved_message", count=len(geaendert),
                        total=basis.count),
                      t("tab_store.changes_kept_note")
                      + zusatz)

        def zuruecksetzen() -> None:
            if not messagebox.askyesno(
                    t("tab_store.reset_confirm_title"),
                    t("tab_store.reset_confirm_message", name=pack.name), parent=window):
                return
            alt = self.state.config.dialect_overrides(pack.key)
            dialect.forget_cached_audio(basis, dialect.changed_ids(basis, alt))
            self.state.config.set_dialect_overrides(pack.key, {})
            self.state.save()
            window.destroy()
            self._on_dialect_changed()

        ttk.Button(knoepfe, text=t("tab_store.save_button"), style="Accent.TButton",
                   command=speichern).pack(side="left")
        ttk.Button(knoepfe, text=t("tab_store.reset_to_default_button"),
                   command=zuruecksetzen).pack(side="left", padx=(8, 0))
        ttk.Button(knoepfe, text=t("tab_store.text_editor_cancel_button"),
                   command=window.destroy).pack(side="right")

    def _speak_text(self, text: str) -> None:
        """Spricht einen einzelnen Satz mit der gerade gewählten Stimme."""
        text = (text or "").strip()
        if not text:
            show_warning(self, self.theme, t("tab_store.no_text_title"),
                         t("tab_store.no_text_message"))
            return

        engine = self.var_engine.get()
        api_key = voice_id = win_voice = ""
        modell, klang, eigene = self._eleven_klang()
        tempo, hoehe = self._win_klang()

        if engine == dialect.ENGINE_ELEVENLABS:
            api_key = self.var_key.get().strip() or self.state.config.elevenlabs_key
            gewaehlt = self._selected_eleven_voice()
            if not api_key or gewaehlt is None:
                show_warning(
                    self, self.theme, t("tab_store.connect_first_title"),
                    t("tab_store.connect_first_message"),
                    t("tab_store.connect_first_hint"))
                return
            voice_id = gewaehlt.voice_id
        else:
            if not tts.german_voices():
                show_warning(self, self.theme, t("tab_store.no_german_voice_title"),
                             t("tab_store.no_german_voice_message"))
                return
            win_voice = self._selected_win_voice()

        ordner = build_dir() / "_satzprobe"

        def work(_task):
            return dialect.speak_one(
                text, ordner, engine=engine, voice=win_voice,
                api_key=api_key, voice_id=voice_id, model=modell,
                voice_settings=klang, use_voice_settings=eigene,
                rate=tempo, pitch=hoehe)

        def ok(pfad) -> None:
            try:
                open_with_default_player(pfad)
            except OSError as exc:
                show_error(self, self.theme, t("tab_store.playback_not_possible_title"),
                           t("tab_store.recording_here_hint", path=pfad), str(exc))

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            show_error(self, self.theme, t("tab_store.reading_aloud_failed_title"), message, hint)

        run_async(self, work, on_success=ok, on_error=fail)

    def _on_generate_selected(self) -> None:
        # Bewusst die wirksamen Texte: was der Nutzer geändert hat, wird
        # auch gesprochen.
        pack = self._effective_dialect()
        if pack is not None:
            self.generate_dialect(pack)

    # ------------------------------------------------------------------
    def _on_preview_dialect(self) -> None:
        """Spricht drei Sätze und spielt sie ab."""
        pack = self._effective_dialect()
        if pack is None:
            return

        engine = self.var_engine.get()
        api_key = ""
        voice_id = ""
        win_voice = ""

        if engine == dialect.ENGINE_ELEVENLABS:
            api_key = self.var_key.get().strip() or self.state.config.elevenlabs_key
            chosen = self._selected_eleven_voice()
            if not api_key or chosen is None:
                messagebox.showinfo(
                    t("tab_store.connect_first_title"),
                    t("tab_store.connect_first_preview_message"), parent=self)
                return
            voice_id = chosen.voice_id
        else:
            if not tts.german_voices():
                messagebox.showwarning(
                    t("tab_store.no_german_voice_title"),
                    t("tab_store.no_german_voice_message"),
                    parent=self)
                return
            win_voice = self._selected_win_voice()

        tempo_vor, hoehe_vor = self._win_klang()
        modell_vor, klang_vor, eigen_vor = self._eleven_klang()
        stempel = hashlib.md5(
            f"{win_voice}|{voice_id}|{modell_vor}|{eigen_vor}|"
            f"{sorted((klang_vor or {}).items())}|{tempo_vor}|{hoehe_vor}"
            .encode("utf-8")).hexdigest()[:8]
        work = build_dir() / "_kostprobe" / f"{pack.key}_{engine}_{stempel}"

        self._busy(True)
        self.badge.set(t("tab_store.speaking_sample_badge"), "muted")
        self.log.clear()
        for line in dialect.preview_texts(pack, 3):
            self.log.append(line, "info")

        modell, klang, eigene = self._eleven_klang()
        tempo, hoehe = self._win_klang()

        def work_fn(_task):
            return dialect.preview(
                pack, work, engine=engine, voice=win_voice,
                api_key=api_key, voice_id=voice_id,
                model=modell, voice_settings=klang,
                use_voice_settings=eigene,
                rate=tempo, pitch=hoehe, ffmpeg=self.state.ffmpeg,
                log=lambda m: self._log(m))

        def ok(files) -> None:
            self.badge.set(t("tab_store.sample_ready_badge", count=len(files)), "ok")
            self.log.append(t("tab_store.playing_log"), "ok")
            for path in files:
                try:
                    open_with_default_player(path)
                except OSError as exc:
                    self.log.append(t("tab_store.couldnt_play_log", filename=path.name,
                                      error=exc),
                                    "warn")
                    break

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            self.badge.set(t("tab_store.sample_failed_badge"), "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, t("tab_store.sample_failed_title"),
                       message + (f"\n\n{hint}" if hint else ""))

        run_async(self, work_fn, on_success=ok, on_error=fail,
                  on_finally=lambda: self._busy(False))

    # ------------------------------------------------------------------
    def _build_engine_chooser(self, parent) -> None:
        """Auswahl, wer die Ansagen spricht."""
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=(14, 0))

        ttk.Frame(frame, style="Separator.TFrame", height=1).pack(fill="x",
                                                                   pady=(0, 12))
        ttk.Label(frame, text=t("tab_store.who_speaks_heading"), style="Heading.TLabel").pack(anchor="w")

        self.var_engine = tk.StringVar(value=self.state.config["tts_engine"])

        # --- Windows ---------------------------------------------------
        win_row = ttk.Frame(frame, style="Card.TFrame")
        win_row.pack(fill="x", pady=(8, 0))
        ttk.Radiobutton(win_row, text=t("tab_store.windows_tts_radio"),
                        variable=self.var_engine, value=dialect.ENGINE_WINDOWS,
                        command=self._on_engine_changed).pack(side="left")
        self.combo_winvoice = ttk.Combobox(win_row, state="readonly", width=30,
                                           values=[])
        self.combo_winvoice.pack(side="left", padx=(12, 0))

        self.lbl_voice = ttk.Label(
            frame,
            text=t("tab_store.windows_voice_info"),
            style="Muted.TLabel", wraplength=800, justify="left")
        self.lbl_voice.pack(anchor="w", pady=(2, 0))

        # --- Regler für die Windows-Stimme --------------------------------
        self.win_regler = ttk.Frame(frame, style="Card.TFrame")
        ttk.Label(self.win_regler, text=t("tab_store.rate_label"),
                  style="Surface.TLabel").pack(side="left")
        self.var_rate = tk.IntVar(value=int(self.state.config["tts_rate"]))
        ttk.Scale(self.win_regler, from_=-6, to=6, orient="horizontal",
                  variable=self.var_rate, length=150,
                  command=lambda _v: self._on_win_regler()).pack(side="left",
                                                                 padx=(8, 8))
        self.lbl_rate = ttk.Label(self.win_regler, text="", style="Muted.TLabel")
        self.lbl_rate.pack(side="left")

        ttk.Label(self.win_regler, text=t("tab_store.pitch_label"),
                  style="Surface.TLabel").pack(side="left", padx=(16, 0))
        self.var_pitch = tk.IntVar(value=int(self.state.config["tts_pitch"]))
        ttk.Scale(self.win_regler, from_=-6, to=6, orient="horizontal",
                  variable=self.var_pitch, length=150,
                  command=lambda _v: self._on_win_regler()).pack(side="left",
                                                                 padx=(8, 8))
        self.lbl_pitch = ttk.Label(self.win_regler, text="", style="Muted.TLabel")
        self.lbl_pitch.pack(side="left")

        ttk.Button(self.win_regler, text=t("tab_store.reset_button"), style="Small.TButton",
                   command=self._on_win_reset).pack(side="left", padx=(16, 0))

        # --- ElevenLabs -------------------------------------------------
        el_row = ttk.Frame(frame, style="Card.TFrame")
        el_row.pack(fill="x", pady=(12, 0))
        ttk.Radiobutton(el_row, text=t("tab_store.elevenlabs_radio"),
                        variable=self.var_engine, value=dialect.ENGINE_ELEVENLABS,
                        command=self._on_engine_changed).pack(side="left")

        bedarf = min((elevenlabs.estimate_characters(p.texts)
                      for p in dialect.DIALECTS), default=0)
        self.lbl_eleven_info = ttk.Label(
            frame,
            text=t("tab_store.elevenlabs_info", needed=bedarf),
            style="Muted.TLabel", wraplength=800, justify="left")
        self.lbl_eleven_info.pack(anchor="w", pady=(2, 0))

        key_row = ttk.Frame(frame, style="Card.TFrame")
        key_row.pack(fill="x", pady=(8, 0))
        ttk.Label(key_row, text=t("tab_store.access_key_label"), style="Surface.TLabel").pack(
            side="left")
        self.var_key = tk.StringVar(value=self.state.config.elevenlabs_key)
        self.entry_key = ttk.Entry(key_row, textvariable=self.var_key, width=34,
                                   show="•")
        self.entry_key.pack(side="left", padx=(8, 8))
        self.btn_connect = ttk.Button(key_row, text=t("tab_store.connect_load_voices_button"),
                                      style="Small.TButton",
                                      command=self._on_connect_elevenlabs)
        self.btn_connect.pack(side="left")
        ttk.Button(key_row, text=t("tab_store.get_key_button"), style="Link.TButton",
                   command=self._open_api_key_page).pack(side="left", padx=(8, 0))
        ttk.Button(key_row, text=t("tab_store.forget_key_button"), style="Link.TButton",
                   command=self._on_forget_key).pack(side="left", padx=(8, 0))

        self.lbl_key_ort = ttk.Label(frame, text="", style="Muted.TLabel",
                                     wraplength=800, justify="left")
        self.lbl_key_ort.pack(anchor="w", pady=(2, 0))

        voice_row = ttk.Frame(frame, style="Card.TFrame")
        voice_row.pack(fill="x", pady=(8, 0))
        ttk.Label(voice_row, text=t("tab_store.voice_label"), style="Surface.TLabel").pack(side="left")
        self.combo_elvoice = ttk.Combobox(voice_row, state="readonly", width=44,
                                          values=[])
        self.combo_elvoice.pack(side="left", padx=(8, 8))
        self.combo_elvoice.bind(
            "<<ComboboxSelected>>", lambda _e: self._on_elvoice_changed())
        self.btn_search = ttk.Button(voice_row, text=t("tab_store.search_voice_library_button"),
                                     style="Small.TButton",
                                     command=self._on_search_bavarian)
        self.btn_search.pack(side="left")

        # Eigene Stimmen tauchen nicht immer in der Liste auf. Mit der ID
        # lässt sich jede Stimme direkt ansprechen.
        id_row = ttk.Frame(frame, style="Card.TFrame")
        id_row.pack(fill="x", pady=(8, 0))
        ttk.Label(id_row, text=t("tab_store.custom_voice_id_label"),
                  style="Surface.TLabel").pack(side="left")
        self.var_voice_id = tk.StringVar(
            value=self.state.config["elevenlabs_voice_id"])
        self.entry_voice_id = ttk.Entry(id_row, textvariable=self.var_voice_id,
                                        width=28)
        self.entry_voice_id.pack(side="left", padx=(8, 8))
        self.btn_add_id = ttk.Button(id_row, text=t("tab_store.add_id_apply_button"),
                                     style="Small.TButton",
                                     command=self._on_add_voice_id)
        self.btn_add_id.pack(side="left")
        ttk.Label(id_row,
                  text=t("tab_store.copy_voice_id_hint"),
                  style="Muted.TLabel").pack(side="left", padx=(10, 0))

        # --- Klang -------------------------------------------------------
        klang = ttk.Frame(frame, style="Card.TFrame")
        klang.pack(fill="x", pady=(8, 0))
        ttk.Label(klang, text=t("tab_store.model_label"), style="Surface.TLabel").pack(side="left")
        self.combo_model = ttk.Combobox(klang, state="readonly", width=34,
                                        values=[])
        self.combo_model.pack(side="left", padx=(8, 16))
        self.combo_model.set(t("tab_store.default_model_label", model="eleven_multilingual_v2"))

        self.var_own_settings = tk.BooleanVar(
            value=bool(self.state.config["elevenlabs_use_voice_settings"]))
        ttk.Checkbutton(klang, text=t("tab_store.use_voice_settings_checkbox"),
                        variable=self.var_own_settings,
                        command=self._on_settings_mode).pack(side="left")

        self.regler = ttk.Frame(frame, style="Card.TFrame")
        ttk.Label(self.regler, text=t("tab_store.liveliness_label"),
                  style="Surface.TLabel").pack(side="left")
        self.var_stability = tk.DoubleVar(
            value=float(self.state.config["elevenlabs_stability"]))
        ttk.Scale(self.regler, from_=0.0, to=1.0, orient="horizontal",
                  variable=self.var_stability, length=150,
                  command=lambda _v: self._on_regler()).pack(side="left", padx=(8, 8))
        self.lbl_stability = ttk.Label(self.regler, text="", style="Muted.TLabel")
        self.lbl_stability.pack(side="left")

        ttk.Label(self.regler, text=t("tab_store.expression_label"),
                  style="Surface.TLabel").pack(side="left", padx=(16, 0))
        self.var_style = tk.DoubleVar(
            value=float(self.state.config["elevenlabs_style"]))
        ttk.Scale(self.regler, from_=0.0, to=1.0, orient="horizontal",
                  variable=self.var_style, length=150,
                  command=lambda _v: self._on_regler()).pack(side="left", padx=(8, 8))
        self.lbl_style = ttk.Label(self.regler, text="", style="Muted.TLabel")
        self.lbl_style.pack(side="left")

        ttk.Label(
            frame,
            text=t("tab_store.voice_settings_info"),
            style="Muted.TLabel", wraplength=800, justify="left").pack(
            anchor="w", pady=(4, 0))

        self.lbl_eleven = ttk.Label(frame, text="", style="Muted.TLabel",
                                    wraplength=800, justify="left")
        self.lbl_eleven.pack(anchor="w", pady=(6, 0))

        self._on_settings_mode()
        self._on_regler()
        self._on_win_regler()
        self._refresh_key_location()

        self._eleven_voices: list = []
        #: Die Windows-Stimmen aufzuzählen kostet einen
        #: PowerShell-Aufruf - gemessen rund 0,4 Sekunden, und zwar
        #: blockierend. Beim Start wird das nicht gebraucht: Wer nie
        #: auf diese Seite geht, braucht die Liste nie. Sie entsteht
        #: deshalb beim ersten Öffnen.
        self._stimmen_geladen = False
        self._on_engine_changed()

    def beim_zeigen(self) -> None:
        """Wird aufgerufen, wenn die Seite zum ersten Mal sichtbar wird."""
        if not self._stimmen_geladen:
            self._stimmen_geladen = True
            self._refresh_voice_info()

    def _on_win_regler(self) -> None:
        """Beschriftet die Regler der Windows-Stimme."""
        tempo = self.var_rate.get()
        hoehe = self.var_pitch.get()
        rate_word = ("normal" if tempo == 0 else
                     t("tab_store.rate_slower") if tempo < 0 else
                     t("tab_store.rate_faster"))
        pitch_word = ("normal" if hoehe == 0 else
                      t("tab_store.pitch_lower") if hoehe < 0 else
                      t("tab_store.pitch_higher"))
        self.lbl_rate.configure(text=f"{tempo * 10:+d} %  ({rate_word})")
        self.lbl_pitch.configure(text=f"{hoehe * 10:+d} %  ({pitch_word})")
        self.state.config["tts_rate"] = int(tempo)
        self.state.config["tts_pitch"] = int(hoehe)

    def _on_win_reset(self) -> None:
        self.var_rate.set(0)
        self.var_pitch.set(0)
        self._on_win_regler()

    def _win_klang(self) -> tuple:
        return int(self.var_rate.get()), int(self.var_pitch.get())

    def _on_settings_mode(self) -> None:
        """Regler nur zeigen, wenn nicht die Stimmen-Einstellungen gelten."""
        eigene = self.var_own_settings.get()
        self.state.config["elevenlabs_use_voice_settings"] = eigene
        if eigene:
            self.regler.pack_forget()
        else:
            self.regler.pack(fill="x", pady=(6, 0))

    def _on_regler(self) -> None:
        stab = self.var_stability.get()
        art = (t("tab_store.liveliness_very_lively") if stab < 0.3 else
               t("tab_store.liveliness_lively") if stab < 0.5 else
               t("tab_store.liveliness_balanced") if stab < 0.7 else
               t("tab_store.liveliness_uniform"))
        self.lbl_stability.configure(text=f"{stab:.2f}  ({art})")
        self.lbl_style.configure(text=f"{self.var_style.get():.2f}")

    def _eleven_klang(self):
        """Was an ElevenLabs geschickt wird: (Modell, Einstellungen, Modus)."""
        modell = ""
        gewaehlt = self.combo_model.get()
        for eintrag in getattr(self, "_models", []):
            if eintrag["label"] == gewaehlt:
                modell = eintrag["id"]
                break

        if self.var_own_settings.get():
            return modell, None, True
        return modell, {"stability": round(self.var_stability.get(), 2),
                        "similarity_boost": 0.75,
                        "style": round(self.var_style.get(), 2),
                        "use_speaker_boost": True}, False

    def _on_engine_changed(self) -> None:
        engine = self.var_engine.get()
        self.state.config["tts_engine"] = engine
        self.state.save()

        eleven = engine == dialect.ENGINE_ELEVENLABS
        for widget in (self.entry_key, self.btn_connect, self.combo_elvoice,
                       self.btn_search, self.entry_voice_id, self.btn_add_id,
                       self.combo_model):
            widget.configure(state="normal" if eleven else "disabled")
        if eleven:
            self.combo_elvoice.configure(state="readonly")
            self.combo_model.configure(state="readonly")
        self.combo_winvoice.configure(state="disabled" if eleven else "readonly")
        self.refresh_progress()

        # Die Regler der Windows-Stimme nur zeigen, wenn sie auch spricht.
        if eleven:
            self.win_regler.pack_forget()
        else:
            self.win_regler.pack(fill="x", pady=(6, 0),
                                 before=self.lbl_voice)

    def _refresh_voice_info(self) -> None:
        self._win_voices = tts.german_voices()
        if self._win_voices:
            labels = [v.label for v in self._win_voices]
            self.combo_winvoice.configure(values=labels)
            stored = self.state.config["tts_voice"]
            chosen = next((v for v in self._win_voices if v.name == stored), None)
            self.combo_winvoice.set((chosen or self._win_voices[0]).label)
        else:
            self.combo_winvoice.configure(values=[])
            self.lbl_voice.configure(
                text=t("tab_store.no_german_voice_full_message"),
                style="Warning.TLabel")

        # Dasselbe für die ElevenLabs-Stimme: Solange keine Verbindung
        # steht, ist die Liste leer - der zuletzt benutzte Name soll
        # trotzdem dastehen, sonst wirkt die Auswahl vergessen.
        #
        # Diese drei Zeilen standen bis hierher hinter dem `return` von
        # _selected_win_voice und liefen deshalb nie.
        if self.state.config["elevenlabs_voice_name"]:
            self.combo_elvoice.configure(
                values=[self.state.config["elevenlabs_voice_name"]])
            self.combo_elvoice.set(self.state.config["elevenlabs_voice_name"])

    def _selected_win_voice(self) -> str:
        """Name der gewählten Windows-Stimme (leer = automatisch)."""
        label = self.combo_winvoice.get()
        voice = next((v for v in getattr(self, "_win_voices", [])
                      if v.label == label), None)
        return voice.name if voice else ""

    # ------------------------------------------------------------------
    def _refresh_key_location(self) -> None:
        """Zeigt, wo der Zugangsschlüssel abgelegt ist."""
        code = self.state.config.elevenlabs_key_location_code
        if code == Config.LOCATION_CREDENTIAL_MANAGER:
            text = t("tab_store.key_location_credential_manager")
            stil = "Success.TLabel"
        elif code == Config.LOCATION_CONFIG_ENCRYPTED:
            text = t("tab_store.key_location_config_json")
            stil = "Muted.TLabel"
        else:
            text = t("tab_store.key_location_none")
            stil = "Muted.TLabel"
        self.lbl_key_ort.configure(text=text, style=stil)

    def _on_forget_key(self) -> None:
        if not messagebox.askyesno(
                t("tab_store.forget_key_confirm_title"),
                t("tab_store.forget_key_confirm_message"), parent=self):
            return
        self.state.config.forget_elevenlabs_key()
        self.state.save()
        self.var_key.set("")
        self._refresh_key_location()
        self.lbl_eleven.configure(text=t("tab_store.key_removed_status"),
                                  style="Muted.TLabel")

    def _open_api_key_page(self) -> None:
        messagebox.showinfo(
            t("tab_store.get_access_key_title"),
            t("tab_store.get_access_key_message"),
            parent=self)
        webbrowser.open(elevenlabs.API_KEY_URL)

    def _on_connect_elevenlabs(self) -> None:
        key = self.var_key.get().strip()
        if not key:
            show_warning(
                self, self.theme, t("tab_store.access_key_missing_title"),
                t("tab_store.access_key_missing_connect_message"),
                t("tab_store.access_key_missing_connect_hint"))
            return

        if not elevenlabs.looks_like_key(key):
            show_warning(
                self, self.theme, t("tab_store.key_unusual_title"),
                t("tab_store.key_unusual_connect_message"),
                t("tab_store.key_unusual_connect_hint", count=len(key), prefix=key[:6]))

        self.btn_connect.configure(state="disabled")
        self.lbl_eleven.configure(text=t("tab_store.connecting_status"), style="Muted.TLabel")

        def work(_task):
            quota = elevenlabs.check_key(key)
            voices = elevenlabs.list_voices(key)
            models = elevenlabs.list_models(key)
            return quota, voices, models

        def ok(result):
            quota, voices, models = result
            self.state.config.set_elevenlabs_key(key)
            self.state.save()
            self._set_eleven_voices(voices)
            self._set_models(models)
            self._refresh_key_location()

            # Das GEWAEHLTE Paket, nicht das erste in der Liste. Früher
            # stand hier DIALECTS[0] - wer Wienerisch erzeugte, las
            # trotzdem "Für das bayerische Paket". Und mit
            # _effective_dialect zählen die eigenen Textänderungen
            # mit, die Zahl stimmt also auch dann noch.
            gewaehlt = self._effective_dialect()
            needed = (elevenlabs.estimate_characters(gewaehlt.texts)
                      if gewaehlt else 0)
            wofuer = (t("tab_store.quota_for_pack", name=gewaehlt.name) if gewaehlt
                      else t("tab_store.quota_for_generic_pack"))
            enough = quota.left >= needed
            self.lbl_eleven.configure(
                text=t("tab_store.quota_connected_status", quota=quota.describe(),
                       target=wofuer, needed=needed,
                       enough=(t("tab_store.quota_enough") if enough
                               else t("tab_store.quota_not_enough"))),
                style="Success.TLabel" if enough else "Warning.TLabel")

            eigene = [v for v in voices if v.is_own_creation]
            bavarian = [v for v in voices if v.is_bavarian]
            zusatz = t("tab_store.voices_in_account", count=len(voices))
            if eigene:
                zusatz += t("tab_store.voices_self_created", count=len(eigene))
            elif not bavarian:
                zusatz += t("tab_store.no_bavarian_in_library")
            self.lbl_eleven.configure(text=self.lbl_eleven.cget("text") + zusatz)

        def fail(exc):
            message, hint = error_text(exc)
            self.lbl_eleven.configure(text=f"   {message} {hint}".strip(),
                                      style="Danger.TLabel")

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_connect.configure(state="normal"))

    def _set_eleven_voices(self, voices, bevorzugt: str = "") -> None:
        """Füllt die Stimmenliste. Selbst erzeugte und bayerische zuerst."""
        self._eleven_voices = sorted(
            voices,
            key=lambda v: (not v.is_own_creation, not v.is_bavarian, v.name.lower()))
        self.combo_elvoice.configure(
            values=[v.label for v in self._eleven_voices])

        stored = bevorzugt or self.state.config["elevenlabs_voice_id"]
        chosen = next((v for v in self._eleven_voices if v.voice_id == stored), None)
        if chosen is None:
            chosen = next((v for v in self._eleven_voices if v.is_own_creation), None)
        if chosen is None:
            chosen = next((v for v in self._eleven_voices if v.is_bavarian), None)
        if chosen is None and self._eleven_voices:
            chosen = self._eleven_voices[0]
        if chosen is not None:
            self.combo_elvoice.set(chosen.label)
            self.var_voice_id.set(chosen.voice_id)

    def _set_models(self, models) -> None:
        """Füllt die Modellauswahl. Ein neueres Modell klingt oft lebendiger."""
        self._models = [{"id": m["id"], "label": f"{m['name']} ({m['id']})"}
                        for m in models]
        if not self._models:
            self._models = [{"id": elevenlabs.MODEL,
                             "label": t("tab_store.default_model_label", model=elevenlabs.MODEL)}]

        self.combo_model.configure(values=[m["label"] for m in self._models])
        gespeichert = self.state.config["elevenlabs_model"] or elevenlabs.MODEL
        treffer = next((m for m in self._models if m["id"] == gespeichert), None)
        self.combo_model.set((treffer or self._models[0])["label"])

    def _selected_eleven_voice(self):
        label = self.combo_elvoice.get()
        return next((v for v in self._eleven_voices if v.label == label), None)

    def _on_elvoice_changed(self) -> None:
        """Hält das ID-Feld mit der Auswahl im Gleichklang."""
        voice = self._selected_eleven_voice()
        if voice is not None:
            self.var_voice_id.set(voice.voice_id)

    def _on_add_voice_id(self) -> None:
        """Übernimmt eine Stimme direkt über ihre ID."""
        key = self.var_key.get().strip() or self.state.config.elevenlabs_key
        voice_id = self.var_voice_id.get().strip()

        if not key:
            show_warning(self, self.theme, t("tab_store.access_key_missing_title"),
                         t("tab_store.access_key_missing_add_id_message"))
            return
        if not voice_id:
            show_warning(
                self, self.theme, t("tab_store.no_id_entered_title"),
                t("tab_store.no_id_entered_message"),
                t("tab_store.no_id_entered_hint"))
            return

        # Vertauschte Felder sind der häufigste Stolperstein - lieber vorher
        # erkennen als eine unverständliche Serverantwort zeigen.
        if voice_id.startswith("sk_"):
            show_warning(
                self, self.theme, t("tab_store.fields_swapped_title"),
                t("tab_store.fields_swapped_message"),
                t("tab_store.fields_swapped_hint"))
            return
        if not elevenlabs.looks_like_key(key):
            show_warning(
                self, self.theme, t("tab_store.key_unusual_title"),
                t("tab_store.key_unusual_addid_message"),
                t("tab_store.key_unusual_addid_hint", count=len(key), prefix=key[:6]))
            return

        self.btn_add_id.configure(state="disabled")
        self.lbl_eleven.configure(text=t("tab_store.fetching_voice_status"), style="Muted.TLabel")

        def work(_task):
            voice = elevenlabs.get_voice(key, voice_id)
            alle = elevenlabs.list_voices(key)
            return voice, alle

        def ok(result):
            voice, alle = result
            # Die geholte Stimme nach vorne, Doppelte vermeiden.
            rest = [v for v in alle if v.voice_id != voice.voice_id]
            self._set_eleven_voices([voice] + rest, bevorzugt=voice.voice_id)

            self.state.config.set_elevenlabs_key(key)
            self.state.config["elevenlabs_voice_id"] = voice.voice_id
            self.state.config["elevenlabs_voice_name"] = voice.label
            self.state.save()

            self.lbl_eleven.configure(
                text=t("tab_store.voice_selected_status", name=voice.name),
                style="Success.TLabel")

        def fail(exc):
            message, hint = error_text(exc)
            self.lbl_eleven.configure(text=f"   {message} {hint}".strip(),
                                      style="Danger.TLabel")
            show_error(self, self.theme, t("tab_store.voice_not_found_title"),
                       message + (f"\n\n{hint}" if hint else ""))

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_add_id.configure(state="normal"))

    # ------------------------------------------------------------------
    def _on_search_bavarian(self) -> None:
        key = self.var_key.get().strip() or self.state.config.elevenlabs_key
        if not key:
            messagebox.showinfo(t("tab_store.access_key_missing_title"),
                                t("tab_store.access_key_missing_search_message"),
                                parent=self)
            return

        self.btn_search.configure(state="disabled")
        self.lbl_eleven.configure(text=t("tab_store.searching_library_status"),
                                  style="Muted.TLabel")

        def work(_task):
            return elevenlabs.search_bavarian_voices(key)

        def ok(found):
            if not found:
                self.lbl_eleven.configure(
                    text=t("tab_store.no_bavarian_found_status"),
                    style="Warning.TLabel")
                webbrowser.open(elevenlabs.LIBRARY_URL)
                return
            self._show_voice_chooser(key, found)

        def fail(exc):
            message, hint = error_text(exc)
            self.lbl_eleven.configure(text=f"   {message} {hint}".strip(),
                                      style="Danger.TLabel")

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_search.configure(state="normal"))

    def _show_voice_chooser(self, key: str, found: list) -> None:
        """Lässt den Nutzer auswählen, welche Stimme übernommen wird."""
        window = tk.Toplevel(self)
        window.title(t("tab_store.choose_voice_window_title"))
        window.configure(bg=self.theme.color("bg"))
        window.geometry("760x560")
        window.transient(self)
        window.grab_set()

        card = Card(window, self.theme, t("tab_store.voices_found_title", count=len(found)),
                    t("tab_store.voices_found_subtitle"))
        card.pack(fill="both", expand=True, padx=16, pady=16)

        liste = ScrollableList(card.content, self.theme)
        liste.pack(fill="both", expand=True)

        gewaehlt = tk.StringVar(value=found[0].voice_id)
        for voice in found:
            block = ttk.Frame(liste.inner, style="Card.TFrame")
            block.pack(fill="x", padx=4, pady=(0, 6))
            ttk.Radiobutton(block, text=voice.details, variable=gewaehlt,
                            value=voice.voice_id).pack(anchor="w")
            if voice.preview_url:
                ttk.Button(
                    block, text=t("tab_store.listen_on_elevenlabs_button"), style="Link.TButton",
                    command=lambda u=voice.preview_url: webbrowser.open(u)
                ).pack(anchor="w", padx=(24, 0))
            ttk.Frame(block, style="Separator.TFrame", height=1).pack(
                fill="x", pady=(6, 0))

        buttons = ttk.Frame(window, style="TFrame")
        buttons.pack(fill="x", padx=16, pady=(0, 16))

        def uebernehmen() -> None:
            voice = next((v for v in found if v.voice_id == gewaehlt.get()), None)
            window.destroy()
            if voice is not None:
                self._add_voice(key, voice)

        ttk.Button(buttons, text=t("tab_store.add_selected_voice_button"),
                   style="Accent.TButton", command=uebernehmen).pack(side="left")
        ttk.Button(buttons, text=t("tab_store.voice_chooser_cancel_button"),
                   command=window.destroy).pack(side="left", padx=(8, 0))
        ttk.Label(buttons,
                  text=t("tab_store.none_fit_hint"),
                  style="MutedBg.TLabel", wraplength=380,
                  justify="left").pack(side="left", padx=(16, 0))

    def _add_voice(self, key: str, voice) -> None:
        def work(_task):
            elevenlabs.add_shared_voice(key, voice)
            return elevenlabs.list_voices(key)

        def ok(voices):
            self._set_eleven_voices(voices)
            self.lbl_eleven.configure(
                text=t("tab_store.voice_added_status", name=voice.name),
                style="Success.TLabel")

        def fail(exc):
            message, hint = error_text(exc)
            self.lbl_eleven.configure(text=f"   {message} {hint}".strip(),
                                      style="Danger.TLabel")

        run_async(self, work, on_success=ok, on_error=fail)

    # ------------------------------------------------------------------
    def generate_dialect(self, pack) -> None:
        """Spricht ein Dialektpaket und baut es auf das Originalpaket."""
        if not self.state.has_base_pack:
            messagebox.showwarning(
                t("tab_store.original_pack_missing_title"),
                t("tab_store.original_pack_missing_generate_message"),
                parent=self)
            return

        engine = self.var_engine.get()
        api_key = ""
        voice_id = ""
        win_voice = ""

        if engine == dialect.ENGINE_ELEVENLABS:
            api_key = self.var_key.get().strip() or self.state.config.elevenlabs_key
            chosen = self._selected_eleven_voice()
            if not api_key:
                messagebox.showwarning(
                    t("tab_store.access_key_missing_title"),
                    t("tab_store.access_key_missing_generate_message"), parent=self)
                return
            if chosen is None:
                messagebox.showwarning(
                    t("tab_store.no_voice_chosen_title"),
                    t("tab_store.no_voice_chosen_message"), parent=self)
                return
            voice_id = chosen.voice_id
            # Bei selbst erzeugten Stimmen sagen die Merkmale nichts über den
            # Dialekt aus - da weiß der Nutzer besser Bescheid als die Labels.
            if (not chosen.is_bavarian and not chosen.is_own_creation
                    and not messagebox.askyesno(
                        t("tab_store.no_bavarian_voice_title"),
                        t("tab_store.no_bavarian_voice_message", name=chosen.name),
                        parent=self)):
                return
        else:
            if not tts.german_voices():
                messagebox.showwarning(
                    t("tab_store.no_german_voice_title"),
                    t("tab_store.no_german_voice_generate_message"),
                    parent=self)
                return
            win_voice = self._selected_win_voice()

        if not self.state.ffmpeg:
            messagebox.showwarning(
                t("tab_store.ffmpeg_missing_title"),
                t("tab_store.ffmpeg_missing_message"),
                parent=self)
            return

        # Der Ablageort enthält Stimme, Dienst und Klangeinstellung. Sonst
        # würde nach einem Wechsel das alte Audio wiederverwendet - und beim
        # Fortsetzen nach aufgebrauchtem Kontingent landeten zwei
        # verschiedene Klangbilder im selben Paket.
        # Muss vor der Rückfrage stehen: dort wird schon gezeigt, wie weit
        # ein früherer Lauf gekommen ist.
        tempo, hoehe = self._win_klang()
        work = self._work_dir(pack)

        schon_da = dialect.spoken_count(work)
        offen = dialect.remaining_texts(pack, work)

        if engine == dialect.ENGINE_ELEVENLABS:
            chars = elevenlabs.estimate_characters(offen)

            # Kontingent abfragen, damit vorher klar ist, wie weit es reicht.
            rest = None
            try:
                rest = elevenlabs.check_key(api_key).left
            except Exception:
                pass

            question = t("tab_store.question_already_spoken", done=schon_da,
                         total=pack.count, remaining=len(offen), chars=chars)

            if rest is not None:
                question += t("tab_store.question_quota_free", rest=rest)
                if rest < chars:
                    passt = 0
                    verbraucht = 0
                    for _i, t_text in sorted(offen.items()):
                        if verbraucht + len(t_text) > rest:
                            break
                        verbraucht += len(t_text)
                        passt += 1
                    question += t("tab_store.question_not_enough", doable=passt,
                                  remaining=len(offen))
                else:
                    question += t("tab_store.question_enough_for_all")

            question += t("tab_store.question_privacy_continue")
        else:
            question = t("tab_store.question_windows_intro", count=len(offen),
                         name=pack.name)
            if schon_da:
                question += t("tab_store.question_already_spoken_skipped", count=schon_da)
            question += t("tab_store.question_windows_local_continue")

        if not messagebox.askyesno(t("tab_store.generate_confirm_title", name=pack.name),
                                   question, parent=self):
            return

        # ---- Name des Pakets -------------------------------------------
        # Wichtig: jede Stimme bekommt ihre eigene Datei. Sonst überschreibt
        # ein Testlauf mit einer Windows-Stimme das Paket, das vorher mit
        # bezahltem ElevenLabs-Kontingent entstanden ist.
        if engine == dialect.ENGINE_ELEVENLABS:
            stimmen_label = (self._selected_eleven_voice().name
                             if self._selected_eleven_voice() else "")
        else:
            stimmen_label = win_voice
        vorschlag = library.suggest_name(pack.name, engine, stimmen_label)

        gewuenscht = simpledialog.askstring(
            t("tab_store.name_for_pack_generate_title"),
            t("tab_store.name_for_pack_generate_prompt"),
            initialvalue=vorschlag, parent=self)
        if gewuenscht is None:
            return
        dateiname = library.safe_name(gewuenscht) or vorschlag
        ziel_pfad = library.unique_path(build_dir(), dateiname)
        out_name = ziel_pfad.name

        # Auswahl merken
        self.state.config["tts_engine"] = engine
        self.state.config["tts_voice"] = win_voice
        if engine == dialect.ENGINE_ELEVENLABS:
            self.state.config.set_elevenlabs_key(api_key)
            self.state.config["elevenlabs_voice_id"] = voice_id
            chosen = self._selected_eleven_voice()
            self.state.config["elevenlabs_voice_name"] = chosen.label if chosen else ""
            modell_speichern, _, _ = self._eleven_klang()
            self.state.config["elevenlabs_model"] = modell_speichern
            self.state.config["elevenlabs_use_voice_settings"] = \
                self.var_own_settings.get()
            self.state.config["elevenlabs_stability"] = round(
                self.var_stability.get(), 2)
            self.state.config["elevenlabs_style"] = round(self.var_style.get(), 2)
        self.state.save()

        base = self.state.base_pack_path
        ffmpeg = self.state.ffmpeg

        self.log.clear()
        self.log.append(t("tab_store.generating_dialect_log", name=pack.name), "step")
        # Das Sprechen hört auf den Abbruch - hier darf der Knopf mitspielen.
        self._busy(True, abbrechbar=True)
        self.badge.set(t("tab_store.speaking_announcements_badge"), "muted")

        modell, klang, eigene = self._eleven_klang()

        def work_fn(task):
            return dialect.generate(
                dialect=pack, base_pack=base, work_dir=work, ffmpeg=ffmpeg,
                voice=win_voice, engine=engine, api_key=api_key, voice_id=voice_id,
                model=modell, voice_settings=klang, use_voice_settings=eigene,
                mapping=self.state.voice_mapping(),
                out_name=out_name,
                rate=tempo, pitch=hoehe,
                log=lambda m: self._log(m),
                progress=lambda d, t: to_main(
                    self, self.progress.configure,
                    {"value": (d / t * 100) if t else 0}),
                cancelled=lambda: task.cancelled,
            )

        def ok(build) -> None:
            self.state.last_build = build
            self.state.prebuilt = build
            self.state.prebuilt_name = pack.name
            # Die Kennung kommt nicht mehr vom Paket: Aufgespielt wird
            # ausnahmslos unter CUSTOM. Stünde hier etwas anderes,
            # zeigte die Startseite eine Kennung an, die der Roboter
            # gar nicht führt.
            self.state.config["custom_lang_id"] = installer.DEFAULT_CUSTOM_LANG_ID
            self.state.save()
            self.state.notify("assignments_changed")

            # Beschreibung daneben legen, damit unter 'Fertige Stimmen' erkennbar bleibt,
            # welche Stimme in welchem Paket steckt.
            library.write_info(
                build.path, dialect=pack.name, engine=(
                    "ElevenLabs" if engine == dialect.ENGINE_ELEVENLABS
                    else t("tab_store.engine_windows_tts")),
                voice=stimmen_label, lang_id=pack.lang_id,
                replaced=len(build.replaced), total=pack.count)

            vollstaendig = len(build.replaced) >= pack.count
            self.badge.set(t("tab_store.generate_done_badge", count=len(build.replaced),
                             name=pack.name), "ok" if vollstaendig else "warn")
            self.log.append(build.summary(), "ok")
            for warnung in build.warnings:
                self.log.append(warnung, "warn")

            hinweis = ""
            if not vollstaendig:
                hinweis = t("tab_store.generate_missing_hint",
                            count=pack.count - len(build.replaced))

            messagebox.showinfo(
                t("tab_store.generate_ready_title", name=pack.name),
                t("tab_store.generate_ready_message", count=len(build.replaced),
                  name=pack.name, hint=hinweis, filename=build.path.name),
                parent=self)

        def fail(exc: Exception) -> None:
            # Ein selbst ausgelöster Abbruch ist kein Fehler und darf sich
            # auch nicht so anfühlen.
            if getattr(self, "_task", None) is not None and self._task.cancelled:
                gesprochen = dialect.spoken_count(work)
                self.badge.set(t("tab_store.cancelled_badge"), "warn")
                self.log.append(t("tab_store.operation_cancelled_log"), "warn")
                show_info(
                    self, self.theme, t("tab_store.cancelled_title"),
                    t("tab_store.no_pack_built_message"),
                    t("tab_store.cancelled_spoken_info", count=gesprochen, total=pack.count)
                    + (t("tab_store.cancelled_quota_note_eleven")
                       if engine == dialect.ENGINE_ELEVENLABS else
                       t("tab_store.cancelled_quota_note_windows")))
                return

            message, hint = error_text(exc)
            self.badge.set(t("tab_store.generate_failed_badge"), "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, t("tab_store.error_title"),
                       message + (f"\n\n{hint}" if hint else ""))

        self._task = run_async(self, work_fn, on_success=ok, on_error=fail,
                               on_finally=lambda: self._busy(False))

    # ------------------------------------------------------------------
    def _on_cancel_work(self) -> None:
        """Bricht einen laufenden Vorgang ab.

        Beim Sprechen über ElevenLabs zählt jede Ansage Kontingent. Wer
        sich verklickt hat, soll nicht zusehen müssen, wie sein Guthaben
        verbraucht wird. Bereits gesprochene Ansagen bleiben gespeichert -
        ihr Kontingent ist ohnehin weg, und beim nächsten Anlauf macht die
        App genau dort weiter.
        """
        task = getattr(self, "_task", None)
        if task is None or task.cancelled:
            return
        task.cancel()
        self.btn_abbrechen.configure(state="disabled")
        self.badge.set(t("tab_store.cancelling_badge"), "warn")
        self.log.append(t("tab_store.cancel_requested_log"), "warn")

    def _busy(self, active: bool, abbrechbar: bool = False) -> None:
        """Sperrt die Bedienung während der Arbeit.

        `abbrechbar` schaltet den Abbrechen-Knopf frei. Er bleibt gesperrt,
        wenn der laufende Vorgang gar nicht auf einen Abbruch hört - ein
        Knopf, der nichts tut, ist schlimmer als keiner.
        """
        state = "disabled" if active else "normal"
        for child in self.list_frame.winfo_children():
            if isinstance(child, PackCard):
                child.btn_use.configure(state=state)
        for button in self._dialect_buttons:
            button.configure(state=state)
        self.btn_abbrechen.configure(
            state="normal" if (active and abbrechbar) else "disabled")
        if not active:
            self._task = None
        if active:
            self.progress.pack(side="right")
            self.progress.configure(value=0)
        else:
            self.progress.pack_forget()

    def _log(self, message: str, kind: str = "info") -> None:
        to_main(self, self.log.append, message, kind)

    # ------------------------------------------------------------------
    def use_pack(self, pack: CommunityPack) -> None:
        if not self.state.has_base_pack:
            messagebox.showwarning(
                t("tab_store.original_pack_missing_title"),
                t("tab_store.original_pack_missing_use_message"),
                parent=self)
            return

        if not messagebox.askyesno(
                t("tab_store.use_pack_confirm_title", name=pack.name),
                t("tab_store.use_pack_confirm_message", url=pack.url),
                parent=self):
            return

        base = self.state.base_pack_path
        self.log.clear()
        self.log.append(t("tab_store.downloading_log", name=pack.name,
                          url=pack.project_url), "step")
        self._busy(True)
        self.badge.set(t("tab_store.downloading_badge"), "muted")

        def report(done: int, total: int) -> None:
            percent = (done / total * 100) if total else 0
            to_main(self, self.progress.configure, {"value": percent})

        def work(_task):
            archive = community.download(pack, progress=report)
            self._log(t("tab_store.downloaded_log", filename=archive.name), "ok")
            self._log(t("tab_store.adapting_pack_log"), "step")
            return packer.overlay_pack(
                base_pack=base,
                overlay_pack_path=archive,
                out_name=f"community_{pack.key}.tar.gz",
                mapping=self.state.voice_mapping(),
                log=lambda m: self._log(m),
                progress=lambda d, t: to_main(
                    self, self.progress.configure,
                    {"value": (d / t * 100) if t else 0}),
            )

        def ok(build: packer.BuildResult) -> None:
            self.state.last_build = build
            self.state.prebuilt = build
            self.state.prebuilt_name = pack.name
            self.state.notify("assignments_changed")

            covered = len(build.replaced)
            total = build.total_members or covered
            self.badge.set(t("tab_store.use_pack_ready_badge", covered=covered, total=total), "ok")
            self.log.append(build.summary(), "ok")
            for warning in build.warnings:
                self.log.append(warning, "warn")

            self.state.config["custom_lang_id"] = installer.DEFAULT_CUSTOM_LANG_ID
            self.state.save()

            messagebox.showinfo(
                t("tab_store.pack_prepared_title"),
                t("tab_store.pack_prepared_message", name=pack.name, covered=covered,
                  total=total),
                parent=self)

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            self.badge.set(t("tab_store.use_pack_failed_badge"), "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, t("tab_store.use_pack_error_title"),
                       message + (f"\n\n{hint}" if hint else ""))

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self._busy(False))
