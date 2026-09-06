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

        self.title("Updates")
        self.configure(bg=theme.color("bg"))
        self.geometry("660x520")
        self.minsize(520, 420)
        self.transient(master)

        # Knopf zum Schließen zuerst, damit ihn ein langer Text nicht
        # aus dem Fenster schiebt.
        ttk.Button(self, text="Close", style="Accent.TButton",
                   command=self.destroy).pack(side="bottom", pady=(0, 14))

        karte = Card(self, theme, "Updates",
                     "Check whether a newer version is available")
        karte.pack(fill="both", expand=True, padx=16, pady=16)
        inhalt = karte.content

        ttk.Label(
            inhalt,
            text=(f"This version: {__version__}\n\n"
                  "The app asks GitHub for the latest version. This doesn't "
                  "transmit anything about you or your robot - but as with "
                  "any page request, the other side sees your IP address. "
                  "That's why the check is off until you turn it on."),
            style="Surface.TLabel", wraplength=580, justify="left").pack(anchor="w")

        self.var_update = tk.BooleanVar(
            value=bool(state.config["update_pruefen"]))
        ttk.Checkbutton(inhalt, style="Haken.TCheckbutton",
                        text="Check for a newer version on startup",
                        variable=self.var_update,
                        command=self._on_schalter).pack(anchor="w", pady=(12, 0))

        reihe = ttk.Frame(inhalt, style="Card.TFrame")
        reihe.pack(fill="x", pady=(12, 0))
        self.btn_update = ttk.Button(reihe, text="Check for Updates Now",
                                     command=self._on_suchen)
        self.btn_update.pack(side="left")
        self.lbl_update = ttk.Label(reihe, text="", style="Muted.TLabel",
                                    wraplength=380, justify="left")
        self.lbl_update.pack(side="left", padx=(12, 0))

        ttk.Label(
            inhalt,
            text=("Nothing found gets installed automatically. The app shows "
                  "what's new and asks first. Only then does it download the "
                  "new file, verify its checksum, and replace itself - no "
                  "installer, no admin rights needed. Your data folder stays "
                  "untouched."),
            style="Muted.TLabel", wraplength=580, justify="left"
        ).pack(anchor="w", pady=(14, 0))

    # ------------------------------------------------------------------
    def _on_schalter(self) -> None:
        self.state.config["update_pruefen"] = bool(self.var_update.get())
        self.state.save()

    def _on_suchen(self) -> None:
        """Von Hand nachsehen. Hier wird auch ein Fehler gezeigt."""
        self.btn_update.configure(state="disabled")
        self.lbl_update.configure(text="Checking ...")

        def work(_task):
            return aktualisierung.pruefen()

        def ok(neuerung) -> None:
            self.state.config["update_zuletzt"] = aktualisierung.jetzt()
            self.state.save()
            if neuerung is None:
                self.lbl_update.configure(
                    text=f"{__version__} is the latest version.")
                return
            self.lbl_update.configure(text=f"Version {neuerung.version} is available.")
            self.anbieten(neuerung)

        def fail(exc: Exception) -> None:
            nachricht, hinweis = error_text(exc)
            self.lbl_update.configure(text=nachricht)
            show_error(self, self.theme, "Check Failed", nachricht, hinweis)

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
            show_info(self, self.theme, f"Version {neuerung.version} is available",
                      "This app is running from source - replacing the "
                      "program file doesn't make sense here.",
                      f"Get the new version via git.\n\n{notizen}")
            return

        if not neuerung.pruefbar:
            show_warning(self, self.theme, f"Version {neuerung.version} is available",
                         "No checksum is available for this version.",
                         "Without one, nothing gets replaced - writing over "
                         "the program file unverified would be exactly the "
                         "opening an attacker shouldn't be given.\n\n"
                         f"Download it from the project page:\n{neuerung.seite}")
            return

        if not aktualisierung.ordner_beschreibbar(exe):
            show_warning(self, self.theme, f"Version {neuerung.version} is available",
                         "The app isn't allowed to write in this folder.",
                         "So it can't replace itself here. Move it to a "
                         "folder of your own - the desktop, say - or "
                         "download the new version from the project "
                         f"page:\n{neuerung.seite}")
            return

        if not messagebox.askyesno(
                f"Version {neuerung.version} is available",
                f"You have {__version__}, {neuerung.version} "
                f"({neuerung.groesse_mb:.0f} MB) is new.\n\n"
                f"The app downloads the new file, verifies its checksum, "
                f"and sets itself aside. It then restarts. Your data "
                f"folder and packages stay untouched.\n\n"
                + (f"What's new:\n{notizen}\n\n" if notizen else "")
                + "Update now?",
                parent=self):
            return

        self._holen(neuerung)

    def _holen(self, neuerung) -> None:
        self.btn_update.configure(state="disabled")
        self.lbl_update.configure(text="Downloading ...")

        def melde(geladen: int, gesamt: int) -> None:
            if not gesamt:
                return
            text = f"Downloading ... {geladen * 100 // gesamt} %"
            to_main(self, lambda t=text: self.lbl_update.configure(text=t))

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
            self.lbl_update.configure(text=f"Version {neuerung.version} is ready.")
            if messagebox.askyesno(
                    "Done",
                    f"Version {neuerung.version} has been installed.\n\n"
                    f"Restart now? The old version will be cleaned up on "
                    f"the next start.",
                    parent=self):
                if aktualisierung.neu_starten():
                    haupt = self.master.winfo_toplevel()
                    spaeter(haupt, 200, haupt.destroy)
                else:
                    show_warning(self, self.theme, "Restart",
                                 "The new version couldn't be started.",
                                 "Close the app and start it manually.")

        def fail(exc: Exception) -> None:
            nachricht, hinweis = error_text(exc)
            self.lbl_update.configure(text=nachricht)
            # Im Notstand liegt tatsächlich keine startfähige Datei mehr
            # am Platz. "Es wurde nichts ausgetauscht" wäre dann das
            # Gegenteil der Wahrheit - und zwar genau in dem Moment, in
            # dem der Benutzer wissen muss, was zu tun ist.
            if isinstance(exc, aktualisierung.TauschNotstand):
                show_error(self, self.theme, "Manual Action Needed",
                           nachricht, hinweis)
                return
            show_error(self, self.theme, "Not Updated", nachricht,
                       (hinweis + "\n\n" if hinweis else "")
                       + f"Nothing was replaced. The file is still "
                         f"waiting on the project page:\n"
                         f"{neuerung.seite}")

        run_async(self, work, on_success=ok, on_error=fail,
                  on_finally=lambda: self.btn_update.configure(state="normal"))
