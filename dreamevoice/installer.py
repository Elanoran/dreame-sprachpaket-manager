"""Der eigentliche Installationsablauf.

Reihenfolge:

1. Webserver starten, der genau das gebaute Paket ausliefert.
2. Über die Dreame-Cloud den Auftrag an den Roboter schicken
   (MIoT-Eigenschaft 7/4) - mit URL, MD5 und Größe.
3. Warten, bis der Roboter die Datei tatsächlich abholt.
4. Den Installationszustand abfragen, bis er fertig meldet.
5. Webserver in jedem Fall wieder schließen.

Der Roboter prüft das Archiv selbst gegen MD5 und Größe. Stimmt etwas
nicht, verwirft er es und behält die bisherige Stimme - genau das macht
den Vorgang unkritisch.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from .cloud import DreameCloud, Device
from .errors import InstallError, LoginError, NetworkError
from .official import VoicePackInfo
from .packer import BuildResult
from .server import PackServer, reachability_hint

_LOG = logging.getLogger(__name__)

LogFn = Callable[[str], None]
StepFn = Callable[[str, float], None]   # (Beschreibung, Fortschritt 0..1)

# Kennungen, die Dreame selbst vergibt. Wer eine davon überschreibt,
# verliert die Möglichkeit, per Knopfdruck dorthin zurückzukehren.
OFFICIAL_LANG_IDS = {
    "ZH", "EN", "DE", "RU", "FR", "KO", "ES", "IT", "JA", "PL",
    "TR", "SV", "DA", "NB", "PT", "THA", "VI", "UK", "HE",
}
DEFAULT_CUSTOM_LANG_ID = "CUSTOM"

#: Abstand zwischen zwei Blicken auf den Roboter, in Sekunden.
#:
#: Der Zustand durchläuft beim Wechsel kurz "downloading" und kehrt
#: danach auf "success" zurück. Genau diese Bewegung ist der Beweis,
#: dass gerade etwas passiert ist - wer zu selten hinsieht, verpasst
#: sie und wartet anschließend ergebnislos die volle Frist ab.
TAKT = 3.0


def _status_lesen(roh: Any) -> Optional[dict]:
    """Macht aus der Zustandsmeldung des Roboters ein Wörterbuch.

    Der Roboter liefert dort JSON - allerdings mit maskierten
    Anführungszeichen, also `{\\"id\\":\\"CUSTOM\\", ...}`. Das ist kein
    gültiges JSON, deshalb der zweite Versuch.
    """
    if isinstance(roh, dict):
        return roh
    if not isinstance(roh, str) or not roh.strip():
        return None
    for text in (roh, roh.replace('\\"', '"')):
        try:
            wert = json.loads(text)
        except (ValueError, TypeError):
            continue
        if isinstance(wert, dict):
            return wert
    return None


def validate_lang_id(lang_id: str) -> tuple[str, str]:
    """Prüft die Paketkennung. Rückgabe: (bereinigt, Warnung oder "").

    Zurzeit ruft das niemand mehr auf: `install_pack` setzt die Kennung
    fest auf CUSTOM, damit sich auf dem Roboter keine unlöschbaren
    Ordner ansammeln. Die Funktion bleibt samt Tests stehen, weil sie
    die Regeln festhält, die gelten *würden* - wer die Kennung je wieder
    freigibt, braucht genau diese Prüfung wieder. Wer sie entfernt,
    entfernt auch `OFFICIAL_LANG_IDS`.
    """
    cleaned = (lang_id or "").strip().upper()
    if not cleaned:
        return DEFAULT_CUSTOM_LANG_ID, ""
    if not cleaned.isalnum() or len(cleaned) > 8:
        raise InstallError(
            f"The pack identifier '{lang_id}' is invalid.",
            "Up to 8 letters or digits are allowed, e.g. CUSTOM or BAYERN.",
        )
    if cleaned in OFFICIAL_LANG_IDS:
        return cleaned, (
            f"'{cleaned}' is an official Dreame identifier. Your pack "
            f"overwrites the built-in language with it. To switch back, "
            f"you'll need to reinstall the original pack - this app can "
            f"do that, but a custom identifier like CUSTOM is more "
            f"convenient."
        )
    return cleaned, ""


@dataclass
class InstallOutcome:
    success: bool
    message: str
    downloaded: bool = False
    final_status: Optional[str] = None
    hint: str = ""
    #: Ob der Erfolg belegt ist oder nur wahrscheinlich.
    #:
    #: Der Unterschied darf nicht in der Oberfläche verlorengehen:
    #: Ein Download belegt die Übertragung, nicht die Installation.
    #: Verwirft der Roboter das Paket wegen der Prüfsumme und lässt
    #: seine alte Erfolgsmeldung stehen, sieht das von außen genauso
    #: aus wie ein geglückter Wechsel.
    bestaetigt: bool = True


def _noop_log(_: str) -> None:
    pass


def _noop_step(_msg: str, _p: float) -> None:
    pass


#: Ob beim Auffrischen ein Umweg über einen anderen Wert nötig ist.
#:
#: Bleibt aus. Ein Nutzer hat nach dem Paketwechsel über die
#: Dreamehome-App einen echten Wertwechsel geschrieben - er wollte
#: lauter stellen - und es blieb leise. Der Umweg wäre genau das, was
#: dort schon versagt hat, und er hinterlässt bei einem Abbruch
#: zwischen den beiden Schreibzugriffen dauerhaft den falschen Wert.
LAUTSTAERKE_UMWEG = False

#: Ob nach dem Schreiben der Testton ausgelöst wird (7/aiid 2).
#:
#: Die Referenz-Integration für Dreame-Sauger ruft die Aktion nach
#: jedem Schreiben der Lautstärke auf. Warum, steht dort nicht - am
#: naheliegendsten ist eine Rückmeldung für den Nutzer, damit er hört,
#: was er eingestellt hat. Dass die Firmware den Wert *dadurch* erst
#: übernimmt, wäre ein Rückschluss, für den es keinen Beleg gibt.
#:
#: Als Hörprobe wäre die Aktion sinnvoll. Sie bleibt trotzdem aus,
#: solange nicht am Gerät geprüft ist, dass sie beim r2532v wirklich
#: nur einen Ton abspielt.
LAUTSTAERKE_TESTTON = False


def refresh_volume(cloud: DreameCloud, device: Device, wert: Optional[int],
                   log: LogFn = _noop_log) -> bool:
    """Schreibt die gemerkte Lautstärke zurück, damit sie wieder greift.

    Schlägt fehl, ohne zu stören: Das Sprachpaket ist an dieser Stelle
    bereits installiert, und eine nicht wiederhergestellte Lautstärke ist
    ein Schönheitsfehler - kein Grund, den Vorgang als gescheitert zu
    melden.
    """
    if wert is None:
        return False
    try:
        if LAUTSTAERKE_UMWEG:
            # Erst absichtlich daneben, damit ein echter Wertwechsel
            # entsteht, dann zurück auf den gemerkten Wert.
            cloud.set_voice_volume(device, 99 if wert != 99 else 98)
        ok = cloud.set_voice_volume(device, wert)
        if ok and LAUTSTAERKE_TESTTON:
            cloud.play_voice_test(device)
    except Exception as exc:  # pragma: no cover - reine Absicherung
        _LOG.warning("Lautstärke konnte nicht aufgefrischt werden: %s", exc)
        return False
    if ok:
        # Bewusst ohne Versprechen: Der Roboter hat den Wert im Speicher
        # übernommen - ob er ihn auch auf die Ausgabe anwendet, weiß die
        # App nicht. Ein früherer Text hier lautete "kein Neustart
        # nötig" und redete dem Nutzer damit genau das aus, was als
        # einziges nachweislich hilft.
        log(f"Volume confirmed: {wert}.")
    else:
        log("Note: the volume couldn't be confirmed.")
    return ok


class _Beobachter:
    """Verfolgt, ob der Roboter seit dem Auftrag wirklich etwas getan hat.

    Nötig, weil die Zielkennung schon vor dem Auftrag dieselbe sein kann:
    Eigene Pakete gehen immer unter CUSTOM raus, und wer die Originalstimme
    wiederherstellt, während sie ohnehin läuft, hat denselben Fall. "Die
    Kennung ist aktiv" beweist dann gar nichts - die Meldung stand schon
    vorher da.

    Die Regeln, jede aus einem echten Fehlschlag entstanden:

    1. Als Beweis zählt eine *Veränderung* gegenüber dem Zustand vor dem
       Auftrag. Bloßes Abwarten zählt nicht - der Roboter lässt seine
       letzte Meldung stehen, notfalls tagelang.
    2. Verglichen wird die Bedeutung, nicht die Rohzeile. Ein Nebenfeld
       wie `progress`, das die Firmware von selbst hochzählt, hat sonst
       genau den "Beweis" fabriziert, den Regel 1 verlangt.
    3. Eine Stelle, die nicht, mit `null` oder leer antwortet, ist keine
       Information - und damit auch keine Veränderung.
    4. Widerspricht die aktive Kennung der Erfolgsmeldung, gilt der
       Erfolg nicht. Das wird nach ein paar Runden als eigenes Ergebnis
       gemeldet, statt bis zum Zeitablauf stillzustehen.
    5. Ein Fehlschlag muss zweimal hintereinander zu sehen sein. Er
       beendet den Vorgang und reißt den Webserver ab; ein einzelner
       Ausreißer darf das nicht auslösen.
    """

    FERTIG = "fertig"
    WAHRSCHEINLICH = "wahrscheinlich"
    FEHLER = "fehler"
    WIDERSPRUCH = "widerspruch"
    WARTEN = "warten"

    #: Wartezeit, bevor eine unveränderte Erfolgsmeldung als
    #: WAHRSCHEINLICH durchgeht. Sie beweist nichts - sie gibt der
    #: Installation nur Zeit, überhaupt anzulaufen.
    NACH_DOWNLOAD = 20.0

    #: So oft muss dieselbe Auffälligkeit zu sehen sein, bevor sie zählt.
    BESTAETIGUNGEN = 2

    #: Wie lange ein Widerspruch zwischen Zustand und aktiver Kennung
    #: anhalten muss, bevor er zählt.
    #:
    #: Die beiden Stellen werden am Roboter getrennt geführt: Der Zustand
    #: springt auf "erfolgreich", die aktive Kennung zieht Sekunden später
    #: nach. Wer hier nach zwei Blicken abbricht, würgt eine laufende
    #: Installation ab - und schließt dabei den Webserver, über den der
    #: Roboter womöglich noch nachladen wollte.
    WIDERSPRUCH_FRIST = 60.0

    def __init__(self, cloud: DreameCloud, device: Device, ziel_id: str) -> None:
        self.cloud = cloud
        self.device = device
        self.ziel = (ziel_id or "").strip().upper()
        self.letzter_zustand = None
        self.bewegung = False
        self.start = time.time()
        self.download_beleg = False
        self._fehler_gesehen = 0
        self._widerspruch_gesehen = 0

        vorher = cloud.voice_state(device) or {}
        self.vorher_paket = self._wert(vorher, "paket")
        self.vorher_zustand = self._wert(vorher, "zustand")
        self.vorher_kern = self._kern(_status_lesen(self.vorher_zustand))
        self.paket_bekannt = self.vorher_paket is not None
        self.zustand_bekannt = self.vorher_kern is not None
        self.aktiv = self.vorher_paket
        # Ohne gelesene Kennung wird pessimistisch angenommen, sie stehe
        # bereits auf dem Ziel. Sonst risse ein einziger Abfragefehler
        # genau das Loch auf, das diese Klasse stopfen soll.
        self.schon_aktiv = (not self.paket_bekannt
                            or self._passt(self.vorher_paket))

    # -- Lesen und Vergleichen --------------------------------------------

    @staticmethod
    def _wert(gelesen: dict, schluessel: str):
        """Der brauchbare Wert einer Stelle - sonst None.

        Fehlender Schlüssel, `null` und leerer Text sind dasselbe: keine
        Auskunft. Text wird dabei gleich von Leerzeichen befreit, sonst
        wäre " CUSTOM " etwas anderes als "CUSTOM".
        """
        wert = gelesen.get(schluessel)
        if wert is None:
            return None
        if isinstance(wert, str):
            wert = wert.strip()
            return wert or None
        return wert

    def _passt(self, kennung) -> bool:
        return str(kennung or "").strip().upper() == self.ziel

    @staticmethod
    def _kern(zustand):
        """Die Bedeutung einer Zustandsmeldung: (Zustand, Kennung).

        Nur darauf kommt es an. Früher wurde die ganze Rohzeile
        verglichen - dann genügte ein hochzählendes
        `progress`-Feld, um eine Veränderung vorzutäuschen. Und
        für unlesbaren Text gab es einen Rückfall auf ebendiese
        Rohzeile, womit eine einzelne Fehlerseite denselben
        Scheinbeweis lieferte. Unlesbares kommt hier gar nicht
        mehr an: Der Aufrufer behandelt es als "keine Auskunft".
        """
        if not zustand:
            return None
        return (str(zustand.get("state", "")).strip().lower(),
                str(zustand.get("id", "") or "").strip().upper())

    def los(self) -> None:
        """Setzt die Uhr auf jetzt - Beginn der eigentlichen Beobachtung."""
        self.start = time.time()

    def beleg_download(self) -> None:
        """Der Roboter hat die Datei vollständig vom eigenen Server geholt."""
        self.download_beleg = True

    def beleg_endzustand(self) -> None:
        """Schon der Endzustand allein trägt hier die Aussage.

        Nur beim Zurückholen eines offiziellen Pakets: Dort lautet die
        Meldung "Das Originalpaket ist wieder aktiv" - eine Aussage über
        den Zustand. War es schon vorher aktiv, ist sie trotzdem wahr.

        Beim eigenen Paket wäre derselbe Schluss falsch: Dass CUSTOM
        aktiv ist, heißt nicht, dass das NEUE Paket darunterliegt.
        """
        self.download_beleg = True

    # -- Der Blick auf den Roboter ----------------------------------------

    def nachsehen(self, log: LogFn = _noop_log) -> str:
        gelesen = self.cloud.voice_state(self.device) or {}
        if not gelesen:
            return self.WARTEN

        paket = self._wert(gelesen, "paket")
        zustand_roh = self._wert(gelesen, "zustand")
        # Unlesbares ist keine Auskunft. Früher fiel der Vergleich auf
        # die Rohzeile zurück - eine einzelne HTML-Fehlerseite an dieser
        # Stelle galt damit als Veränderung und machte aus einer
        # stehengebliebenen Erfolgsmeldung ein "installiert und aktiv".
        zustand = _status_lesen(zustand_roh) if zustand_roh is not None else None

        if zustand is not None:
            if zustand_roh != self.letzter_zustand:
                log(f"Zustand: {zustand_roh}")
            self.letzter_zustand = zustand_roh
            kern = self._kern(zustand)
            if not self.zustand_bekannt:
                self.vorher_kern = kern
                self.zustand_bekannt = True
            elif kern != self.vorher_kern:
                self.bewegung = True
        elif zustand_roh is not None:
            _LOG.debug("Zustand nicht lesbar: %r", zustand_roh)

        if paket is not None:
            self.aktiv = paket
            if not self.paket_bekannt:
                self.vorher_paket = paket
                self.paket_bekannt = True
                self.schon_aktiv = self._passt(paket)
            elif str(paket).strip().upper() != str(self.vorher_paket).strip().upper():
                # Verglichen wird normalisiert: "custom" statt "CUSTOM"
                # ist keine Veränderung am Roboter, sondern Schreibweise.
                self.bewegung = True

        gemeldet = (str(zustand.get("state", "")).strip().lower()
                    if zustand is not None else "")
        gescheitert = gemeldet in ("fail", "failed", "error")

        # Der klarste Fall: Die Kennung ist umgesprungen. Nicht aber,
        # wenn der Roboter im selben Atemzug einen Fehlschlag meldet.
        if (paket is not None and self._passt(paket) and not self.schon_aktiv
                and not gescheitert):
            return self.FERTIG

        # Ohne lesbaren Zustand bleibt nur der Download als Beleg. Diese
        # Abzweigung stand früher hinter einem vorzeitigen Ausstieg -
        # ein Roboter, der die Zustandsstelle nicht beantwortet, wurde
        # dadurch nie fertig, obwohl er das Paket nachweislich hatte.
        if zustand is None:
            return self._wahrscheinlich_wenn_reif()

        genannte_id = str(zustand.get("id", "") or "").strip().upper()
        if genannte_id and genannte_id != self.ziel:
            # Eine Meldung über ein fremdes Paket geht uns nichts an -
            # weder ihr Erfolg noch ihr Fehlschlag. Die Zähler laufen
            # dabei nicht weiter: "zweimal hintereinander" heißt
            # hintereinander.
            self._fehler_gesehen = 0
            self._widerspruch_gesehen = 0
            return self.WARTEN

        if gescheitert:
            self._widerspruch_gesehen = 0
            if not self.bewegung:
                self._fehler_gesehen = 0
                return self.WARTEN
            self._fehler_gesehen += 1
            return (self.FEHLER if self._fehler_gesehen >= self.BESTAETIGUNGEN
                    else self.WARTEN)
        self._fehler_gesehen = 0

        if not gemeldet.startswith("succe"):
            self._widerspruch_gesehen = 0
            return self.WARTEN

        # Eine Erfolgsmeldung, der die aktive Kennung widerspricht, ist
        # keine. Sie darf aber nicht sofort zuschlagen: Die beiden
        # Stellen am Roboter werden getrennt geführt, und die Kennung
        # zieht der Zustandsmeldung um Sekunden hinterher. Wer hier nach
        # zwei Blicken abbricht, würgt eine laufende Installation ab -
        # und schließt dabei den Webserver, über den der Roboter noch
        # nachladen wollte.
        if self.aktiv is not None and not self._passt(self.aktiv):
            self._widerspruch_gesehen += 1
            reif = (time.time() - self.start) >= self.WIDERSPRUCH_FRIST
            return (self.WIDERSPRUCH
                    if (reif
                        and self._widerspruch_gesehen >= self.BESTAETIGUNGEN)
                    else self.WARTEN)
        self._widerspruch_gesehen = 0

        if self.bewegung:
            return self.FERTIG
        return self._wahrscheinlich_wenn_reif()

    def _wahrscheinlich_wenn_reif(self) -> str:
        """Der Download als letzter Beleg - aber erst nach der Wartezeit.

        Nichts hat sich gerührt. Der Roboter hat unsere Datei aber
        nachweislich geholt; mehr als "wahrscheinlich" ist daraus nicht
        zu machen, und genau das bekommt der Nutzer auch zu lesen.
        """
        if (self.download_beleg
                and (time.time() - self.start) >= self.NACH_DOWNLOAD):
            return self.WAHRSCHEINLICH
        return self.WARTEN

    @property
    def aktiv_text(self) -> str:
        """Die aktive Kennung für Meldungen - nie das Wort "None"."""
        return str(self.aktiv) if self.aktiv is not None else "unbekannt"


#: Was nach jedem Sprachwechsel im Protokoll und im Fertig-Fenster steht.
#:
#: Zwei unabhängige Berichte, dass der Roboter nach einem Paketwechsel
#: leiser bleibt - in einem Fall ließ er sich auch über die
#: Dreamehome-App nicht mehr lauter stellen, und zwar ebenso nach dem
#: Zurückholen der Originalstimme. Erst ein Neustart half.
#:
#: Damit liegt die Ursache in der Firmware, unterhalb dessen, was über
#: die Cloud erreichbar ist: Der gespeicherte Wert und die gehörte
#: Lautstärke laufen auseinander. Die App kann das nicht beheben. Was
#: sie kann, ist den Nutzer richtig informieren - deshalb steht der
#: Hinweis sichtbar im Fertig-Fenster und nicht nur im Protokoll.
NEUSTART_HINWEIS = (
    "If the robot sounds quieter than usual afterward: that's due to its "
    "firmware, not the recordings - they're at the same level as the "
    "original announcements. After switching languages it sometimes only "
    "applies its volume again after a restart. Turn it off and on again "
    "at the device; that fixes it."
)


def install_pack(cloud: DreameCloud,
                 device: Device,
                 build: BuildResult,
                 port: int = 0,
                 host_ip: str = "",
                 public_url: str = "",
                 log: LogFn = _noop_log,
                 step: StepFn = _noop_step,
                 download_timeout: float = 120.0,
                 install_timeout: float = 420.0,
                 cancelled: Optional[Callable[[], bool]] = None) -> InstallOutcome:
    """Installiert ein gebautes Paket auf dem Roboter.

    Die Kennung ist fest `CUSTOM` und lässt sich nicht ändern. Der
    Roboter legt jedes Paket in einem Ordner pro Kennung ab; löschen
    kann man dort über die Cloud nichts. Vier Kennungen wären vier
    Ordner, die für immer bleiben - eine einzige überschreibt sich
    selbst und belegt dauerhaft nur einen Platz.
    """

    cancelled = cancelled or (lambda: False)
    lang_id = DEFAULT_CUSTOM_LANG_ID

    log(f"Pack:  {build.path.name}")
    log(f"Size: {build.size} bytes ({build.size_mb:.1f} MB)")
    log(f"MD5:    {build.md5}")
    log(f"Identifier: {lang_id}")

    server: Optional[PackServer] = None
    try:
        # ---- 1. Auslieferung vorbereiten -------------------------------
        if public_url:
            url = public_url.strip()
            log(f"Using custom URL: {url}")
            step("Using custom URL", 0.15)
        else:
            step("Starting web server", 0.05)
            server = PackServer(build.path, port=port, host_ip=host_ip, log=log)
            url = server.start()
            step("Web server running", 0.15)

        # ---- 2. Auftrag senden ------------------------------------------
        step("Checking the robot", 0.20)
        log("Asking the robot whether it accepts voice packs the usual "
            "way ...")
        try:
            kennt_sprachpakete = cloud.supports_voice_service(device)
        except (NetworkError, LoginError) as exc:
            # Der Roboter hat gar nicht geantwortet. Das ist etwas anderes
            # als "kennt keine Sprachpakete" - meist schläft er nur.
            # Früher stand hier dieselbe Meldung, und der Nutzer suchte
            # den Fehler bei seinem Gerät.
            return InstallOutcome(
                False,
                "The robot didn't respond to the query.",
                hint=("Nothing was sent. Most often it's because it's "
                      "asleep: wake it in the Dreamehome app - tapping "
                      "'Find Robot' is enough - and try again.\n\n"
                      f"Technical details: {exc}"))

        if not kennt_sprachpakete:
            return InstallOutcome(
                False,
                "This robot doesn't report a voice-pack service.",
                hint=("The app cautiously sent nothing. The install order "
                      "always goes to the same spot on Dreame and MOVA "
                      "vacuum robots (MIoT siid 7, piid 4); your device "
                      "isn't responding there. That suggests it doesn't "
                      "know voice packs at all - for example on mowing "
                      "robots or very old Mi-Home models.\n\n"
                      "Check whether you can even choose a language under "
                      "'Voice' in the Dreamehome app. If that doesn't work "
                      "there, this app can't do it either."),
            )
        log("The robot knows the voice-pack service.")

        # Jetzt merken, nicht später: Nach dem Wechsel wollen wir genau
        # den Wert wiederherstellen, den der Benutzer eingestellt hatte.
        lautstaerke = cloud.voice_volume(device)
        if lautstaerke is not None:
            log(f"Configured volume: {lautstaerke}")

        beobachter = _Beobachter(cloud, device, lang_id)
        if beobachter.schon_aktiv:
            log(f"There's already a pack under '{lang_id}' - it will be "
                f"overwritten.")

        step("Sending the order to the robot", 0.25)
        log("Sending install order via the Dreame cloud ...")
        try:
            cloud.install_voice_pack(device, lang_id, url, build.md5, build.size)
        except NetworkError as exc:
            return InstallOutcome(
                False,
                "The robot didn't accept the order.",
                hint=str(exc),
            )
        log("Order accepted.")

        # ---- 3. Auf den Download warten ---------------------------------
        if server is not None:
            step("Robot downloading the pack", 0.4)
            log(f"Waiting up to {int(download_timeout)} seconds for the download ...")

            deadline = time.time() + download_timeout
            while time.time() < deadline and not server.was_downloaded:
                if cancelled():
                    return InstallOutcome(False, "Cancelled by the user.")
                server.wait_for_download(1.0)

            if not server.was_downloaded:
                # Hat der Roboter überhaupt angeklopft? Dann liegt es
                # nicht an Firewall oder getrennten Netzen - er hat uns
                # ja erreicht. Die alte Meldung schickte den Nutzer in
                # genau diesem Fall auf eine stundenlange Suche an der
                # falschen Stelle.
                # Auch eine abgelehnte Anfrage belegt die
                # Erreichbarkeit - sie kam ja an. Früher zählten nur
                # GET und HEAD, womit gerade der häufigste Auslöser
                # (falscher Pfad) wieder als Firewall galt.
                angeklopft = bool(server.hits)
                if angeklopft:
                    return InstallOutcome(
                        False,
                        "The robot started downloading and then stopped.",
                        hint=("It reached this PC - so it's not a firewall "
                              "or separate networks. The connection dropped "
                              "midway. Most common reasons: weak Wi-Fi "
                              "where the robot currently is, or it went "
                              "into standby. Move it closer to the router, "
                              "wake it in the Dreamehome app, and try "
                              "again."),
                    )
                return InstallOutcome(
                    False,
                    "The robot didn't pick up the voice pack.",
                    hint=reachability_hint(server.port),
                )
            log("Download confirmed by the robot.")
            # Der stärkste Beleg, den wir haben - und der einzige, der
            # nicht vom Roboter selbst kommt: Er hat die Datei gerade
            # von diesem PC geholt. Damit zählt seine Erfolgsmeldung
            # auch dann, wenn kein Blick ins kurze Zwischenfenster
            # gefallen ist. Ohne diesen Beleg meldete die App
            # "Nicht aufgespielt", obwohl alles geklappt hatte.
            beobachter.beleg_download()
            step("Pack transferred", 0.6)
        else:
            step("Waiting for the robot", 0.4)
            time.sleep(5)

        # ---- 4. Installation beobachten ---------------------------------
        step("Robot installing the pack", 0.7)
        log("Waiting for the robot's response ...")

        beobachter.los()
        deadline = time.time() + install_timeout

        while time.time() < deadline:
            if cancelled():
                return InstallOutcome(False, "Cancelled by the user.",
                                      downloaded=True)
            time.sleep(TAKT)

            ergebnis = beobachter.nachsehen(log)

            if ergebnis == _Beobachter.FEHLER:
                return InstallOutcome(
                    False,
                    "The robot reports that the installation failed.",
                    downloaded=True,
                    final_status=str(beobachter.letzter_zustand),
                    hint=("Usually the file doesn't match on MD5 or size, "
                          "or the robot didn't get all the way through it. "
                          "The current voice stays untouched - you can "
                          "just try again."),
                )

            if ergebnis == _Beobachter.WIDERSPRUCH:
                return InstallOutcome(
                    False,
                    f"The robot reports '{beobachter.aktiv_text}' as the "
                    f"active language, not '{lang_id}'.",
                    downloaded=beobachter.download_beleg,
                    final_status=(str(beobachter.letzter_zustand)
                                  if beobachter.letzter_zustand is not None
                                  else None),
                    hint=("The device's state reports success, but the "
                          "active language doesn't match it. Most likely a "
                          "language was selected under 'Voice' in the "
                          "Dreamehome app in the meantime - this makes the "
                          "robot re-download the official pack and "
                          "overwrite the custom one. Try again and leave "
                          "the language selection in the phone app alone."),
                )

            if ergebnis in (_Beobachter.FERTIG, _Beobachter.WAHRSCHEINLICH):
                sicher = ergebnis == _Beobachter.FERTIG
                log(f"The robot reports '{beobachter.aktiv_text}' as the "
                    f"active voice pack.")
                refresh_volume(cloud, device, lautstaerke, log)
                if sicher:
                    meldung = (f"The voice pack '{lang_id}' is "
                               f"installed and active.")
                    hinweis = NEUSTART_HINWEIS
                else:
                    # Der Roboter hat die Datei nachweislich geholt und
                    # meldet Erfolg - aber seine Zustandsmeldung ist
                    # wortgleich mit der von vorher. Damit ist der
                    # Wechsel nicht belegt, nur wahrscheinlich. Das
                    # gehört dem Nutzer gesagt, statt es zu glätten.
                    meldung = (f"The voice pack '{lang_id}' was "
                               f"transferred.")
                    hinweis = (
                        "The robot has provably picked up the pack and "
                        "reports 'successful' - but no state change was "
                        "observed, because the same message was already "
                        "there before. Listen: if the robot speaks in the "
                        "new voice, everything worked.\n\n") + NEUSTART_HINWEIS
                log(hinweis)
                step("Done", 1.0)
                return InstallOutcome(
                    True, meldung,
                    downloaded=True,
                    bestaetigt=sicher,
                    final_status=(str(beobachter.letzter_zustand)
                                  if beobachter.letzter_zustand is not None else None),
                    hint=hinweis,
                )

            progress = 0.7 + min(0.25, (time.time() - beobachter.start)
                                 / install_timeout * 0.25)
            step("Robot installing the pack", progress)

        # Zeit abgelaufen, aber der Download hat geklappt.
        return InstallOutcome(
            False,
            "The robot didn't confirm the installation within the wait time.",
            downloaded=True,
            final_status=(str(beobachter.letzter_zustand)
                          if beobachter.letzter_zustand is not None else None),
            # Bei einer eigenen URL liefert nicht dieser PC aus - dann
            # ist über den Download nichts bekannt, und die Meldung
            # darf ihn auch nicht behaupten.
            hint=(("The pack was provably fetched completely. "
                   if beobachter.download_beleg else
                   "Whether the robot picked up the pack can't be seen "
                   "from here with a custom URL. ")
                  + "It's very likely that the installation is still "
                    "running or is already done. On success the robot "
                    "says 'language switched successfully'. Check the "
                    "voice on the device; if it's unchanged, just start "
                    "the process again."),
        )

    except InstallError:
        raise
    except Exception as exc:  # pragma: no cover - unerwartete Fälle
        _LOG.exception("Installation fehlgeschlagen")
        return InstallOutcome(False, "Unexpected error during installation.",
                              hint=str(exc))
    finally:
        if server is not None:
            server.stop()


def restore_official(cloud: DreameCloud,
                     device: Device,
                     pack: VoicePackInfo,
                     log: LogFn = _noop_log,
                     step: StepFn = _noop_step,
                     timeout: float = 420.0) -> InstallOutcome:
    """Stellt ein offizielles Sprachpaket wieder her.

    Hier wird bewusst Dreames eigene Download-URL benutzt - der Roboter
    lädt also direkt beim Hersteller, ganz ohne PC im Spiel. Das ist
    derselbe Vorgang, den die Dreamehome-App beim Sprachwechsel auslöst.
    """
    log(f"Restoring the official pack '{pack.label}'.")
    log(f"Source: {pack.url}")
    log(f"Size: {pack.size} bytes, MD5: {pack.md5}")

    # Wie beim eigenen Paket: erst die Lautstärke merken, dann den
    # Zustand vor dem Auftrag festhalten. Aus dem Forum kam der Bericht,
    # dass der Roboter auch *nach* dem Zurückholen der Originalstimme
    # leise blieb - dieser Weg braucht also dieselbe Behandlung.
    lautstaerke = cloud.voice_volume(device)
    if lautstaerke is not None:
        log(f"Configured volume: {lautstaerke}")
    beobachter = _Beobachter(cloud, device, pack.id)
    if beobachter.schon_aktiv:
        log(f"'{pack.id}' is already the active identifier - the pack "
            f"will be reloaded.")

    step("Sending the order", 0.2)
    try:
        cloud.install_voice_pack(device, pack.id, pack.url, pack.md5, pack.size)
    except NetworkError as exc:
        return InstallOutcome(False, "The robot didn't accept the order.",
                              hint=str(exc))

    log("Order accepted. The robot is now downloading directly from Dreame.")
    step("Robot downloading from Dreame", 0.5)

    beobachter.los()
    beobachter.beleg_endzustand()
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(TAKT)
        ergebnis = beobachter.nachsehen(log)

        if ergebnis == _Beobachter.FEHLER:
            return InstallOutcome(
                False,
                "The robot reports that restoring it failed.",
                final_status=str(beobachter.letzter_zustand),
                hint=("The current voice stays untouched. Try again, or "
                      "switch the language in the Dreamehome app under "
                      "Settings > Voice Pack."))

        if ergebnis == _Beobachter.WIDERSPRUCH:
            return InstallOutcome(
                False,
                f"The robot reports '{beobachter.aktiv_text}' as the "
                f"active language, not '{pack.id}'.",
                hint=("The device's state message doesn't match the "
                      "active language. Switch the language in the "
                      "Dreamehome app under 'Voice' - that's the same "
                      "process, and you'll see immediately what the robot "
                      "does."))

        if ergebnis in (_Beobachter.FERTIG, _Beobachter.WAHRSCHEINLICH):
            refresh_volume(cloud, device, lautstaerke, log)
            hinweis = NEUSTART_HINWEIS
            if not beobachter.bewegung:
                # Der Roboter führte diese Sprache schon vorher, und es
                # war keine Veränderung zu beobachten. Die Meldung
                # stimmt trotzdem - sie sagt etwas über den Zustand aus,
                # nicht über den Vorgang. Wer aber wiederherstellt,
                # WEIL etwas kaputt ist, darf davon nicht in Sicherheit
                # gewiegt werden.
                hinweis = (
                    f"Note: '{pack.id}' was already the active language "
                    f"before, and the robot didn't report a fresh install. "
                    f"If you wanted to renew the pack because something's "
                    f"wrong: switch to a different language in the "
                    f"Dreamehome app under 'Voice' and back again - that "
                    f"guarantees the robot reloads it.\n\n"
                ) + NEUSTART_HINWEIS
                log(hinweis)
            else:
                log(NEUSTART_HINWEIS)
            step("Done", 1.0)
            return InstallOutcome(
                True, f"The original pack '{pack.id}' is active again.",
                # Hier lädt der Roboter direkt bei Dreame - von hier
                # aus wurde nichts übertragen, das dürfen wir auch
                # nicht behaupten.
                downloaded=False,
                bestaetigt=(ergebnis == _Beobachter.FERTIG),
                hint=hinweis)

    return InstallOutcome(
        False,
        "No confirmation within the wait time.",
        hint=("The order was accepted. Check the voice on the robot - "
              "the installation often went through anyway. Alternatively, "
              "the language can be changed any time in the Dreamehome "
              "app under Settings > Voice Pack."),
    )
