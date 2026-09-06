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
from ..paths import build_dir
from .state import AppState, error_text, run_async, to_main
from .tab_builder import open_with_default_player
from .theme import Theme
from .widgets import (Card, InfoBanner, LogView, ScrollableList, ScrollablePage,
                      StatusBadge, show_error, show_info, show_warning)


# Die beiden Wege zu eigenen Aufnahmen. Der ZIP-Fall steht zuerst und wird
# beim Namen genannt: so heißen die Dateien auf der Projektseite.
WAHL_ARCHIV = "ZIP file or ready-made pack (.tar.gz)"
WAHL_ORDNER = "Folder with mp3, wav, or ogg files"

# Was passiert, wenn der gewählte Name schon vergeben ist. Das Danebenlegen
# steht zuerst und ist die Vorgabe - ein Paket, das Kontingent gekostet hat,
# soll nicht mit einem Klick verschwinden.
WAHL_DANEBEN = "Save alongside - the existing one stays"
WAHL_ERSETZEN = "Replace the existing one"


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

        meta = f"{pack.language}  ·  approx. {pack.approx_sounds} announcements"
        if pack.size_mb:
            meta += f"  ·  {pack.size_mb:.1f} MB"
        ttk.Label(head, text=meta, style="Muted.TLabel").pack(side="left", padx=(12, 0))

        ttk.Label(self, text=pack.description, style="Surface.TLabel",
                  wraplength=700, justify="left").grid(row=1, column=0, sticky="ew",
                                                       pady=(4, 0))

        source = f"Source: {pack.author}  ·  License: {pack.license}"
        ttk.Label(self, text=source, style="Muted.TLabel").grid(
            row=2, column=0, sticky="w", pady=(4, 0))

        if pack.notes:
            ttk.Label(self, text=pack.notes, style="Warning.TLabel",
                      wraplength=700, justify="left").grid(row=3, column=0,
                                                           sticky="ew", pady=(4, 0))

        buttons = ttk.Frame(self, style="Card.TFrame")
        buttons.grid(row=4, column=0, sticky="w", pady=(10, 0))

        self.btn_use = ttk.Button(buttons, text="Download and Adapt",
                                  style="Accent.TButton",
                                  command=lambda: tab.use_pack(pack))
        self.btn_use.pack(side="left")

        ttk.Button(buttons, text="View Project Page", style="Small.TButton",
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
            "Honestly: there's no real store. What's here are the few "
            "freely available fan projects that actually exist and whose "
            "files have been checked. Every pack is verified against its "
            "checksum on download and then laid over your model's "
            "official pack - anything the third-party pack doesn't cover "
            "stays on the German original voice.",
        ).pack(fill="x", pady=(0, 14))

        self._build_dialect_card(outer)

        listing = Card(outer, self.theme, "Available Packs")
        listing.pack(fill="both", expand=True, pady=(14, 0))

        # Der ganze Tab scrollt bereits - hier kein zweiter Bildlaufbereich.
        self.list_frame = ttk.Frame(listing.content, style="Card.TFrame")
        self.list_frame.pack(fill="both", expand=True)

        for pack in community.PACKS:
            card = PackCard(self.list_frame, self.theme, self, pack)
            card.pack(fill="x", padx=4)

        status = ttk.Frame(listing.content, style="Card.TFrame")
        status.pack(fill="x", pady=(10, 0))
        self.badge = StatusBadge(status, self.theme, "Ready")
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
        card = Card(outer, self.theme, "Generate Your Own: Dialect Packs",
                    f"{len(dialect.DIALECTS)} dialects, {spanne} announcements - "
                    f"nowhere can you download these ready-made.")
        card.pack(fill="x")

        ttk.Label(
            card.content,
            text=("Dialect packs don't exist for any vacuum robot to "
                  "download - not for Dreame, Roborock, Xiaomi, or "
                  "Valetudo. They've often been requested in forums, but "
                  "nobody's built them; the only one out there is a Swiss "
                  "German pack for the Roborock S5. So there's no "
                  "third-party pack to adapt.\n\n"
                  "This app therefore writes the announcements itself in "
                  "each dialect and has them spoken. With the Windows "
                  "voice this runs offline and free; for genuine dialect "
                  "in the pronunciation, you can switch to ElevenLabs."),
            style="Surface.TLabel", wraplength=820, justify="left").pack(anchor="w")

        # --- Dialektauswahl ---------------------------------------------
        picker = ttk.Frame(card.content, style="Card.TFrame")
        picker.pack(fill="x", pady=(14, 0))
        ttk.Label(picker, text="Dialect", style="Surface.TLabel").pack(side="left")

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
        ttk.Button(eigene, text="Create Custom Pack ...",
                   style="Small.TButton",
                   command=self._on_new_custom).pack(side="left")
        self.btn_rename = ttk.Button(eigene, text="Rename",
                                     style="Small.TButton",
                                     command=self._on_rename_custom)
        self.btn_rename.pack(side="left", padx=(8, 0))
        self.btn_delete_custom = ttk.Button(eigene, text="Delete",
                                            style="Small.TButton",
                                            command=self._on_delete_custom)
        self.btn_delete_custom.pack(side="left", padx=(8, 0))
        ttk.Button(eigene, text="Import Recordings ...",
                   style="Small.TButton",
                   command=self._on_import_ready).pack(side="left", padx=(8, 0))

        ttk.Label(card.content,
                  text=("'Create Custom Pack' creates your own text "
                        "collection - say, in the style of a movie "
                        "character. It behaves like a dialect: preview, "
                        "edit texts, generate with any voice, resume after "
                        "the quota runs out. 'Import Recordings' takes "
                        "already-spoken announcements: a ZIP file from the "
                        "project page, a ready-made .tar.gz, or a folder "
                        "full of mp3 and wav files."),
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
            fortschritt, text="Discard Progress", style="Small.TButton",
            command=self._on_discard_progress)

        self._build_engine_chooser(card.content)

        # --- Aktionen ----------------------------------------------------
        actions = ttk.Frame(card.content, style="Card.TFrame")
        actions.pack(fill="x", pady=(14, 0))

        self.btn_preview = ttk.Button(actions, text="Listen to Sample",
                                      command=self._on_preview_dialect)
        self.btn_preview.pack(side="left")
        self._dialect_buttons.append(self.btn_preview)

        self.btn_texts = ttk.Button(actions, text="View and Edit Texts",
                                    command=self._on_show_texts)
        self.btn_texts.pack(side="left", padx=(8, 0))

        self.btn_generate = ttk.Button(actions, text="Generate Pack",
                                       style="Accent.TButton",
                                       command=self._on_generate_selected)
        self.btn_generate.pack(side="left", padx=(8, 0))
        self._dialect_buttons.append(self.btn_generate)

        # Absichtlich NICHT in _dialect_buttons: dieser Knopf muss genau
        # dann bedienbar sein, wenn alle anderen gesperrt sind.
        self.btn_abbrechen = ttk.Button(actions, text="Cancel",
                                        command=self._on_cancel_work,
                                        state="disabled")
        self.btn_abbrechen.pack(side="left", padx=(8, 0))

        # --- Textdateien --------------------------------------------------
        dateien = ttk.Frame(card.content, style="Card.TFrame")
        dateien.pack(fill="x", pady=(8, 0))

        ttk.Button(dateien, text="Export Texts as Files",
                   style="Small.TButton",
                   command=self._on_export_texts).pack(side="left")
        ttk.Button(dateien, text="Import Texts from File",
                   style="Small.TButton",
                   command=self._on_import_texts).pack(side="left", padx=(8, 0))
        ttk.Button(dateien, text="Open Folder", style="Small.TButton",
                   command=self._on_open_text_folder).pack(side="left", padx=(8, 0))

        ttk.Label(card.content,
                  text=("The sample speaks three sentences with the "
                        "currently chosen voice and plays them - so you "
                        "can hear beforehand whether you like the result. "
                        "With ElevenLabs it costs about 60 characters from "
                        "the monthly quota.\n"
                        "Under 'View and Edit Texts' you can reword any "
                        "announcement. Your version stays saved; already-"
                        "spoken recordings of changed announcements are "
                        "discarded and re-recorded the next time you "
                        "generate.\n"
                        "For bigger rewrites, every dialect is also "
                        "available as a text file in the data folder: "
                        "copy it, have a language AI improve it, paste "
                        "the result back in, and read it in again."),
                  style="Muted.TLabel", wraplength=800,
                  justify="left").pack(anchor="w", pady=(6, 0))

        # Erst hier: die Auswahlliste füllt auch die Beschriftungen, die es
        # weiter oben noch gar nicht gibt.
        self._refill_dialect_picker()

        ttk.Label(
            card.content,
            text=("Recreating the voice of a real living person - say, "
                  "from YouTube recordings or other voice packs - is "
                  "legally sensitive (personality rights, and for actors "
                  "there's also exploitation rights). This app "
                  "deliberately offers no feature for that."),
            style="Muted.TLabel", wraplength=820, justify="left").pack(anchor="w",
                                                                       pady=(10, 0))

    # ------------------------------------------------------------------
    # Auswahlliste: mitgelieferte Dialekte und eigene Pakete
    # ------------------------------------------------------------------
    VORSATZ_DIALEKT = "Dialect · "
    VORSATZ_EIGEN = "Custom · "

    def _all_packs(self) -> list:
        """Alle wählbaren Pakete: erst die Dialekte, dann die eigenen."""
        try:
            eigene = custom.list_packs()
        except OSError:
            eigene = []
        return list(dialect.DIALECTS) + eigene

    def _label_for(self, pack) -> str:
        vorsatz = (self.VORSATZ_EIGEN if self._is_custom(pack)
                   else self.VORSATZ_DIALEKT)
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

        meta = f"{aktuell.count} announcements  ·  identifier {pack.lang_id}"
        if eigene:
            meta += f"  ·  {eigene} custom edited"
        self.lbl_dialect_meta.configure(text=meta)
        self.lbl_dialect_desc.configure(text=pack.description)
        samples = "\n".join(f"   {line}"
                            for line in dialect.preview_texts(aktuell, 6))
        self.lbl_samples.configure(text="Sample:\n" + samples)
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
                text="Progress: nothing spoken yet.",
                style="Muted.TLabel")
            self.btn_verwerfen.pack_forget()
            return

        teile = [f"Progress: {fertig} of {pack.count} announcements spoken"]
        if uebernommen:
            teile.append(f"of which {len(uebernommen)} taken over from "
                         f"existing files")
        if veraltet:
            teile.append(f"{len(veraltet)} belong to changed text and will "
                         f"be redone")
        offen = pack.count - fertig
        if offen > 0:
            teile.append(f"{offen} remaining - 'Generate Pack' continues from there")
        else:
            teile.append("everything's there, generating costs nothing more")

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
                "Discard Progress",
                f"{fertig} already-spoken announcements will be deleted.\n\n"
                f"Everything will be re-spoken next time you generate - "
                f"with ElevenLabs that costs quota again.\n\nReally delete?",
                parent=self):
            return

        try:
            shutil.rmtree(ordner / "gesprochen", ignore_errors=True)
            shutil.rmtree(ordner / "umgewandelt", ignore_errors=True)
        except OSError:
            pass
        self.refresh_progress()
        self.log.append(f"Progress discarded ({fertig} recordings).", "warn")

    # ------------------------------------------------------------------
    # Eigene Pakete anlegen, umbenennen, löschen
    # ------------------------------------------------------------------
    def _on_new_custom(self) -> None:
        """Legt eine eigene Textsammlung an - meist als Kopie eines Dialekts."""
        name = simpledialog.askstring(
            "Custom Voice Pack",
            "What should the pack be called?\n\n"
            "For example 'Bruce Willis', 'Pirate', or 'Butler'. The name "
            "only appears in this app - the robot gets a short identifier "
            "derived from it.",
            parent=self)
        if not name or not name.strip():
            return

        vorlagen = [f"Copy of {p.name}" for p in dialect.DIALECTS]
        vorlagen.append("Start Empty")

        wahl = self._ask_choice(
            "Start with What?",
            "A pack needs a text for every announcement.\n\n"
            "The easiest way is to copy an existing dialect: then every "
            "announcement is already there and you just reword it. Next "
            "to each line is what it needs to mean.\n\n"
            "Starting empty is only worth it if you just want to replace "
            "a few individual announcements - the rest then stays on the "
            "German original voice.",
            vorlagen, vorlagen[0])
        if wahl is None:
            return

        texte = {}
        if wahl != "Start Empty":
            quelle = next((p for p in dialect.DIALECTS
                           if f"Copy of {p.name}" == wahl), None)
            if quelle is not None:
                # Bewusst die wirksamen Texte: eigene Änderungen am Dialekt
                # sollen in der Kopie erhalten bleiben.
                texte = dict(self._effective_dialect(quelle).texts)

        vergeben = [p.lang_id for p in self._all_packs()]
        neu = custom.create(name.strip(), texte, vergeben=vergeben)
        try:
            custom.save(neu)
        except OSError as exc:
            show_error(self, self.theme, "Not Saved",
                       "The custom pack couldn't be created.",
                       f"Technical details: {exc}")
            return

        self.log.append(f"Custom pack '{neu.name}' created "
                        f"({neu.count} announcements, identifier {neu.lang_id}).", "ok")
        self._refill_dialect_picker(self._label_for(neu))
        show_info(
            self, self.theme, "Pack Created",
            f"'{neu.name}' is now in the selection.",
            f"{neu.count} announcements as a template, identifier {neu.lang_id}.\n\n"
            f"Use 'View and Edit Texts' to rewrite them - or hand the file\n"
            f"{custom.path_for(neu.key).name}\nfrom the '{custom.ORDNER}' "
            f"folder to a language AI. Then click 'Generate Pack' as usual.")

    def _on_rename_custom(self) -> None:
        pack = self._selected_dialect()
        if pack is None or not self._is_custom(pack):
            show_warning(self, self.theme, "No Custom Pack",
                         "Built-in dialects can't be renamed.",
                         "Choose a pack above that starts with 'Custom'.")
            return
        neu = simpledialog.askstring("Rename", "New name:",
                                     initialvalue=pack.name, parent=self)
        if not neu or not neu.strip():
            return
        custom.rename(pack, neu)
        try:
            custom.save(pack)
        except OSError as exc:
            show_error(self, self.theme, "Not Saved", str(exc))
            return
        self._refill_dialect_picker(self._label_for(pack))
        self.log.append(f"Renamed to '{pack.name}'.", "ok")

    def _on_delete_custom(self) -> None:
        pack = self._selected_dialect()
        if pack is None or not self._is_custom(pack):
            show_warning(self, self.theme, "No Custom Pack",
                         "Built-in dialects can't be deleted.",
                         "Choose a pack above that starts with 'Custom'.")
            return
        if not messagebox.askyesno(
                "Really Delete?",
                f"Delete '{pack.name}' with {pack.count} announcements?\n\n"
                f"Already-spoken recordings and built packs are kept - "
                f"only the text collection disappears.",
                parent=self):
            return
        custom.delete(pack.key)
        self.log.append(f"'{pack.name}' deleted.", "warn")
        self._refill_dialect_picker()

    def _on_import_ready(self) -> None:
        """Ein fertiges Paket oder einen Ordner voller Aufnahmen übernehmen."""
        if not self.state.has_base_pack:
            show_warning(
                self, self.theme, "Original Pack Missing",
                "First download your robot's official voice pack under "
                "'Individual Announcements'.",
                "Every custom pack is built as a copy of it - otherwise "
                "the robot would be missing every announcement you didn't "
                "supply yourself.")
            return

        art = self._ask_choice(
            "What Should Be Imported?",
            "The recordings from the project page are ZIP files like "
            "'Bayerisch-Aufnahmen.zip'. Use the first option for those and "
            "choose the ZIP directly - you don't need to unpack anything.\n\n"
            "Either way ends up as a finished pack in your collection and "
            "then shows up under 'Ready-Made Voices' for selection.",
            [WAHL_ARCHIV, WAHL_ORDNER],
            WAHL_ARCHIV)
        if art is None:
            return

        bekannt = self.state.catalog.ids() if self.state.catalog else None
        start = self.state.config["last_audio_dir"] or str(
            Path.home() / "Downloads")

        if art == WAHL_ARCHIV:
            quelle = filedialog.askopenfilename(
                parent=self, title="Choose a ZIP or Pack File",
                initialdir=start if Path(start).is_dir() else str(Path.home()),
                filetypes=[("Recordings and packs",
                            "*.zip *.tar.gz *.tgz *.tar"),
                           ("All files", "*.*")])
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
                parent=self, title="Choose the Folder with the Recordings",
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
                self, self.theme, "Nothing Found",
                f"{Path(quelle).name} contains no assignable recording.",
                "Files need the announcement number in their name, so "
                "7.ogg, 7.wav, or 7.mp3. A correctly-named template folder "
                "can be created under 'Individual Announcements'.")
            return

        name = simpledialog.askstring(
            "Name for This Pack",
            f"{len(zuordnung)} announcements found.\n\n"
            f"What name should the finished pack be saved under?",
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
                "This Pack Already Exists",
                f"Existing:\n{alt.label}\n\n"
                f"Replacing overwrites it permanently. The new pack is "
                f"built completely first - if that fails, the existing "
                f"one stays untouched.",
                [WAHL_DANEBEN, WAHL_ERSETZEN], WAHL_DANEBEN)
            if wahl is None:
                return
            if wahl == WAHL_ERSETZEN:
                ziel = schon_da
                self.log.append(f"Replacing {schon_da.name}.", "warn")
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
        self.log.append(f"Building pack from {len(zuordnung)} recordings ...", "step")
        self._busy(True)
        self.badge.set("Converting and building ...", "muted")

        def work_fn(_task):
            return packer.build_pack(
                base_pack=Path(base), assignments=zuordnung,
                out_name=ziel.name, ffmpeg=ffmpeg,
                work_dir=build_dir() / "_import_arbeit",
                mapping=mapping, log=lambda m: self._log(m))

        def ok(build) -> None:
            library.write_info(build.path, dialect=name.strip() or ziel.stem,
                               engine="Custom Recordings",
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
            self.badge.set(f"Done - {len(build.replaced)} announcements", "ok")
            self.log.append(build.summary(), "ok")
            for warnung in build.warnings:
                self.log.append(warnung, "warn")
            show_info(self, self.theme, "Pack Is Ready",
                      f"{len(build.replaced)} announcements taken over.",
                      f"Saved as:\n{build.path.name}\n\n"
                      f"Choose it for install under 'Ready-Made Voices'.")

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            self.badge.set("Failed", "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, "Pack Not Built", message, hint)

        run_async(self, work_fn, on_success=ok, on_error=fail,
                  on_finally=lambda: self._busy(False))

    def _on_import_error(self, exc: Exception) -> None:
        message, hint = error_text(exc)
        self.log.append(message, "error")
        show_error(self, self.theme, "Import Failed", message, hint)

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
        ttk.Button(knoepfe, text="Apply", style="Accent.TButton",
                   command=uebernehmen).pack(side="left")
        ttk.Button(knoepfe, text="Cancel",
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
            show_error(self, self.theme, "Files Not Written",
                       "The text files couldn't be created.",
                       f"Technical details: {exc}")
            return

        self.log.append(f"{len(pfade)} dialect text files written.", "ok")
        show_info(
            self, self.theme, "Text Files Created",
            f"{len(pfade)} files are now in:\n{textfiles.folder()}",
            "Copy a whole file, have a language AI rework it, paste the "
            "result back in and save. Then click 'Import Texts from File' "
            "here.\n\n"
            "Note: existing files were overwritten with the current state.")

    def _on_open_text_folder(self) -> None:
        try:
            open_with_default_player(textfiles.folder())
        except Exception as exc:                       # noqa: BLE001
            show_error(self, self.theme, "Folder Not Opened",
                       str(exc), f"The folder is here:\n{textfiles.folder()}")

    def _on_import_texts(self) -> None:
        """Liest eine überarbeitete Textdatei ein."""
        pack = self._selected_dialect()
        vorschlag = textfiles.file_for(pack.key) if pack else None

        pfad = filedialog.askopenfilename(
            parent=self,
            title="Import Revised Dialect Texts",
            initialdir=str(textfiles.folder()),
            initialfile=vorschlag.name if vorschlag else "",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not pfad:
            return

        pfad = Path(pfad)
        # Der Dialekt richtet sich nach dem Dateinamen, nicht nach der
        # Auswahl im Fenster - sonst landen kölsche Texte beim Bayerischen.
        ziel = next((p for p in self._all_packs() if p.key == pfad.stem), None)
        if ziel is None:
            show_warning(
                self, self.theme, "Pack Not Recognized",
                f"There's no matching pack for '{pfad.name}'.",
                "The file must be named like the pack, e.g. "
                "'wienerisch.txt'. Rename it and try again.")
            return

        try:
            ergebnis = textfiles.read_one(pfad, ziel)
        except (OSError, UnicodeError) as exc:
            show_error(self, self.theme, "File Not Readable",
                       f"{pfad.name} couldn't be read.",
                       f"Technical details: {exc}")
            return

        if not ergebnis.gelesen:
            show_warning(
                self, self.theme, "Nothing Found",
                f"{pfad.name} doesn't contain a single usable line.",
                "Every line needs the form\n"
                "  Number | Meaning | Dialect text\n\n"
                "If the AI changed the format, hand it the file again with "
                "a note to keep the line structure.")
            return

        hinweise = []
        if ergebnis.unbekannt:
            zeige = ", ".join(str(i) for i in ergebnis.unbekannt[:8])
            if len(ergebnis.unbekannt) > 8:
                zeige += " ..."
            hinweise.append(
                f"{len(ergebnis.unbekannt)} numbers don't exist for this "
                f"dialect and were skipped: {zeige}")
        if ergebnis.leer:
            hinweise.append(
                f"{ergebnis.leer} lines had no text - these announcements "
                f"stay as they were.")

        if not messagebox.askyesno(
                "Apply Texts?",
                f"{pfad.name}\n\n{ergebnis.summary()}\n\n"
                + ("\n".join(hinweise) + "\n\n" if hinweise else "")
                + f"Apply these texts for {ziel.name}?",
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
            f"{ziel.name}: {ergebnis.geaendert} texts taken over from "
            f"{pfad.name}.", "ok")

        zusatz = ""
        if verworfen:
            zusatz = (f"\n\n{verworfen} already-spoken recordings were "
                      f"discarded so they're re-created with the new text. "
                      f"All the rest stay and cost no quota.")
        show_info(self, self.theme, "Texts Applied",
                  f"{ergebnis.geaendert} of {ziel.count} announcements now "
                  f"differ from the built-in text.",
                  "The changes are kept, even after a restart."
                  + zusatz)

    def _on_show_texts(self) -> None:
        """Öffnet den Texteditor für den gewählten Dialekt."""
        pack = self._selected_dialect()
        if pack is None:
            return

        basis = pack                      # mitgelieferte Texte
        aktuell = self._effective_dialect(pack)   # mit eigenen Änderungen

        window = tk.Toplevel(self)
        window.title(f"{pack.name} - Edit {pack.count} Announcements")
        window.configure(bg=self.theme.color("bg"))
        window.geometry("900x700")
        window.transient(self.winfo_toplevel())

        card = Card(window, self.theme, f"Customize {pack.name}",
                    "Change the texts to however you want to hear them. "
                    "What you leave empty stays on the German original voice.")
        card.pack(fill="both", expand=True, padx=16, pady=16)

        suche_zeile = ttk.Frame(card.content, style="Card.TFrame")
        suche_zeile.pack(fill="x", pady=(0, 8))
        ttk.Label(suche_zeile, text="Search", style="Surface.TLabel").pack(side="left")
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
            lbl_zahl.configure(text="Building the list ...")
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
                hinweis = bedeutung + ("   ·  edited" if geaendert else "")
                ttk.Label(zeile, text=hinweis, style="Muted.TLabel",
                          anchor="w").grid(row=1, column=1, sticky="ew",
                                           pady=(1, 4))
                gezeigt += 1

            liste.scroll_to_top()
            lbl_zahl.configure(text=f"{gezeigt} of {basis.count} announcements")

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
                zusatz = (f"\n\n{verworfen} already-spoken recordings were "
                          f"discarded so they're re-created with your text.")
            show_info(self, self.theme, "Texts Saved",
                      f"{len(geaendert)} of {basis.count} announcements now "
                      f"differ from the built-in text.",
                      "The changes are kept, even after a restart."
                      + zusatz)

        def zuruecksetzen() -> None:
            if not messagebox.askyesno(
                    "Reset",
                    f"Discard all custom changes to {pack.name} and restore "
                    f"the built-in texts?", parent=window):
                return
            alt = self.state.config.dialect_overrides(pack.key)
            dialect.forget_cached_audio(basis, dialect.changed_ids(basis, alt))
            self.state.config.set_dialect_overrides(pack.key, {})
            self.state.save()
            window.destroy()
            self._on_dialect_changed()

        ttk.Button(knoepfe, text="Save", style="Accent.TButton",
                   command=speichern).pack(side="left")
        ttk.Button(knoepfe, text="Reset to Default",
                   command=zuruecksetzen).pack(side="left", padx=(8, 0))
        ttk.Button(knoepfe, text="Cancel",
                   command=window.destroy).pack(side="right")

    def _speak_text(self, text: str) -> None:
        """Spricht einen einzelnen Satz mit der gerade gewählten Stimme."""
        text = (text or "").strip()
        if not text:
            show_warning(self, self.theme, "No Text",
                         "This line has nothing to read out.")
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
                    self, self.theme, "Connect First",
                    "ElevenLabs needs a key and a voice.",
                    "The sentence can't be spoken without both. With the "
                    "Windows voice it works right away.")
                return
            voice_id = gewaehlt.voice_id
        else:
            if not tts.german_voices():
                show_warning(self, self.theme, "No German Voice",
                             "No German text-to-speech voice is installed.")
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
                show_error(self, self.theme, "Playback Not Possible",
                           f"The recording is here:\n{pfad}", str(exc))

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            show_error(self, self.theme, "Reading Aloud Failed", message, hint)

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
                    "Connect First",
                    "Enter your ElevenLabs key, click 'Connect and Load "
                    "Voices', and choose a voice. Then you can preview it "
                    "here.", parent=self)
                return
            voice_id = chosen.voice_id
        else:
            if not tts.german_voices():
                messagebox.showwarning(
                    "No German Voice",
                    "No German text-to-speech voice is installed.",
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
        self.badge.set("Speaking the sample ...", "muted")
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
            self.badge.set(f"Sample Ready - {len(files)} Sentences", "ok")
            self.log.append("Playing ...", "ok")
            for path in files:
                try:
                    open_with_default_player(path)
                except OSError as exc:
                    self.log.append(f"Couldn't play {path.name}: {exc}",
                                    "warn")
                    break

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            self.badge.set("Sample Failed", "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, "Sample Failed",
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
        ttk.Label(frame, text="Who Speaks?", style="Heading.TLabel").pack(anchor="w")

        self.var_engine = tk.StringVar(value=self.state.config["tts_engine"])

        # --- Windows ---------------------------------------------------
        win_row = ttk.Frame(frame, style="Card.TFrame")
        win_row.pack(fill="x", pady=(8, 0))
        ttk.Radiobutton(win_row, text="Windows Text-to-Speech",
                        variable=self.var_engine, value=dialect.ENGINE_WINDOWS,
                        command=self._on_engine_changed).pack(side="left")
        self.combo_winvoice = ttk.Combobox(win_row, state="readonly", width=30,
                                           values=[])
        self.combo_winvoice.pack(side="left", padx=(12, 0))

        self.lbl_voice = ttk.Label(
            frame,
            text=("   Offline, free, ready to use right away - but standard "
                  "German pronunciation. The dialect only lives in the "
                  "wording. Stefan is the only male German voice; System.Speech doesn't "
                  "know it, the app fetches it via the Windows Runtime."),
            style="Muted.TLabel", wraplength=800, justify="left")
        self.lbl_voice.pack(anchor="w", pady=(2, 0))

        # --- Regler für die Windows-Stimme --------------------------------
        self.win_regler = ttk.Frame(frame, style="Card.TFrame")
        ttk.Label(self.win_regler, text="   Rate",
                  style="Surface.TLabel").pack(side="left")
        self.var_rate = tk.IntVar(value=int(self.state.config["tts_rate"]))
        ttk.Scale(self.win_regler, from_=-6, to=6, orient="horizontal",
                  variable=self.var_rate, length=150,
                  command=lambda _v: self._on_win_regler()).pack(side="left",
                                                                 padx=(8, 8))
        self.lbl_rate = ttk.Label(self.win_regler, text="", style="Muted.TLabel")
        self.lbl_rate.pack(side="left")

        ttk.Label(self.win_regler, text="   Pitch",
                  style="Surface.TLabel").pack(side="left", padx=(16, 0))
        self.var_pitch = tk.IntVar(value=int(self.state.config["tts_pitch"]))
        ttk.Scale(self.win_regler, from_=-6, to=6, orient="horizontal",
                  variable=self.var_pitch, length=150,
                  command=lambda _v: self._on_win_regler()).pack(side="left",
                                                                 padx=(8, 8))
        self.lbl_pitch = ttk.Label(self.win_regler, text="", style="Muted.TLabel")
        self.lbl_pitch.pack(side="left")

        ttk.Button(self.win_regler, text="Reset", style="Small.TButton",
                   command=self._on_win_reset).pack(side="left", padx=(16, 0))

        # --- ElevenLabs -------------------------------------------------
        el_row = ttk.Frame(frame, style="Card.TFrame")
        el_row.pack(fill="x", pady=(12, 0))
        ttk.Radiobutton(el_row, text="ElevenLabs - genuine dialect pronunciation",
                        variable=self.var_engine, value=dialect.ENGINE_ELEVENLABS,
                        command=self._on_engine_changed).pack(side="left")

        bedarf = min((elevenlabs.estimate_characters(p.texts)
                      for p in dialect.DIALECTS), default=0)
        self.lbl_eleven_info = ttk.Label(
            frame,
            text=("   No freely available dialect speech model exists - "
                  "checked: Piper only has standard German, Thorsten-Voice "
                  "only Hessian, and the only Bavarian speech corpus "
                  "belongs to Bayerischer Rundfunk. ElevenLabs, on the "
                  "other hand, explicitly offers dialects, with 10,000 "
                  f"free characters a month. A dialect pack needs at "
                  f"least {bedarf} characters; full coverage more like "
                  f"double that. If the quota runs out, the app picks up "
                  f"there next time.\n"
                  "   You need your own (free) account. The app doesn't "
                  "create one. Only the announcement texts are transmitted."),
            style="Muted.TLabel", wraplength=800, justify="left")
        self.lbl_eleven_info.pack(anchor="w", pady=(2, 0))

        key_row = ttk.Frame(frame, style="Card.TFrame")
        key_row.pack(fill="x", pady=(8, 0))
        ttk.Label(key_row, text="   Access Key", style="Surface.TLabel").pack(
            side="left")
        self.var_key = tk.StringVar(value=self.state.config.elevenlabs_key)
        self.entry_key = ttk.Entry(key_row, textvariable=self.var_key, width=34,
                                   show="•")
        self.entry_key.pack(side="left", padx=(8, 8))
        self.btn_connect = ttk.Button(key_row, text="Connect and Load Voices",
                                      style="Small.TButton",
                                      command=self._on_connect_elevenlabs)
        self.btn_connect.pack(side="left")
        ttk.Button(key_row, text="Get a Key", style="Link.TButton",
                   command=self._open_api_key_page).pack(side="left", padx=(8, 0))
        ttk.Button(key_row, text="Forget Key", style="Link.TButton",
                   command=self._on_forget_key).pack(side="left", padx=(8, 0))

        self.lbl_key_ort = ttk.Label(frame, text="", style="Muted.TLabel",
                                     wraplength=800, justify="left")
        self.lbl_key_ort.pack(anchor="w", pady=(2, 0))

        voice_row = ttk.Frame(frame, style="Card.TFrame")
        voice_row.pack(fill="x", pady=(8, 0))
        ttk.Label(voice_row, text="   Voice", style="Surface.TLabel").pack(side="left")
        self.combo_elvoice = ttk.Combobox(voice_row, state="readonly", width=44,
                                          values=[])
        self.combo_elvoice.pack(side="left", padx=(8, 8))
        self.combo_elvoice.bind(
            "<<ComboboxSelected>>", lambda _e: self._on_elvoice_changed())
        self.btn_search = ttk.Button(voice_row, text="Search Voice Library",
                                     style="Small.TButton",
                                     command=self._on_search_bavarian)
        self.btn_search.pack(side="left")

        # Eigene Stimmen tauchen nicht immer in der Liste auf. Mit der ID
        # lässt sich jede Stimme direkt ansprechen.
        id_row = ttk.Frame(frame, style="Card.TFrame")
        id_row.pack(fill="x", pady=(8, 0))
        ttk.Label(id_row, text="   Custom Voice ID",
                  style="Surface.TLabel").pack(side="left")
        self.var_voice_id = tk.StringVar(
            value=self.state.config["elevenlabs_voice_id"])
        self.entry_voice_id = ttk.Entry(id_row, textvariable=self.var_voice_id,
                                        width=28)
        self.entry_voice_id.pack(side="left", padx=(8, 8))
        self.btn_add_id = ttk.Button(id_row, text="Apply",
                                     style="Small.TButton",
                                     command=self._on_add_voice_id)
        self.btn_add_id.pack(side="left")
        ttk.Label(id_row,
                  text="(in ElevenLabs: three dots on the voice > Copy Voice ID)",
                  style="Muted.TLabel").pack(side="left", padx=(10, 0))

        # --- Klang -------------------------------------------------------
        klang = ttk.Frame(frame, style="Card.TFrame")
        klang.pack(fill="x", pady=(8, 0))
        ttk.Label(klang, text="   Model", style="Surface.TLabel").pack(side="left")
        self.combo_model = ttk.Combobox(klang, state="readonly", width=34,
                                        values=[])
        self.combo_model.pack(side="left", padx=(8, 16))
        self.combo_model.set("Default (eleven_multilingual_v2)")

        self.var_own_settings = tk.BooleanVar(
            value=bool(self.state.config["elevenlabs_use_voice_settings"]))
        ttk.Checkbutton(klang, text="Use the voice's own sound",
                        variable=self.var_own_settings,
                        command=self._on_settings_mode).pack(side="left")

        self.regler = ttk.Frame(frame, style="Card.TFrame")
        ttk.Label(self.regler, text="   Liveliness",
                  style="Surface.TLabel").pack(side="left")
        self.var_stability = tk.DoubleVar(
            value=float(self.state.config["elevenlabs_stability"]))
        ttk.Scale(self.regler, from_=0.0, to=1.0, orient="horizontal",
                  variable=self.var_stability, length=150,
                  command=lambda _v: self._on_regler()).pack(side="left", padx=(8, 8))
        self.lbl_stability = ttk.Label(self.regler, text="", style="Muted.TLabel")
        self.lbl_stability.pack(side="left")

        ttk.Label(self.regler, text="   Expression",
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
            text=("   'Use the voice's own sound' uses exactly the "
                  "settings you've set on the voice in ElevenLabs - so it "
                  "sounds like the preview there. Without the checkbox you "
                  "control it yourself: lower stability means more life, "
                  "higher stability means more uniform."),
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
        self.lbl_rate.configure(
            text=f"{tempo * 10:+d} %  ({'normal' if tempo == 0 else 'slower' if tempo < 0 else 'faster'})")
        self.lbl_pitch.configure(
            text=f"{hoehe * 10:+d} %  ({'normal' if hoehe == 0 else 'lower' if hoehe < 0 else 'higher'})")
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
        art = ("very lively" if stab < 0.3 else
               "lively" if stab < 0.5 else
               "balanced" if stab < 0.7 else "uniform")
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
                text=("   No German text-to-speech voice is installed. "
                      "Windows Settings > Time and Language > Language > "
                      "German > Options > Add speech, then restart the app."),
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
        ort = self.state.config.elevenlabs_key_location
        if "Credential Manager" in ort:
            text = ("   Key is stored in the Windows Credential Manager - "
                    "viewable under Control Panel > Credential Manager > "
                    "Windows Credentials > “DreameSprachpaket:ElevenLabs”. "
                    "config.json doesn't contain it.")
            stil = "Success.TLabel"
        elif "config.json" in ort:
            text = ("   Key is stored encrypted in config.json "
                    "(the Windows Credential Manager wasn't reachable).")
            stil = "Muted.TLabel"
        else:
            text = "   Key isn't saved."
            stil = "Muted.TLabel"
        self.lbl_key_ort.configure(text=text, style=stil)

    def _on_forget_key(self) -> None:
        if not messagebox.askyesno(
                "Forget Key",
                "The saved ElevenLabs key will be removed - from the "
                "Windows Credential Manager and from config.json.\n\n"
                "Continue?", parent=self):
            return
        self.state.config.forget_elevenlabs_key()
        self.state.save()
        self.var_key.set("")
        self._refresh_key_location()
        self.lbl_eleven.configure(text="   Key removed.",
                                  style="Muted.TLabel")

    def _open_api_key_page(self) -> None:
        messagebox.showinfo(
            "Get an Access Key",
            "The page where ElevenLabs generates the key will open.\n\n"
            "Click 'Create API Key' there. The key is only shown in full "
            "once - copy it immediately and paste it here.\n\n"
            "If the page doesn't open directly: bottom left on your "
            "profile, then Settings > API Keys.\n\n"
            "This is included in the free plan (10,000 characters a month).",
            parent=self)
        webbrowser.open(elevenlabs.API_KEY_URL)

    def _on_connect_elevenlabs(self) -> None:
        key = self.var_key.get().strip()
        if not key:
            show_warning(
                self, self.theme, "Access Key Missing",
                "Create a free ElevenLabs account and paste the access "
                "key in here.",
                "Found under elevenlabs.io/app/settings/api-keys > "
                "Create API Key. The app doesn't create an account for you.")
            return

        if not elevenlabs.looks_like_key(key):
            show_warning(
                self, self.theme, "Key Looks Unusual",
                "The entered access key doesn't start with 'sk_'.",
                f"What's entered is {len(key)} characters starting with "
                f"'{key[:6]}…'. If this is a voice ID: that belongs in "
                f"the field below.\n\nThe connection will be attempted "
                f"anyway - maybe ElevenLabs changed the format.")

        self.btn_connect.configure(state="disabled")
        self.lbl_eleven.configure(text="Connecting ...", style="Muted.TLabel")

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
            wofuer = f"the pack '{gewaehlt.name}'" if gewaehlt else "a pack"
            enough = quota.left >= needed
            self.lbl_eleven.configure(
                text=(f"   Connected. Quota: {quota.describe()}. "
                      f"{wofuer} needs about {needed} characters - " +
                      ("that's enough." if enough else "that's not enough right now.")),
                style="Success.TLabel" if enough else "Warning.TLabel")

            eigene = [v for v in voices if v.is_own_creation]
            bavarian = [v for v in voices if v.is_bavarian]
            zusatz = f"\n   {len(voices)} voices in the account"
            if eigene:
                zusatz += f", {len(eigene)} of them self-created (listed above)"
            elif not bavarian:
                zusatz += (". None of them are labeled Bavarian - library "
                           "voices tend to be poor at it. Better: build your "
                           "own with Voice Design in ElevenLabs and enter "
                           "its ID below.")
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
                             "label": f"Default ({elevenlabs.MODEL})"}]

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
            show_warning(self, self.theme, "Access Key Missing",
                         "First enter your ElevenLabs key.")
            return
        if not voice_id:
            show_warning(
                self, self.theme, "No ID Entered",
                "Copy your voice's ID from ElevenLabs in here.",
                "You'll find it in the voice overview: click the three "
                "dots on the voice and choose 'Copy Voice ID'. It's about "
                "20 characters long.")
            return

        # Vertauschte Felder sind der häufigste Stolperstein - lieber vorher
        # erkennen als eine unverständliche Serverantwort zeigen.
        if voice_id.startswith("sk_"):
            show_warning(
                self, self.theme, "Fields Swapped?",
                "The voice ID field has an access key in it.",
                "Keys start with 'sk_', voice IDs don't. The key belongs "
                "in the field above, the voice ID here.")
            return
        if not elevenlabs.looks_like_key(key):
            show_warning(
                self, self.theme, "Key Looks Unusual",
                f"The entered access key doesn't start with 'sk_'.",
                f"What's entered is {len(key)} characters starting with "
                f"'{key[:6]}…'. An ElevenLabs key looks like this: "
                f"sk_ followed by about 45 more characters.\n\n"
                f"Get a new key: elevenlabs.io/app/settings/api-keys "
                f"> Create API Key. It's only shown in full once.")
            return

        self.btn_add_id.configure(state="disabled")
        self.lbl_eleven.configure(text="   Fetching the voice ...", style="Muted.TLabel")

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
                text=f"   '{voice.name}' is selected. Preview it with "
                     f"'Listen to Sample'.",
                style="Success.TLabel")

        def fail(exc):
            message, hint = error_text(exc)
            self.lbl_eleven.configure(text=f"   {message} {hint}".strip(),
                                      style="Danger.TLabel")
            show_error(self, self.theme, "Voice Not Found",
                       message + (f"\n\n{hint}" if hint else ""))

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_add_id.configure(state="normal"))

    # ------------------------------------------------------------------
    def _on_search_bavarian(self) -> None:
        key = self.var_key.get().strip() or self.state.config.elevenlabs_key
        if not key:
            messagebox.showinfo("Access Key Missing",
                                "First enter your ElevenLabs key.",
                                parent=self)
            return

        self.btn_search.configure(state="disabled")
        self.lbl_eleven.configure(text="   Searching the voice library ...",
                                  style="Muted.TLabel")

        def work(_task):
            return elevenlabs.search_bavarian_voices(key)

        def ok(found):
            if not found:
                self.lbl_eleven.configure(
                    text=("   No voice labeled Bavarian was found in the "
                          "library right now. Best to build your own in "
                          "ElevenLabs (Voice Design) and enter its ID below."),
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
        window.title("Choose a Voice")
        window.configure(bg=self.theme.color("bg"))
        window.geometry("760x560")
        window.transient(self)
        window.grab_set()

        card = Card(window, self.theme, f"{len(found)} Voices Found",
                    "Choose the voice to add to your ElevenLabs account. "
                    "You can preview it afterward with 'Listen to Sample'.")
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
                    block, text="Listen on ElevenLabs", style="Link.TButton",
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

        ttk.Button(buttons, text="Add Selected Voice",
                   style="Accent.TButton", command=uebernehmen).pack(side="left")
        ttk.Button(buttons, text="Cancel",
                   command=window.destroy).pack(side="left", padx=(8, 0))
        ttk.Label(buttons,
                  text=("None of these fit? Build your own in ElevenLabs "
                        "with Voice Design and enter its ID in the field "
                        "below."),
                  style="MutedBg.TLabel", wraplength=380,
                  justify="left").pack(side="left", padx=(16, 0))

    def _add_voice(self, key: str, voice) -> None:
        def work(_task):
            elevenlabs.add_shared_voice(key, voice)
            return elevenlabs.list_voices(key)

        def ok(voices):
            self._set_eleven_voices(voices)
            self.lbl_eleven.configure(
                text=f"   '{voice.name}' is now in your account and selected.",
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
                "Original Pack Missing",
                "First download your robot's official voice pack under "
                "'Individual Announcements' - it's the foundation of every pack.",
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
                    "Access Key Missing",
                    "Enter your ElevenLabs key and click 'Connect and Load "
                    "Voices'.", parent=self)
                return
            if chosen is None:
                messagebox.showwarning(
                    "No Voice Chosen",
                    "Click 'Connect and Load Voices' and then choose a "
                    "voice - preferably a Bavarian one.", parent=self)
                return
            voice_id = chosen.voice_id
            # Bei selbst erzeugten Stimmen sagen die Merkmale nichts über den
            # Dialekt aus - da weiß der Nutzer besser Bescheid als die Labels.
            if (not chosen.is_bavarian and not chosen.is_own_creation
                    and not messagebox.askyesno(
                        "No Bavarian Voice",
                        f"'{chosen.name}' isn't labeled Bavarian. The result "
                        f"won't sound like the dialect then.\n\nContinue "
                        f"anyway?", parent=self)):
                return
        else:
            if not tts.german_voices():
                messagebox.showwarning(
                    "No German Voice",
                    "No German text-to-speech voice is installed.\n\n"
                    "Windows Settings > Time and Language > Language > "
                    "German > Options > Add speech. Then restart the app.",
                    parent=self)
                return
            win_voice = self._selected_win_voice()

        if not self.state.ffmpeg:
            messagebox.showwarning(
                "ffmpeg Missing",
                "ffmpeg is needed to convert the spoken announcements.\n\n"
                "Briefly switch to 'Individual Announcements' - the app "
                "sets it up there.",
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

            question = (f"Already spoken: {schon_da} of {pack.count} "
                        f"announcements.\nStill open: {len(offen)} "
                        f"({chars} characters).\n\n")

            if rest is not None:
                question += f"Your quota: {rest} characters free.\n"
                if rest < chars:
                    passt = 0
                    verbraucht = 0
                    for _i, t in sorted(offen.items()):
                        if verbraucht + len(t) > rest:
                            break
                        verbraucht += len(t)
                        passt += 1
                    question += (
                        f"\nTHAT'S NOT ENOUGH FOR EVERYTHING: about {passt} of "
                        f"the {len(offen)} remaining announcements are "
                        f"doable.\n\n"
                        f"The app won't abort because of this. It speaks as "
                        f"much as possible, builds the pack with that, and "
                        f"the rest stays in standard German. Next month just "
                        f"click 'Generate Pack' again - it picks up exactly "
                        f"here and only speaks what's missing.\n")
                else:
                    question += "\nThat's enough for everything remaining.\n"

            question += ("\nOnly the announcement texts are transmitted, no "
                         "personal data.\n\nContinue?")
        else:
            question = (
                f"The app will now speak {len(offen)} announcements for "
                f"{pack.name} and build a voice pack from them."
                + (f"\n\n{schon_da} are already spoken and will be "
                   f"skipped." if schon_da else "")
                + f"\n\nThis takes a few minutes and happens entirely on "
                  f"this PC - nothing gets uploaded.\n\nContinue?")

        if not messagebox.askyesno(f"Generate {pack.name}?", question, parent=self):
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
            "Name for This Pack",
            "What name should the pack be saved under?\n\n"
            "The suggestion includes dialect and voice, so several "
            "versions can exist side by side. An existing pack is never "
            "overwritten - the app appends a number if needed.",
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
        self.log.append(f"Generating dialect pack: {pack.name}", "step")
        # Das Sprechen hört auf den Abbruch - hier darf der Knopf mitspielen.
        self._busy(True, abbrechbar=True)
        self.badge.set("Speaking the announcements ...", "muted")

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
                    else "Windows Text-to-Speech"),
                voice=stimmen_label, lang_id=pack.lang_id,
                replaced=len(build.replaced), total=pack.count)

            vollstaendig = len(build.replaced) >= pack.count
            self.badge.set(f"Done - {len(build.replaced)} announcements for "
                           f"{pack.name}", "ok" if vollstaendig else "warn")
            self.log.append(build.summary(), "ok")
            for warnung in build.warnings:
                self.log.append(warnung, "warn")

            hinweis = ""
            if not vollstaendig:
                hinweis = (f"\n\n{pack.count - len(build.replaced)} announcements are "
                           f"still missing - the ElevenLabs quota was "
                           f"probably used up. What's spoken is saved: just "
                           f"start generating again next month, and the app "
                           f"picks up exactly there.")

            messagebox.showinfo(
                f"{pack.name} Is Ready",
                f"{len(build.replaced)} announcements now speak {pack.name}, "
                f"the rest stays in standard German.{hinweis}\n\n"
                f"Saved as:\n{build.path.name}\n\n"
                f"Earlier packs are kept. Switch to 'Ready-Made Voices' - "
                f"there you choose which one gets installed.",
                parent=self)

        def fail(exc: Exception) -> None:
            # Ein selbst ausgelöster Abbruch ist kein Fehler und darf sich
            # auch nicht so anfühlen.
            if getattr(self, "_task", None) is not None and self._task.cancelled:
                gesprochen = dialect.spoken_count(work)
                self.badge.set("Cancelled", "warn")
                self.log.append("Operation cancelled.", "warn")
                show_info(
                    self, self.theme, "Cancelled",
                    f"No pack was built.",
                    f"{gesprochen} of {pack.count} announcements are spoken "
                    f"and stay saved."
                    + (" The ElevenLabs quota spent on those is gone, but "
                       "next time the app picks up exactly here and only "
                       "requests what's missing."
                       if engine == dialect.ENGINE_ELEVENLABS else
                       " Next time the app picks up exactly here."))
                return

            message, hint = error_text(exc)
            self.badge.set("Failed", "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, "Error",
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
        self.badge.set("Cancelling ...", "warn")
        self.log.append("Cancellation requested - the current announcement "
                        "will still finish being spoken.", "warn")

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
                "Original Pack Missing",
                "First download your robot's official voice pack under "
                "'Individual Announcements'. Only then can a third-party "
                "pack be safely adapted to your model.",
                parent=self)
            return

        if not messagebox.askyesno(
                f"Use '{pack.name}'?",
                f"The pack will be downloaded from this source:\n\n{pack.url}\n\n"
                f"It'll then be laid over your model's official pack. "
                f"After that you can install it under 'Build and "
                f"Install'.\n\nContinue?",
                parent=self):
            return

        base = self.state.base_pack_path
        self.log.clear()
        self.log.append(f"Downloading '{pack.name}' from {pack.project_url}", "step")
        self._busy(True)
        self.badge.set("Downloading ...", "muted")

        def report(done: int, total: int) -> None:
            percent = (done / total * 100) if total else 0
            to_main(self, self.progress.configure, {"value": percent})

        def work(_task):
            archive = community.download(pack, progress=report)
            self._log(f"Downloaded: {archive.name}", "ok")
            self._log("Adapting the pack to your model ...", "step")
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
            self.badge.set(f"Ready - {covered} of {total} announcements replaced", "ok")
            self.log.append(build.summary(), "ok")
            for warning in build.warnings:
                self.log.append(warning, "warn")

            self.state.config["custom_lang_id"] = installer.DEFAULT_CUSTOM_LANG_ID
            self.state.save()

            messagebox.showinfo(
                "Pack Prepared",
                f"'{pack.name}' has been adapted to your model.\n\n"
                f"{covered} of {total} announcements get the new voice, the "
                f"rest stays in German.\n\nNow switch to "
                f"'Build and Install' and click "
                f"'Install Voice Pack on Robot'.",
                parent=self)

        def fail(exc: Exception) -> None:
            message, hint = error_text(exc)
            self.badge.set("Failed", "error")
            self.log.append(message, "error")
            if hint:
                self.log.append(hint, "warn")
            show_error(self, self.theme, "Error",
                       message + (f"\n\n{hint}" if hint else ""))

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self._busy(False))
