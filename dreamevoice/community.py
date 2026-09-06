"""Fertige Sprachpakete aus der Community.

Was es wirklich gibt - und was nicht
------------------------------------
Es existiert **kein** offizieller oder inoffizieller Marktplatz mit
Dreame-Sprachpaketen. Was es gibt, sind einige wenige Bastelprojekte auf
GitHub. Die hier gelisteten Einträge wurden einzeln geprüft: das
Projekt existiert, die Datei lädt herunter, und der Inhalt ist ein
tar-Archiv mit Ogg-Dateien im erwarteten Schema.

Bayerisch, Schwäbisch oder eine Prominentenstimme wie Bruce Willis gibt
es als fertiges Dreame-Paket nicht. Solche Pakete müsste man selbst
erzeugen - technisch geht das über "Einzelne Ansagen", indem
man die gewünschten Ansagen mit einer Sprachsynthese erzeugt und
zuweist. Stimmen realer Personen nachzubilden ist rechtlich heikel
(Persönlichkeitsrecht) und deshalb bewusst nicht Teil dieser App.

Wichtig zur Kompatibilität
---------------------------
Alle Community-Pakete stammen von älteren Modellen und enthalten nur
150-520 Ansagen, während der X50 Ultra Complete 558 kennt. Direkt
installiert bliebe der Roboter bei allen fehlenden Ansagen stumm.

Diese App installiert sie deshalb nie direkt, sondern legt sie über das
offizielle Paket des eigenen Modells (siehe packer.overlay_pack). Ersetzt
wird nur, was das Fremdpaket wirklich mitbringt - der Rest bleibt auf der
offiziellen deutschen Stimme.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit
from typing import Callable, List, Optional

import requests

from .errors import NetworkError, PackError
from .official import md5_of_file
from .paths import data_dir

_LOG = logging.getLogger(__name__)

ProgressFn = Callable[[int, int], None]

#: Größer ist kein Sprachpaket. Das größte Fremdpaket in dieser
#: Liste wiegt 18,8 MB; die Originalpakete von Dreame rund 10 MB.
#: Ohne Grenze lädt ein `archive/refs/heads/main.zip` so viel, wie der
#: Projektinhaber gerade hineinlegt - und `Content-Length` fehlt dort.
MAX_PAKET_BYTES = 200 * 1024 * 1024

#: Von wo ein Fremdpaket kommen darf. Nachgemessen an allen sieben
#: Einträgen: ausgeliefert wird von release-assets.githubusercontent.com,
#: raw.githubusercontent.com und codeload.github.com - alle unter
#: github.com bzw. githubusercontent.com.
ERLAUBTE_HOSTS = ("github.com", "githubusercontent.com")


def adresse_erlaubt(url: str) -> bool:
    """Nur gesichert und nur von GitHub."""
    try:
        teil = urlsplit(url or "")
    except ValueError:
        return False
    if teil.scheme.lower() != "https":
        return False
    wirt = (teil.hostname or "").lower()
    return any(wirt == h or wirt.endswith("." + h) for h in ERLAUBTE_HOSTS)


@dataclass
class CommunityPack:
    """Ein herunterladbares Community-Paket."""

    key: str
    name: str
    description: str
    language: str
    url: str
    project_url: str
    author: str
    license: str
    approx_sounds: int
    expected_size: int = 0
    expected_md5: str = ""
    archive_kind: str = "tar.gz"   # tar.gz oder zip
    notes: str = ""
    tags: List[str] = field(default_factory=list)

    @property
    def size_mb(self) -> float:
        return self.expected_size / (1024 * 1024) if self.expected_size else 0.0

    def local_path(self) -> Path:
        suffix = ".zip" if self.archive_kind == "zip" else ".tar.gz"
        folder = data_dir() / "Community Packs"
        folder.mkdir(parents=True, exist_ok=True)
        return folder / f"{self.key}{suffix}"


# --------------------------------------------------------------------------
# Geprüft am 08.08.2026: Projekt vorhanden, Datei lädt, Format stimmt.
# --------------------------------------------------------------------------

PACKS: List[CommunityPack] = [
    CommunityPack(
        key="glados_zigerschlitz",
        name="GLaDOS",
        description=(
            "The sarcastic AI from the game Portal. The best-maintained "
            "GLaDOS set, as a ready-made archive with a published checksum."
        ),
        language="English",
        url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
             "releases/download/0.1/glados.tar.gz"),
        project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
        author="Makers Im Zigerschlitz",
        license="no license given",
        approx_sounds=155,
        expected_size=4322744,
        expected_md5="d79114b8b0b41e132dd0214f4922836c",
        tags=["funny", "AI", "game"],
    ),
    CommunityPack(
        key="r2d2_zigerschlitz",
        name="R2-D2",
        description=(
            "Just beeps and chirps from the Star Wars droid instead of "
            "sentences. Very entertaining, but you no longer know what the "
            "robot is actually reporting."
        ),
        language="no speech",
        url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
             "releases/download/0.1/r2d2.tar.gz"),
        project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
        author="Makers Im Zigerschlitz",
        license="no license given",
        approx_sounds=155,
        expected_size=18808415,
        expected_md5="bdd0b85996748e20037b20bbede258aa",
        notes="Note: error messages are no longer intelligible after this.",
        tags=["funny", "movie", "no speech"],
    ),
    CommunityPack(
        key="memes_zigerschlitz",
        name="Memes",
        description="Internet meme sounds instead of the usual announcements.",
        language="English / no speech",
        url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
             "releases/download/0.1/memes.tar.gz"),
        project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
        author="Makers Im Zigerschlitz",
        license="no license given",
        approx_sounds=155,
        expected_size=4398965,
        expected_md5="ba83696fe8e954983a9960a14825b6c5",
        tags=["funny"],
    ),
    CommunityPack(
        key="glados_findus23",
        name="GLaDOS (15.ai variant)",
        description=(
            "Older GLaDOS version, generated with the 15.ai speech "
            "synthesizer. Different intonation than the variant above."
        ),
        language="English",
        url="https://github.com/Findus23/voice_pack_dreame/raw/main/voice_pack.tar.gz",
        project_url="https://github.com/Findus23/voice_pack_dreame",
        author="Findus23",
        license="no license given",
        approx_sounds=155,
        expected_size=4325024,
        expected_md5="8ebfabb9e23e169a5c9b867266f9d1ef",
        tags=["funny", "AI", "game"],
    ),
    CommunityPack(
        key="glados_x40_kokoro",
        name="GLaDOS for X40 (514 announcements)",
        description=(
            "By far the most extensive set: all 514 announcements of the "
            "X40 Ultra rewritten and spoken with Kokoro TTS. Since the X40 "
            "and X50 share 513 numbers, this pack covers almost the "
            "entire X50."
        ),
        language="English",
        url="https://github.com/sproft/dreame-x40-glados-voice-pack/archive/refs/heads/main.zip",
        project_url="https://github.com/sproft/dreame-x40-glados-voice-pack",
        author="sproft",
        license="see LICENSE in the project",
        approx_sounds=514,
        archive_kind="zip",
        notes=("Downloaded as a project archive; the app extracts the "
               "Ogg files from it. Size and checksum change with every "
               "update to the project, so they aren't checked against a "
               "fixed value."),
        tags=["funny", "AI", "game", "extensive"],
    ),
    CommunityPack(
        key="uk_female_pensive",
        name="Ukrainian (female, calm)",
        description="Ukrainian announcements, spoken calmly and matter-of-factly.",
        language="Ukrainian",
        url=("https://github.com/oleksandr-belei/dreame-vacuum-uk-voice-packs/"
             "raw/main/voice_packs/uk_female_pensive"),
        project_url="https://github.com/oleksandr-belei/dreame-vacuum-uk-voice-packs",
        author="oleksandr-belei",
        license="MIT",
        approx_sounds=199,
        expected_size=3585448,
        # Selbst nachgerechnet: gzip-tar mit genau 199 .ogg-Dateien,
        # ohne Steuerdateien. Ohne diese Angabe galt eine einmal
        # geladene Datei für immer als gültig.
        expected_md5="55bfe4272ce1e77d9bbafebf9ec99330",
        tags=["language"],
    ),
    CommunityPack(
        key="original_en_zigerschlitz",
        name="Original English (backup)",
        description=(
            "The original English announcements of an older model. Mainly "
            "useful as reference material."
        ),
        language="English",
        url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
             "releases/download/0.1/original-en.tar.gz"),
        project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
        author="Makers Im Zigerschlitz",
        license="no license given",
        approx_sounds=155,
        expected_size=3102855,
        expected_md5="2a467cdb59f0ecff54ccb6931c81c0b3",
        tags=["language", "reference"],
    ),
]


def get(key: str) -> Optional[CommunityPack]:
    for pack in PACKS:
        if pack.key == key:
            return pack
    return None


def download(pack: CommunityPack, progress: Optional[ProgressFn] = None,
             force: bool = False) -> Path:
    """Lädt ein Community-Paket herunter und prüft es, soweit möglich."""
    target = pack.local_path()

    if target.exists() and not force:
        if not pack.expected_md5 or md5_of_file(target) == pack.expected_md5:
            if progress:
                progress(1, 1)
            return target
        target.unlink(missing_ok=True)

    if not adresse_erlaubt(pack.url):
        raise NetworkError(
            f"'{pack.name}''s source address isn't allowed.",
            f"Third-party packs are only downloaded from GitHub.\n\n"
            f"Address: {pack.url}")

    tmp = target.with_suffix(target.suffix + ".part")
    try:
        with requests.get(pack.url, stream=True, timeout=90,
                          headers={"User-Agent": "DreameSprachpakete/1.0"}) as resp:
            if resp.status_code != 200:
                raise NetworkError(
                    f"Download failed (HTTP {resp.status_code}).",
                    f"Source: {pack.url}",
                )
            total = int(resp.headers.get("Content-Length") or pack.expected_size or 0)
            done = 0
            with tmp.open("wb") as fh:
                for block in resp.iter_content(chunk_size=1 << 16):
                    if not block:
                        continue
                    fh.write(block)
                    done += len(block)
                    if done > MAX_PAKET_BYTES:
                        raise NetworkError(
                            f"'{pack.name}' is unexpectedly large.",
                            "The download was aborted. A voice pack "
                            "weighs about ten megabytes.")
                    if progress:
                        progress(done, total)
    except requests.exceptions.RequestException as exc:
        tmp.unlink(missing_ok=True)
        raise NetworkError(f"The pack '{pack.name}' couldn't be downloaded.",
                           f"Technical details: {exc}") from exc
    except BaseException:
        # Der Abbruch wegen Überlänge ist ein NetworkError und damit
        # keine RequestException - er liefe sonst an dieser Zeile vorbei
        # und ließe die halbe Datei liegen. Auch für den Abbruch durch
        # den Nutzer gilt das.
        tmp.unlink(missing_ok=True)
        raise

    if pack.expected_md5:
        actual = md5_of_file(tmp)
        if actual != pack.expected_md5:
            tmp.unlink(missing_ok=True)
            raise PackError(
                f"'{pack.name}''s checksum doesn't match.",
                f"Expected {pack.expected_md5}, got {actual}. The download "
                f"was discarded - the file won't be used.",
            )

    tmp.replace(target)
    _LOG.info("Community-Paket %s geladen (%d Bytes)", pack.key, target.stat().st_size)
    return target


def all_tags() -> List[str]:
    tags = set()
    for pack in PACKS:
        tags.update(pack.tags)
    return sorted(tags)
