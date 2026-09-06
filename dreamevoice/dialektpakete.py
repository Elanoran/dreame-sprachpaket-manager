"""Die fertig gesprochenen Dialekte bereitstellen.

Bisher war das ein Weg über vier Stationen: auf die Projektseite gehen,
das ZIP herunterladen, im Explorer wiederfinden, in der App einlesen.
Für jemanden, der einfach nur einen bayerisch sprechenden Roboter will,
sind das drei Stationen zu viel.

Deshalb sind die Aufnahmen **in der EXE mit dabei** (siehe embedded.py)
und werden beim ersten Bedarf ausgepackt. Kein Download, kein Explorer,
und vor allem: keine Abhängigkeit davon, dass ein Release im Netz steht.

Das Herunterladen aus dem Release gibt es weiterhin - aber nur noch als
freiwilliges Update, wenn jemand eine neuere Fassung möchte als die, mit
der seine EXE gebaut wurde.

Warum Aufnahmen und kein fertiges Paket: Ein fertiges Sprachpaket
enthält immer die Steuerdateien genau eines Modells. Die Aufnahmen
dagegen passen auf jedes Modell - gebaut wird daraus erst auf dem
Rechner des Benutzers, mit den Steuerdateien seines eigenen Roboters.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

import requests

from . import PROJEKT_URL, embedded
from .errors import NetworkError, PackError
from .paths import data_dir

_LOG = logging.getLogger(__name__)

ProgressFn = Callable[[int, int], None]

ORDNER = "Geladene Dialekte"

# Zu klein, um eine Sammlung von Ansagen zu sein - dann ist etwas
# schiefgelaufen (Fehlerseite, abgebrochener Download).
MINDESTGROESSE = 1_000_000


class Abgebrochen(Exception):
    """Der Benutzer hat den Download abgebrochen.

    Bewusst keine Unterklasse von DreameError: ein Abbruch ist kein
    Fehler und soll dem Benutzer nicht als solcher gezeigt werden.
    """


@dataclass(frozen=True)
class FertigerDialekt:
    """Ein Satz fertig gesprochener Ansagen von der Projektseite."""

    key: str
    name: str
    datei: str
    ansagen: int
    stimme: str
    beschreibung: str
    #: "male" or "female". Shown in the display name, because it's the
    #: first thing you pick by - it used to sit small in a trailing
    #: parenthesis and got overlooked.
    geschlecht: str = "male"

    @property
    def url(self) -> str:
        basis = (PROJEKT_URL or "").rstrip("/")
        if not basis:
            return ""
        return f"{basis}/releases/latest/download/{self.datei}"

    @property
    def local_path(self) -> Path:
        return ordner() / self.datei

    @property
    def anzeigename(self) -> str:
        """Name mit Geschlecht, so wie er in der Liste steht."""
        return f"{self.name} ({self.geschlecht})"

    @property
    def label(self) -> str:
        return f"{self.anzeigename}  ({self.ansagen} announcements, {self.stimme})"


# Die Stimmen, für die es fertige Aufnahmen gibt - vier Dialekte, davon
# Bayerisch in zwei Stimmen. Die übrigen drei Dialekte (Schwäbisch,
# Sächsisch, Kölsch) stecken als Texte im Programm und werden unter
# "Eigene Stimmen" selbst erzeugt.
KATALOG: List[FertigerDialekt] = [
    FertigerDialekt(
        key="bayerisch", name="Bavarian",
        datei="Bayerisch-Aufnahmen.zip", ansagen=593,
        stimme="ElevenLabs",
        beschreibung="Upper Bavarian, as spoken around Munich."),
    FertigerDialekt(
        key="bayerisch-weiblich", name="Bavarian",
        datei="Bayerisch-Weiblich-Aufnahmen.zip", ansagen=598,
        stimme="ElevenLabs", geschlecht="female",
        beschreibung="Upper Bavarian, as spoken around Munich."),
    FertigerDialekt(
        key="hessisch", name="Hessian",
        datei="Hessisch-Aufnahmen.zip", ansagen=593,
        stimme="ElevenLabs",
        beschreibung="Frankfurt-style Hessian from the Rhine-Main area."),
    FertigerDialekt(
        key="wienerisch", name="Viennese",
        datei="Wienerisch-Aufnahmen.zip", ansagen=593,
        stimme="ElevenLabs",
        beschreibung="Viennese vernacular, not stage dialect."),
    FertigerDialekt(
        key="berlinerisch", name="Berlin Dialect",
        datei="Berlinerisch-Aufnahmen.zip", ansagen=593,
        stimme="ElevenLabs",
        beschreibung="Berlin's Schnauze, with the hard j instead of g."),
]


def ordner() -> Path:
    ziel = data_dir() / ORDNER
    ziel.mkdir(parents=True, exist_ok=True)
    return ziel


def get(key: str) -> Optional[FertigerDialekt]:
    for eintrag in KATALOG:
        if eintrag.key == key:
            return eintrag
    return None


def bereits_geladen(eintrag: FertigerDialekt) -> Optional[Path]:
    """Der Pfad, wenn eine heruntergeladene Fassung schon hier liegt."""
    pfad = eintrag.local_path
    try:
        if pfad.is_file() and pfad.stat().st_size >= MINDESTGROESSE:
            return pfad
    except OSError:
        pass
    return None


# -- Woher die Aufnahmen kommen -------------------------------------------

QUELLE_GELADEN = "geladen"
QUELLE_MITGELIEFERT = "mitgeliefert"
QUELLE_PROJEKTORDNER = "Projektordner"
QUELLE_FEHLT = "fehlt"

#: Wo die Archive liegen, wenn aus dem Quellcode statt aus der EXE
#: gestartet wird. Angehängt ist dann nichts - die Aufnahmen liegen aber
#: im Projektordner, und ohne das hier stünde ein Entwickler vor einer
#: Auswahl ohne einen einzigen Eintrag.
PROJEKT_UNTERORDNER = "Fertige Pakete"


def im_projektordner(eintrag: FertigerDialekt) -> Optional[Path]:
    if embedded.is_frozen():
        return None
    pfad = Path(__file__).resolve().parent.parent / PROJEKT_UNTERORDNER \
        / eintrag.datei
    try:
        if pfad.is_file() and pfad.stat().st_size >= MINDESTGROESSE:
            return pfad
    except OSError:
        pass
    return None


def quelle(eintrag: FertigerDialekt) -> str:
    """Woher dieser Dialekt gerade käme, ohne etwas zu tun."""
    if bereits_geladen(eintrag) is not None:
        return QUELLE_GELADEN
    if eintrag.datei in embedded.list_dialekte():
        return QUELLE_MITGELIEFERT
    if im_projektordner(eintrag) is not None:
        return QUELLE_PROJEKTORDNER
    return QUELLE_FEHLT


def verfuegbar() -> List[FertigerDialekt]:
    """Alle Dialekte, die sich ohne Internet bereitstellen lassen."""
    return [e for e in KATALOG if quelle(e) != QUELLE_FEHLT]


def beschaffen(eintrag: FertigerDialekt,
               log: Optional[Callable[[str], None]] = None) -> Optional[Path]:
    """Der Pfad zu den Aufnahmen - ohne Netz, wenn irgend möglich.

    Eine heruntergeladene Fassung hat Vorrang: Wer sich bewusst ein
    Update geholt hat, will nicht wieder den Stand aus der EXE.
    """
    geladen = bereits_geladen(eintrag)
    if geladen is not None:
        if log:
            log(f"{eintrag.name}: using the downloaded version.")
        return geladen

    ausgepackt = embedded.extract_dialekt(eintrag.datei, log=log)
    if ausgepackt is not None:
        return ausgepackt

    aus_projekt = im_projektordner(eintrag)
    if aus_projekt is not None:
        if log:
            log(f"{eintrag.name}: from the project folder.")
        return aus_projekt

    if log:
        log(f"{eintrag.name} is neither bundled nor downloaded.")
    return None


def download(eintrag: FertigerDialekt,
             progress: Optional[ProgressFn] = None,
             cancelled: Optional[Callable[[], bool]] = None,
             force: bool = False) -> Path:
    """Holt die Aufnahmen; ein bereits geladenes ZIP wird wiederverwendet."""
    cancelled = cancelled or (lambda: False)

    if not force:
        vorhanden = bereits_geladen(eintrag)
        if vorhanden is not None:
            if progress:
                progress(1, 1)
            _LOG.info("%s liegt schon vor", eintrag.datei)
            return vorhanden

    if not eintrag.url:
        raise PackError(
            "No project address is configured.",
            "Without it, the app doesn't know where to get the recordings from.")

    ziel = eintrag.local_path
    tmp = ziel.with_suffix(ziel.suffix + ".part")
    tmp.unlink(missing_ok=True)

    try:
        with requests.get(eintrag.url, stream=True, timeout=90,
                          headers={"User-Agent": "DreameSprachpakete/1.0"}) as resp:
            if resp.status_code != 200:
                raise NetworkError(
                    f"{eintrag.name} couldn't be downloaded "
                    f"(HTTP {resp.status_code}).",
                    f"Source: {eintrag.url}\n\nThere may not be a release "
                    f"with this file yet, or the internet connection isn't "
                    f"working.")
            gesamt = int(resp.headers.get("Content-Length") or 0)
            fertig = 0
            with tmp.open("wb") as fh:
                for block in resp.iter_content(chunk_size=1 << 16):
                    if cancelled():
                        raise Abgebrochen()
                    if not block:
                        continue
                    fh.write(block)
                    fertig += len(block)
                    if progress:
                        progress(fertig, gesamt)
    except Abgebrochen:
        tmp.unlink(missing_ok=True)
        raise
    except requests.exceptions.RequestException as exc:
        tmp.unlink(missing_ok=True)
        raise NetworkError(
            f"{eintrag.name} couldn't be downloaded.",
            f"Technical details: {exc}") from exc

    # Eine Fehlerseite statt eines Archivs fällt hier auf, bevor sie
    # als Sprachpaket missverstanden wird.
    if tmp.stat().st_size < MINDESTGROESSE:
        groesse = tmp.stat().st_size
        tmp.unlink(missing_ok=True)
        raise PackError(
            f"The downloaded file is too small ({groesse} bytes).",
            "Several megabytes of spoken announcements were expected. "
            "The server probably sent an error page instead of the "
            "file.")

    tmp.replace(ziel)
    _LOG.info("%s geladen (%d Bytes)", eintrag.datei, ziel.stat().st_size)
    return ziel
