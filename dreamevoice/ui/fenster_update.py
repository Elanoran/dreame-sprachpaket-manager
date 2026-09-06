"""Das Fenster für Aktualisierungen.

Bis hierher steckte das alles auf der Seite "Verbindung" - unter dem
Konto und der Roboterliste, wo es niemand vermutet. Aktualisieren hat
mit der Verbindung zum Roboter aber nichts zu tun; es betrifft die App
selbst. Deshalb ein eigenes Fenster, erreichbar über den Knopf oben
rechts, direkt neben "Hilfe" und "Über".

Der Schalter "beim Start nachsehen" steht mit im Fenster: Wer wissen
will, ob automatisch geprüft wird, sucht genau da - und nicht in einer
Seite, die er sonst nie öffnet.

Warum ausgeschaltet, bis jemand es einschaltet: Die Abfrage geht an
GitHub und verrät dadurch, dass hier jemand diese App benutzt. Das
gehört gefragt, nicht angenommen.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .. import __version__, aktualisierung
from ..i18n import t
from .state import AppState, error_text, run_async, spaeter, to_main
from .theme import Theme
from .widgets import Card, show_error, show_info, show_warning


class UpdateFenster(tk.Toplevel):
    """Nachsehen, was es Neues gibt - und die App sich selbst ersetzen lassen.

    Das Fenster hält die ganze Kette: nachfragen, anbieten, laden,
    Prüfsumme kontrollieren, austauschen, neu starten. Vorher lag sie
    in `tab_connect`; von dort aus ließ sie sich nur erreichen, wenn
    diese Seite gebaut war.
    """

    def __init__(self, master, theme: Theme, state: AppState) -> None:
        super().__init__(master)
        self.theme = theme
        self.state = state

        self.title(t("fenster_update.window_title"))
        self.configure(bg=theme.color("bg"))
        self.geometry("660x520")
        self.minsize(520, 420)
        self.transient(master)

        # Knopf zum Schließen zuerst, damit ihn ein langer Text nicht
        # aus dem Fenster schiebt.
        ttk.Button(self, text=t("fenster_update.close_button"), style="Accent.TButton",
                   command=self.destroy).pack(side="bottom", pady=(0, 14))

        karte = Card(self, theme, t("fenster_update.card_title"),
                     t("fenster_update.card_subtitle"))
        karte.pack(fill="both", expand=True, padx=16, pady=16)
        inhalt = karte.content

        ttk.Label(
            inhalt,
            text=t("fenster_update.version_info", version=__version__),
            style="Surface.TLabel", wraplength=580, justify="left").pack(anchor="w")

        self.var_update = tk.BooleanVar(
            value=bool(state.config["update_pruefen"]))
        ttk.Checkbutton(inhalt, style="Haken.TCheckbutton",
                        text=t("fenster_update.checkbox_startup"),
                        variable=self.var_update,
                        command=self._on_schalter).pack(anchor="w", pady=(12, 0))

        reihe = ttk.Frame(inhalt, style="Card.TFrame")
        reihe.pack(fill="x", pady=(12, 0))
        self.btn_update = ttk.Button(reihe, text=t("fenster_update.check_now_button"),
                                     command=self._on_suchen)
        self.btn_update.pack(side="left")
        self.lbl_update = ttk.Label(reihe, text="", style="Muted.TLabel",
                                    wraplength=380, justify="left")
        self.lbl_update.pack(side="left", padx=(12, 0))

        ttk.Label(
            inhalt,
            text=t("fenster_update.auto_install_note"),
            style="Muted.TLabel", wraplength=580, justify="left"
        ).pack(anchor="w", pady=(14, 0))

    # ------------------------------------------------------------------
    def _on_schalter(self) -> None:
        self.state.config["update_pruefen"] = bool(self.var_update.get())
        self.state.save()

    def _on_suchen(self) -> None:
        """Von Hand nachsehen. Hier wird auch ein Fehler gezeigt."""
        self.btn_update.configure(state="disabled")
        self.lbl_update.configure(text=t("fenster_update.status_checking"))

        def work(_task):
            return aktualisierung.pruefen()

        def ok(neuerung) -> None:
            self.state.config["update_zuletzt"] = aktualisierung.jetzt()
            self.state.save()
            if neuerung is None:
                self.lbl_update.configure(
                    text=t("fenster_update.status_latest", version=__version__))
                return
            self.lbl_update.configure(
                text=t("fenster_update.status_version_available",
                      version=neuerung.version))
            self.anbieten(neuerung)

        def fail(exc: Exception) -> None:
            nachricht, hinweis = error_text(exc)
            self.lbl_update.configure(text=nachricht)
            show_error(self, self.theme, t("fenster_update.check_failed_title"),
                      nachricht, hinweis)

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_update.configure(state="normal"))

    # ------------------------------------------------------------------
    def anbieten(self, neuerung) -> None:
        """Zeigt, was neu ist, und fragt - installiert wird nichts von selbst."""
        exe = aktualisierung.eigene_exe()
        notizen = (neuerung.notizen or "").strip()
        if len(notizen) > 900:
            notizen = notizen[:900].rsplit("\n", 1)[0] + "\n..."

        if exe is None:
            show_info(self, self.theme,
                      t("fenster_update.version_available_title",
                        version=neuerung.version),
                      t("fenster_update.source_run_message"),
                      t("fenster_update.source_run_hint", notes=notizen))
            return

        if not neuerung.pruefbar:
            show_warning(self, self.theme,
                         t("fenster_update.version_available_title",
                           version=neuerung.version),
                         t("fenster_update.no_checksum_message"),
                         t("fenster_update.no_checksum_hint",
                           url=neuerung.seite))
            return

        if not aktualisierung.ordner_beschreibbar(exe):
            show_warning(self, self.theme,
                         t("fenster_update.version_available_title",
                           version=neuerung.version),
                         t("fenster_update.folder_not_writable_message"),
                         t("fenster_update.folder_not_writable_hint",
                           url=neuerung.seite))
            return

        if not messagebox.askyesno(
                t("fenster_update.version_available_title",
                  version=neuerung.version),
                t("fenster_update.confirm_update_body",
                  current=__version__, new=neuerung.version,
                  size=f"{neuerung.groesse_mb:.0f}")
                + (t("fenster_update.whats_new_segment", notes=notizen)
                   if notizen else "")
                + t("fenster_update.update_now_question"),
                parent=self):
            return

        self._holen(neuerung)

    def _holen(self, neuerung) -> None:
        self.btn_update.configure(state="disabled")
        self.lbl_update.configure(text=t("fenster_update.status_downloading"))

        def melde(geladen: int, gesamt: int) -> None:
            if not gesamt:
                return
            text = t("fenster_update.status_downloading_progress",
                     percent=geladen * 100 // gesamt)
            to_main(self, lambda txt=text: self.lbl_update.configure(text=txt))

        def work(task):
            neu = aktualisierung.herunterladen(
                neuerung, progress=melde, cancelled=lambda: task.cancelled)
            # Erst tauschen, wenn die Datei vollständig und geprüft ist.
            # Die Prüfsumme wird unmittelbar vor dem Tausch noch einmal
            # geprüft - zwischen Download und Umbenennen liegt sonst ein
            # Zeitfenster, in dem jemand die Datei austauschen könnte.
            aktualisierung.austauschen(neu, erwartet_sha256=neuerung.sha256)
            return True

        def ok(_ergebnis) -> None:
            self.lbl_update.configure(
                text=t("fenster_update.status_ready", version=neuerung.version))
            if messagebox.askyesno(
                    t("fenster_update.done_title"),
                    t("fenster_update.done_body", version=neuerung.version),
                    parent=self):
                if aktualisierung.neu_starten():
                    haupt = self.master.winfo_toplevel()
                    spaeter(haupt, 200, haupt.destroy)
                else:
                    show_warning(self, self.theme, t("fenster_update.restart_title"),
                                 t("fenster_update.restart_message"),
                                 t("fenster_update.restart_hint"))

        def fail(exc: Exception) -> None:
            nachricht, hinweis = error_text(exc)
            self.lbl_update.configure(text=nachricht)
            # Im Notstand liegt tatsächlich keine startfähige Datei mehr
            # am Platz. "Es wurde nichts ausgetauscht" wäre dann das
            # Gegenteil der Wahrheit - und zwar genau in dem Moment, in
            # dem der Benutzer wissen muss, was zu tun ist.
            if isinstance(exc, aktualisierung.TauschNotstand):
                show_error(self, self.theme, t("fenster_update.manual_action_title"),
                           nachricht, hinweis)
                return
            show_error(self, self.theme, t("fenster_update.not_updated_title"),
                       nachricht,
                       (hinweis + "\n\n" if hinweis else "")
                       + t("fenster_update.not_updated_hint", url=neuerung.seite))

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_update.configure(state="normal"))
