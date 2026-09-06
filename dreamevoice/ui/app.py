"""Das Hauptfenster: Seitenleiste links, jeweils eine Seite rechts."""

from __future__ import annotations

import logging
import os
import subprocess
import sys
import tkinter as tk
import traceback
import webbrowser
from tkinter import messagebox, ttk

from .. import (APP_NAME, AUTOR, HAFTUNG, LIZENZ, PROJEKT_URL, SPENDEN_URL,
                __version__, textfiles)
from .. import aktualisierung, anleitungen, i18n
from ..i18n import t
from ..paths import data_dir, icon_file, log_file
from .page_start import StartPage
from .page_voice import VoicePage
from .shell import NavShell
from .state import AppState, run_async, spaeter
from .tab_builder import BuilderTab
from .tab_connect import ConnectTab
from .tab_install import InstallTab
from .tab_store import StoreTab
from .fenster_update import UpdateFenster
from .theme import Theme
from .widgets import Card, show_error, show_warning

_LOG = logging.getLogger(__name__)

# Bewusst klein gehalten: die Tabs scrollen bei Bedarf, deshalb muss das
# Fenster nicht groß genug für den ganzen Inhalt sein. Ein zu großes
# Mindestmaß macht die App auf kleinen Notebooks unbenutzbar.
WINDOW_MIN = (860, 560)


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.state_obj = AppState()
        i18n.set_language(self.state_obj.config["ui_language"])
        self._symbol_setzen()
        self.title(f"{APP_NAME}  {__version__}")
        self.minsize(*WINDOW_MIN)
        self._center(1180, 800)

        self.theme = Theme(self, dark=bool(self.state_obj.config["dark_mode"]))
        self._build()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.report_callback_exception = self._on_unhandled

        self._ensure_dialect_files()

        # Jetzt steht das Fenster - erst hier gibt es ein äußeres
        # Fenster, dem sich ein Symbol anheften lässt.
        if sys.platform == "win32":
            self.update_idletasks()
            self._symbol_scharf(icon_file())

    # ------------------------------------------------------------------
    def _symbol_setzen(self) -> None:
        """Setzt das Symbol des Fensters und in der Taskleiste.

        `app.ico` ging bisher nur an PyInstaller - das ist das Symbol
        der DATEI im Explorer. Das Fenster selbst zeigte weiter Tks
        eingebaute Feder.

        Unter Windows genügt das Symbol allein nicht: Ohne eigene
        "AppUserModelID" ordnet die Taskleiste das Fenster dem
        Python-Interpreter zu und nimmt dessen Symbol. Der Aufruf muss
        vor dem ersten Fenster passieren.

        Schlägt irgendetwas davon fehl, bleibt es beim Bisherigen -
        ein Symbol ist es nicht wert, dass die App nicht startet.
        """
        if sys.platform == "win32":
            try:
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "Anon365Project.DreameSprachpaketManager")
            except Exception:                          # noqa: BLE001
                _LOG.debug("AppUserModelID nicht gesetzt", exc_info=True)

        pfad = icon_file()
        if pfad is None:
            _LOG.debug("Keine app.ico gefunden - Fenstersymbol bleibt leer")
            return
        try:
            # default=True gilt auch für alle späteren Fenster - Hilfe,
            # Über, Aktualisierung tragen damit dasselbe Symbol.
            self.iconbitmap(default=str(pfad))
        except tk.TclError:
            _LOG.debug("Fenstersymbol ließ sich nicht setzen", exc_info=True)

        # Unter Windows reicht das nicht: Tk lädt aus der ICO-Datei im
        # Wesentlichen EINE Größe, und Windows rechnet daraus alles
        # andere hoch - in der Taskleiste sieht man das sofort. Deshalb
        # zusätzlich die Fassungen holen, die das System gerade
        # anfordert, und sie direkt ans Fenster hängen.
        # Das passgenaue Symbol wird erst am Ende von __init__ gesetzt:
        # Vorher existiert das äußere Fenster noch nicht, an dem der
        # Taskleisteneintrag hängt - ein "after(0, ...)" feuerte zu
        # früh, und WM_GETICON meldete danach weiterhin "keines".

    def _symbol_scharf(self, pfad) -> None:
        """Hängt passgenaue Symbolgrößen ans Fenster (nur Windows).

        Muss nach dem Erzeugen des Fensters laufen - vorher gibt es
        kein Fensterhandle, an das sich etwas hängen ließe.
        """
        if pfad is None:
            return
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            user32.LoadImageW.restype = wintypes.HANDLE
            user32.SendMessageW.restype = ctypes.c_void_p

            # ACHTUNG: winfo_id() liefert bei Tk das INNERE Fenster
            # (Klasse "TkChild"). Der Eintrag in der Taskleiste und die
            # Titelleiste hängen aber am äußeren ("TkTopLevel").
            # Ein Symbol an das innere Fenster zu hängen, bewirkt gar
            # nichts - WM_GETICON meldete danach weiterhin "keines".
            innen = wintypes.HWND(self.winfo_id())
            aussen = user32.GetParent(innen)
            handle = wintypes.HWND(aussen) if aussen else innen
            #: SM_CXSMICON / SM_CXICON - beide sind DPI-abhängig, das
            #: System nennt also von sich aus die richtige Größe.
            klein = user32.GetSystemMetrics(49)
            gross = user32.GetSystemMetrics(11)

            IMAGE_ICON, LR_LOADFROMFILE = 1, 0x00000010
            WM_SETICON = 0x0080
            #: Die Symbole bleiben absichtlich am Objekt hängen: Gibt
            #: Python sie frei, zeigt Windows wieder das alte Bild.
            self._symbole = []
            for kante, welches in ((klein, 0), (gross, 1)):
                bild = user32.LoadImageW(None, str(pfad), IMAGE_ICON,
                                         kante, kante, LR_LOADFROMFILE)
                if not bild:
                    continue
                self._symbole.append(bild)
                user32.SendMessageW(handle, WM_SETICON, welches, bild)
        except Exception:                              # noqa: BLE001
            _LOG.debug("Passgenaues Fenstersymbol nicht gesetzt", exc_info=True)

    # ------------------------------------------------------------------
    def _ensure_dialect_files(self) -> None:
        """Legt die Dialekt-Textdateien an, falls sie noch fehlen.

        Sie sollen einfach da sein, ohne dass man erst einen Knopf sucht.
        Vorhandene Dateien werden nicht angefasst - eine eigene
        Überarbeitung darf beim Start nicht verlorengehen.
        """
        try:
            neu = textfiles.ensure_files(self.state_obj.config.dialect_overrides)
        except OSError as exc:
            _LOG.warning("Dialekt-Textdateien nicht angelegt: %s", exc)
            return
        if neu:
            _LOG.info("%d Dialekt-Textdateien angelegt", len(neu))

    # ------------------------------------------------------------------
    def _center(self, width: int, height: int) -> None:
        """Setzt eine sinnvolle Startgröße - passend zum Bildschirm."""
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Auf großen Bildschirmen bleibt es bei der Wunschgröße, auf
        # kleinen wird so viel genommen, wie da ist.
        width = max(WINDOW_MIN[0], min(width, screen_w - 100))
        height = max(WINDOW_MIN[1], min(height, screen_h - 120))

        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2 - 20)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(True, True)

        # Passt das Fenster ohnehin kaum auf den Bildschirm, startet es
        # gleich maximiert.
        if screen_h - 120 <= height or screen_w - 100 <= width:
            self._maximize()

    def _maximize(self) -> None:
        """Maximiert über den ganzen Bildschirm.

        Der Umweg über 'zoomed' ist nötig, weil ein bloßes geometry() auf
        Bildschirmgröße die Taskleiste überdeckt und das Fenster je nach
        Skalierung trotzdem nicht ausfüllt.
        """
        try:
            self.state("zoomed")
        except tk.TclError:
            try:
                self.attributes("-zoomed", True)      # Linux-Fenstermanager
            except tk.TclError:
                self.geometry(f"{self.winfo_screenwidth()}x"
                              f"{self.winfo_screenheight()}+0+0")

    def _toggle_maximize(self) -> None:
        if self.state() == "zoomed":
            self.state("normal")
        else:
            self._maximize()

    # ------------------------------------------------------------------
    def _build(self) -> None:
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(16, 0))

        left = ttk.Frame(header, style="TFrame")
        left.pack(side="left")
        ttk.Label(left, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(left,
                  text=t("app.subtitle"),
                  style="MutedBg.TLabel").pack(anchor="w", pady=(2, 0))

        right = ttk.Frame(header, style="TFrame")
        right.pack(side="right")
        self.var_language = tk.StringVar(
            value="Deutsch" if self.state_obj.config["ui_language"] == "de"
            else "English")
        language_box = ttk.Combobox(right, textvariable=self.var_language,
                                    values=["English", "Deutsch"],
                                    state="readonly", width=9)
        language_box.pack(side="left", padx=(0, 12))
        language_box.bind("<<ComboboxSelected>>", self._toggle_language)
        self.var_dark = tk.BooleanVar(value=bool(self.state_obj.config["dark_mode"]))
        ttk.Checkbutton(right, text=t("app.dark_mode_checkbox"), style="Bg.TCheckbutton",
                        variable=self.var_dark,
                        command=self._toggle_theme).pack(side="left", padx=(0, 12))
        # Kein "Vollbild"-Knopf mehr: Er tat nichts anderes als das
        # Viereck in der Fensterleiste von Windows - zwischen "zoomed"
        # und "normal" umschalten. Ein Knopf, der einen vorhandenen
        # Systemknopf verdoppelt, kostet Platz und Aufmerksamkeit und
        # bringt nichts dazu. Über F11 geht es weiterhin.
        # Aktualisierung gehört neben Hilfe und Über: Sie betrifft die
        # App selbst. Früher lag sie auf der Seite "Verbindung", unter
        # Konto und Roboterliste - dort sucht sie niemand, und der
        # Schalter "beim Start nachsehen" war damit ebenso versteckt.
        ttk.Button(right, text=t("app.updates_button"), style="Small.TButton",
                   command=self._show_update).pack(side="left", padx=(0, 8))
        ttk.Button(right, text=t("app.help_button"), style="Small.TButton",
                   command=self._show_help).pack(side="left")
        ttk.Button(right, text=t("app.about_button"), style="Small.TButton",
                   command=self._show_about).pack(side="left", padx=(8, 0))

        self.bind("<F11>", lambda _e: self._toggle_maximize())

        self.shell = NavShell(self, self.theme)
        self.shell.pack(fill="both", expand=True, padx=(0, 0), pady=(14, 0))

        buehne = self.shell.buehne
        # Die beiden Seiten, die jeder sieht, entstehen sofort. Die
        # vier unter "Erweitert" erst beim ersten Öffnen - sie machen
        # den Großteil der über tausend Bedienelemente aus, und die
        # meisten Benutzer sehen keine davon je an.
        self.page_start = StartPage(buehne, self.theme, self.state_obj,
                                    gehe_zu=self.shell.show)
        self.page_voice = VoicePage(buehne, self.theme, self.state_obj,
                                    gehe_zu=self.shell.show)

        # Oben, was man ständig tut - darunter, was selten vorkommt.
        # "Fertige Stimmen" fasst zusammen, was früher auf Tab 4 (aussuchen)
        # und Tab 3 (aufspielen) verteilt war - siehe page_voice.py.
        self.shell.add("start", "Start", "🏠", self.page_start,
                       beim_zeigen=self.page_start.refresh)
        self.shell.add("stimme", t("app.nav_ready_made_voices"), "🔊", self.page_voice,
                       beim_zeigen=self.page_voice.refresh)
        self.shell.add("eigene", t("app.nav_custom_voices"), "🎙",
                       bauen=lambda: StoreTab(buehne, self.theme,
                                              self.state_obj),
                       section=t("app.section_advanced"), beim_zeigen=self._beim_eigene)
        self.shell.add("ansagen", t("app.nav_individual_announcements"), "🧩",
                       bauen=lambda: BuilderTab(buehne, self.theme,
                                                self.state_obj),
                       section=t("app.section_advanced"), beim_zeigen=self._beim_ansagen)
        self.shell.add("aufspielen", t("app.nav_build_install"), "⬆",
                       bauen=lambda: InstallTab(buehne, self.theme,
                                                self.state_obj),
                       section=t("app.section_advanced"),
                       beim_zeigen=lambda: self.tab_install.refresh_summary())
        self.shell.add("verbindung", t("app.nav_connection"), "🔌",
                       bauen=lambda: ConnectTab(buehne, self.theme,
                                                self.state_obj),
                       section=t("app.section_advanced"),
                       beim_zeigen=lambda: self.tab_connect.beim_zeigen())

        self.shell.show("start")
        self._zustand_spiegeln()
        for ereignis in ("device_changed", "base_pack_changed"):
            self.state_obj.subscribe(ereignis, self._zustand_spiegeln)

        status = ttk.Frame(self, style="TFrame")
        status.pack(fill="x", padx=20, pady=(6, 12))
        # Früher stand hier der volle Pfad des Datenordners. Der ist auf
        # jedem Rechner anders lang, schiebt sich über die halbe
        # Fensterbreite und sagt einem Laien nichts - er will nicht
        # wissen, WO die Dateien liegen, sondern hinkommen. Also ein
        # Knopf statt einer Zeile Text; den Pfad zeigt der Hinweis beim
        # Darüberfahren.
        ttk.Button(status, text=t("app.open_data_folder_button"), style="Link.TButton",
                   command=self._datenordner_oeffnen).pack(side="left")
        ttk.Label(status,
                  text=t("app.data_folder_hint"),
                  style="MutedBg.TLabel").pack(side="left", padx=(10, 0))

        # Die beiseitegelegte Vorgängerfassung kann erst jetzt weg -
        # beim Tausch lief sie noch. Kostet nichts und fällt nicht auf.
        try:
            aktualisierung.altlasten_entfernen()
        except Exception:                              # noqa: BLE001
            _LOG.debug("Aufräumen alter Fassungen fehlgeschlagen",
                       exc_info=True)

        # spaeter() statt after(): Der Auftrag wird beim Zerstören des
        # Fensters abbestellt. Ohne das feuert er ins Leere, und Tk
        # meldet "invalid command name ...".
        spaeter(self, 2500, self._update_still_pruefen)

    # ------------------------------------------------------------------
    # Die vier Seiten unter "Erweitert" entstehen erst beim ersten
    # Zugriff. Über diese Eigenschaften bleibt jeder bisherige
    # Aufruf unverändert gültig - er baut die Seite eben, wenn er
    # der erste ist.
    @property
    def tab_store(self):
        return self.shell.seite("eigene")

    @property
    def tab_builder(self):
        return self.shell.seite("ansagen")

    @property
    def tab_install(self):
        return self.shell.seite("aufspielen")

    @property
    def tab_connect(self):
        return self.shell.seite("verbindung")

    # ------------------------------------------------------------------
    def _update_still_pruefen(self) -> None:
        """Beim Start nachsehen - nur wenn eingeschaltet, und leise.

        Leise heißt: Ein ausgefallener Server, kein Netz oder eine
        Zeitüberschreitung sind kein Grund, jemandem beim Start ein
        Fehlerfenster hinzustellen. Gemeldet wird nur, was es Neues
        gibt.
        """
        cfg = self.state_obj.config
        if not cfg["update_pruefen"]:
            return
        # Höchstens einmal am Tag - sonst fragt die App bei jedem
        # Start nach, ohne dass sich etwas geändert haben könnte.
        if aktualisierung.jetzt() - int(cfg["update_zuletzt"] or 0) < 86400:
            return

        def work(_task):
            return aktualisierung.pruefen()

        def ok(neuerung) -> None:
            cfg["update_zuletzt"] = aktualisierung.jetzt()
            self.state_obj.save()
            if neuerung is None:
                return
            if neuerung.version == (cfg["update_uebersprungen"] or ""):
                return
            self._update_melden(neuerung)

        def still(_exc: Exception) -> None:
            # Auch ein Fehlschlag zählt als "nachgesehen". Sonst
            # versucht es die App bei JEDEM Start neu und arbeitet
            # damit gegen das Ratenlimit, das den Fehler ausgelöst
            # haben könnte.
            cfg["update_zuletzt"] = aktualisierung.jetzt()
            self.state_obj.save()
            _LOG.info("Suche nach Aktualisierungen fehlgeschlagen: %s", _exc)

        run_async(self, work, on_success=ok, on_error=still)

    def _update_melden(self, neuerung) -> None:
        """Fragt einmal nach - und merkt sich ein Nein."""
        antwort = messagebox.askyesnocancel(
            t("app.update_available_title", version=neuerung.version),
            t("app.update_available_body", current=__version__,
              new=neuerung.version),
            parent=self)
        if antwort is None:
            self.state_obj.config["update_uebersprungen"] = neuerung.version
            self.state_obj.save()
            return
        if not antwort:
            return
        self._show_update(neuerung)

    def _beim_ansagen(self) -> None:
        self.tab_builder.refresh_rows()
        self.tab_builder.refresh_counter()

    def _beim_eigene(self) -> None:
        if hasattr(self.tab_store, "beim_zeigen"):
            self.tab_store.beim_zeigen()
        if hasattr(self.tab_store, "refresh_saved_packs"):
            self.tab_store.refresh_saved_packs()

    def _zustand_spiegeln(self) -> None:
        """Sperrt, was ohne Anmeldung oder Originalpaket sinnlos wäre.

        Die Einträge bleiben sichtbar - sie sollen ja verraten, dass es
        sie gibt. Wer darauf klickt, erfährt, woran es liegt.
        """
        verbunden = self.state_obj.connected
        basis = self.state_obj.has_base_pack

        self.shell.set_dot("verbindung", "ok" if verbunden else "warn")

        ohne_anmeldung = t("app.disabled_hint_no_login")
        ohne_basis = t("app.disabled_hint_no_basepack")

        for key in ("stimme", "eigene", "ansagen", "aufspielen"):
            self.shell.set_enabled(key, verbunden and basis,
                                   ohne_anmeldung if not verbunden else ohne_basis)

    def _toggle_theme(self) -> None:
        messagebox.showinfo(
            t("app.theme_switch_title"),
            t("app.theme_switch_body"),
            parent=self)
        self.state_obj.config["dark_mode"] = self.var_dark.get()
        self.state_obj.save()

    def _toggle_language(self, _event=None) -> None:
        messagebox.showinfo(
            "Switch language",
            "The new language takes effect the next time the app starts.\n\n"
            "Switching it live would rebuild every view and lose any "
            "unsaved input.",
            parent=self)
        self.state_obj.config["ui_language"] = (
            "de" if self.var_language.get() == "Deutsch" else "en")
        self.state_obj.save()

    # ------------------------------------------------------------------
    def _show_about(self) -> None:
        """Lizenz, Haftungsausschluss und - falls hinterlegt - die Links."""
        window = tk.Toplevel(self)
        window.title(t("app.about_window_title", app_name=APP_NAME))
        window.configure(bg=self.theme.color("bg"))
        window.geometry("640x440")
        window.transient(self)

        card = Card(window, self.theme, f"{APP_NAME} {__version__}",
                    t("app.about_subtitle", autor=AUTOR, lizenz=LIZENZ))
        card.pack(fill="both", expand=True, padx=16, pady=16)

        # Text und Bildlaufleiste nebeneinander in einem eigenen Rahmen.
        # Vorher war der Text mit side="top" und expand=True gepackt - er
        # nahm damit die ganze Fläche, und für die Leiste blieb unten
        # rechts ein sinnloser Stummel übrig.
        feld = ttk.Frame(card.content, style="Card.TFrame")
        feld.pack(fill="both", expand=True)

        text = tk.Text(feld, wrap="word", relief="flat", borderwidth=0,
                       background=self.theme.color("surface"),
                       foreground=self.theme.color("text"),
                       highlightthickness=0,
                       font=self.theme.font_body, padx=4, pady=4, height=14)
        scroll = ttk.Scrollbar(feld, orient="vertical", command=text.yview)
        text.pack(side="left", fill="both", expand=True)

        # Die Leiste erscheint nur, wenn der Text wirklich länger ist als
        # das Fenster. Beim Haftungstext ist er das meistens nicht.
        def leiste_zeigen(erster: str, letzter: str) -> None:
            noetig = not (float(erster) <= 0.0 and float(letzter) >= 1.0)
            if noetig and not scroll.winfo_ismapped():
                scroll.pack(side="right", fill="y")
            elif not noetig and scroll.winfo_ismapped():
                scroll.pack_forget()
            scroll.set(erster, letzter)

        text.configure(yscrollcommand=leiste_zeigen)
        text.insert("1.0", HAFTUNG)
        text.configure(state="disabled")

        unten = ttk.Frame(window, style="TFrame")
        unten.pack(fill="x", padx=16, pady=(0, 16))

        knoepfe = ttk.Frame(unten, style="TFrame")
        knoepfe.pack(fill="x")

        if PROJEKT_URL:
            ttk.Button(knoepfe, text=t("app.open_project_button"),
                       command=lambda: webbrowser.open(PROJEKT_URL)
                       ).pack(side="left")
        if SPENDEN_URL:
            ttk.Button(
                knoepfe, text=t("app.leave_tip_button"),
                command=lambda: webbrowser.open(SPENDEN_URL)
            ).pack(side="left", padx=(8, 0))

        ttk.Button(knoepfe, text=t("app.about_close_button"), style="Accent.TButton",
                   command=window.destroy).pack(side="right")

        # Der Hinweis steht unter den Knöpfen, nicht daneben: dazwischen
        # gequetscht brach er mitten im Satz um.
        if SPENDEN_URL:
            ttk.Label(unten,
                      text=t("app.tip_note"),
                      style="MutedBg.TLabel").pack(anchor="w", pady=(10, 0))

    # ------------------------------------------------------------------
    def _datenordner_oeffnen(self) -> None:
        """Öffnet den Datenordner im Explorer.

        Schlägt das fehl - kein Explorer, gesperrter Ordner -, wird der
        Pfad wenigstens genannt, statt dass der Knopf stumm bleibt.
        """
        ordner = data_dir()
        try:
            if sys.platform == "win32":
                os.startfile(str(ordner))              # noqa: S606
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(ordner)])
            else:
                subprocess.Popen(["xdg-open", str(ordner)])
        except OSError as exc:
            _LOG.warning("Datenordner ließ sich nicht öffnen: %s", exc)
            show_warning(self, self.theme, t("app.folder_not_opened_title"),
                         t("app.folder_not_opened_message"),
                         t("app.folder_not_opened_hint", path=ordner))

    # ------------------------------------------------------------------
    def _show_update(self, neuerung=None):
        """Öffnet das Aktualisierungsfenster - höchstens eines davon.

        Ein zweites Fenster daneben hätte zwei Schalter für dieselbe
        Einstellung und zwei Knöpfe, die denselben Download starten.
        """
        offen = getattr(self, "_fenster_update", None)
        if offen is not None and offen.winfo_exists():
            offen.deiconify()
            offen.lift()
            offen.focus_force()
        else:
            offen = UpdateFenster(self, self.theme, self.state_obj)
            self._fenster_update = offen
        if neuerung is not None:
            spaeter(offen, 120, lambda: offen.anbieten(neuerung))
        return offen

    # ------------------------------------------------------------------
    def _show_help(self) -> None:
        window = tk.Toplevel(self)
        window.title(t("app.help_window_title"))
        window.configure(bg=self.theme.color("bg"))
        window.geometry("760x740")
        window.minsize(560, 420)
        window.transient(self)

        # Von unten nach oben packen: Der Knopf zum Schließen und die
        # Anleitungen bekommen ihren Platz zuerst, der lange Text nimmt
        # den Rest. Andersherum schob er beide aus dem Fenster - auf
        # einem kleineren Bildschirm war das Fenster dann ohne
        # sichtbaren Ausgang.
        ttk.Button(window, text=t("app.help_close_button"), style="Accent.TButton",
                   command=window.destroy).pack(side="bottom", pady=(0, 16))
        self._bau_anleitungen(window)

        card = Card(window, self.theme, t("app.how_it_works_title"))
        card.pack(fill="both", expand=True, padx=16, pady=16)

        text = tk.Text(card.content, wrap="word", relief="flat", borderwidth=0,
                       background=self.theme.color("surface"),
                       foreground=self.theme.color("text"),
                       font=self.theme.font_body, padx=4, pady=4)
        scroll = ttk.Scrollbar(card.content, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        text.insert("1.0", t("app.help_text"))
        text.configure(state="disabled")

    # ------------------------------------------------------------------
    def _bau_anleitungen(self, fenster) -> None:
        """Die ausführlichen Anleitungen als Knöpfe darunter.

        Ohne diese Liste war `docs/` aus der App heraus unsichtbar - wer
        nur die EXE hat, konnte nicht ahnen, dass es zu jedem Thema noch
        mehrere Seiten gibt. Der Knopf sagt vorher, was er tut: Datei
        oder Browser, je nachdem, was wirklich da ist.
        """
        karte = Card(fenster, self.theme, t("app.guides_card_title"))
        karte.pack(side="bottom", fill="x", padx=16, pady=(0, 12))
        inhalt = karte.content

        art = {a.datei: anleitungen.verfuegbar(a.datei)
               for a in anleitungen.ANLEITUNGEN}
        online = [d for d, w in art.items() if w == "netz"]
        fehlt = [d for d, w in art.items() if w == "nein"]

        if fehlt and len(fehlt) == len(art):
            # Weder Dateien noch eine Projektadresse: dann lieber ein
            # ehrlicher Satz als sechs Knöpfe, die nichts tun.
            ttk.Label(inhalt, style="Muted.TLabel", justify="left",
                      wraplength=660,
                      text=t("app.guides_missing_note")).pack(anchor="w")
            return

        ttk.Label(inhalt, style="Muted.TLabel", justify="left", wraplength=660,
                  text=(t("app.guides_open_browser")
                        if online and len(online) == len(art)
                        else t("app.guides_open_textfile"))
                  ).pack(anchor="w", pady=(0, 8))

        # Raster statt nebeneinander gepackter Zeilen: Sonst beginnt
        # jede Erklärung an einer anderen Stelle, weil die Knöpfe
        # unterschiedlich breit sind - das las sich wie ein Zaun.
        gitter = ttk.Frame(inhalt, style="Card.TFrame")
        gitter.pack(fill="x")
        gitter.columnconfigure(1, weight=1)
        reihe = 0
        for eintrag in anleitungen.ANLEITUNGEN:
            if art[eintrag.datei] == "nein":
                continue
            ttk.Button(gitter, text=eintrag.titel, style="Link.TButton",
                       command=lambda d=eintrag.datei: self._zeige_anleitung(d)
                       ).grid(row=reihe, column=0, sticky="w", pady=1)
            ttk.Label(gitter, text=eintrag.inhalt, style="Muted.TLabel",
                      wraplength=420, justify="left").grid(
                row=reihe, column=1, sticky="w", padx=(14, 0), pady=1)
            reihe += 1

    # ------------------------------------------------------------------
    def _zeige_anleitung(self, datei: str) -> None:
        """Anleitung öffnen und Bescheid geben, wenn es nicht klappt."""
        if anleitungen.oeffnen(datei) != "nein":
            return
        show_warning(
            self, self.theme, t("app.guide_not_reachable_title"),
            t("app.guide_not_reachable_message", file=datei),
            t("app.guide_not_reachable_hint"))

    # ------------------------------------------------------------------
    def _on_unhandled(self, art, wert, spur) -> None:
        """Zeigt Fehler, die sonst spurlos verschwinden würden.

        Tkinter fängt Ausnahmen aus Schaltflächen ab und schreibt sie
        bestenfalls auf die Konsole - bei einer Fensteranwendung sieht die
        niemand. Für den Benutzer sieht es dann so aus, als täte der Knopf
        einfach nichts. Deshalb landet hier alles Unerwartete sichtbar auf
        dem Bildschirm und zusätzlich im Protokoll.
        """
        text = "".join(traceback.format_exception(art, wert, spur))
        _LOG.error("Unbehandelter Fehler in der Oberfläche:\n%s", text)
        try:
            show_error(
                self, self.theme, t("app.unexpected_error_title"),
                f"{art.__name__}: {wert}",
                t("app.unexpected_error_hint") + text)
        except Exception:      # pragma: no cover - Notnagel
            pass

    # ------------------------------------------------------------------
    def _on_close(self) -> None:
        try:
            self.state_obj.save()
        except Exception:  # pragma: no cover
            _LOG.exception("Konfiguration konnte beim Beenden nicht gespeichert werden")
        self.destroy()


HELP_TEXT = t("app.help_text")


def run() -> None:
    """Startet die Anwendung."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_file(), encoding="utf-8")],
    )
    _LOG.info("Start %s %s", APP_NAME, __version__)

    window = MainWindow()
    window.mainloop()
