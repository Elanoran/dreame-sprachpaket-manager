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
from .i18n import t
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
        folder = data_dir() / t("community.packs_folder_name")
        folder.mkdir(parents=True, exist_ok=True)
        return folder / f"{self.key}{suffix}"


# --------------------------------------------------------------------------
# Geprüft am 08.08.2026: Projekt vorhanden, Datei lädt, Format stimmt.
# --------------------------------------------------------------------------

#: Cache for _packs() - see the comment there for why PACKS isn't a
#: plain module-level list.
_packs_cache: Optional[List[CommunityPack]] = None


def _build_packs() -> List[CommunityPack]:
    return [
        CommunityPack(
            key="glados_zigerschlitz",
            name="GLaDOS",
            description=t("community.desc_glados_zigerschlitz"),
            language=t("community.language_english"),
            url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
                 "releases/download/0.1/glados.tar.gz"),
            project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
            author="Makers Im Zigerschlitz",
            license=t("community.license_none"),
            approx_sounds=155,
            expected_size=4322744,
            expected_md5="d79114b8b0b41e132dd0214f4922836c",
            tags=[t("community.tag_funny"), t("community.tag_ai"), t("community.tag_game")],
        ),
        CommunityPack(
            key="r2d2_zigerschlitz",
            name="R2-D2",
            description=t("community.desc_r2d2"),
            language=t("community.language_no_speech"),
            url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
                 "releases/download/0.1/r2d2.tar.gz"),
            project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
            author="Makers Im Zigerschlitz",
            license=t("community.license_none"),
            approx_sounds=155,
            expected_size=18808415,
            expected_md5="bdd0b85996748e20037b20bbede258aa",
            notes=t("community.notes_r2d2"),
            tags=[t("community.tag_funny"), t("community.tag_movie"), t("community.tag_no_speech")],
        ),
        CommunityPack(
            key="memes_zigerschlitz",
            name="Memes",
            description=t("community.desc_memes"),
            language=t("community.language_english_no_speech"),
            url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
                 "releases/download/0.1/memes.tar.gz"),
            project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
            author="Makers Im Zigerschlitz",
            license=t("community.license_none"),
            approx_sounds=155,
            expected_size=4398965,
            expected_md5="ba83696fe8e954983a9960a14825b6c5",
            tags=[t("community.tag_funny")],
        ),
        CommunityPack(
            key="glados_findus23",
            name=t("community.name_glados_findus23"),
            description=t("community.desc_glados_findus23"),
            language=t("community.language_english"),
            url="https://github.com/Findus23/voice_pack_dreame/raw/main/voice_pack.tar.gz",
            project_url="https://github.com/Findus23/voice_pack_dreame",
            author="Findus23",
            license=t("community.license_none"),
            approx_sounds=155,
            expected_size=4325024,
            expected_md5="8ebfabb9e23e169a5c9b867266f9d1ef",
            tags=[t("community.tag_funny"), t("community.tag_ai"), t("community.tag_game")],
        ),
        CommunityPack(
            key="glados_x40_kokoro",
            name=t("community.name_glados_x40"),
            description=t("community.desc_glados_x40"),
            language=t("community.language_english"),
            url="https://github.com/sproft/dreame-x40-glados-voice-pack/archive/refs/heads/main.zip",
            project_url="https://github.com/sproft/dreame-x40-glados-voice-pack",
            author="sproft",
            license=t("community.license_see_project"),
            approx_sounds=514,
            archive_kind="zip",
            notes=t("community.notes_x40"),
            tags=[t("community.tag_funny"), t("community.tag_ai"), t("community.tag_game"),
                  t("community.tag_extensive")],
        ),
        CommunityPack(
            key="uk_female_pensive",
            name=t("community.name_uk_female_pensive"),
            description=t("community.desc_uk_female_pensive"),
            language=t("community.language_ukrainian"),
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
            tags=[t("community.tag_language")],
        ),
        CommunityPack(
            key="original_en_zigerschlitz",
            name=t("community.name_original_en"),
            description=t("community.desc_original_en"),
            language=t("community.language_english"),
            url=("https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame/"
                 "releases/download/0.1/original-en.tar.gz"),
            project_url="https://github.com/Makers-Im-Zigerschlitz/voicepacks_dreame",
            author="Makers Im Zigerschlitz",
            license=t("community.license_none"),
            approx_sounds=155,
            expected_size=3102855,
            expected_md5="2a467cdb59f0ecff54ccb6931c81c0b3",
            tags=[t("community.tag_language"), t("community.tag_reference")],
        ),
    ]


def _packs() -> List[CommunityPack]:
    """Builds PACKS on first use and caches it - see __getattr__ below."""
    global _packs_cache
    if _packs_cache is None:
        _packs_cache = _build_packs()
    return _packs_cache


def __getattr__(name: str) -> List[CommunityPack]:
    """PEP 562 module hook: resolves `community.PACKS` lazily.

    A plain `PACKS = [...]` at module scope would run every t() call in
    it the moment this module is first imported - which happens via
    ui/tab_store.py's own top-of-file imports, before ui/app.py's
    MainWindow ever calls i18n.set_language(). Deferring construction to
    first real attribute access (which happens once the UI is actually
    being built, after the language is set) keeps `community.PACKS`
    working exactly as before for every caller.
    """
    if name == "PACKS":
        return _packs()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def get(key: str) -> Optional[CommunityPack]:
    for pack in _packs():
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
            t("community.source_not_allowed_message", name=pack.name),
            t("community.source_not_allowed_hint", url=pack.url))

    tmp = target.with_suffix(target.suffix + ".part")
    try:
        with requests.get(pack.url, stream=True, timeout=90,
                          headers={"User-Agent": "DreameSprachpakete/1.0"}) as resp:
            if resp.status_code != 200:
                raise NetworkError(
                    t("community.download_failed_http", status=resp.status_code),
                    t("community.download_failed_http_hint", url=pack.url),
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
                            t("community.pack_too_large_message", name=pack.name),
                            t("community.pack_too_large_hint"))
                    if progress:
                        progress(done, total)
    except requests.exceptions.RequestException as exc:
        tmp.unlink(missing_ok=True)
        raise NetworkError(t("community.download_request_failed", name=pack.name),
                           t("community.download_technical_details", details=exc)) from exc
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
                t("community.checksum_mismatch_message", name=pack.name),
                t("community.checksum_mismatch_hint",
                  expected=pack.expected_md5, actual=actual),
            )

    tmp.replace(target)
    _LOG.info("Community-Paket %s geladen (%d Bytes)", pack.key, target.stat().st_size)
    return target


def all_tags() -> List[str]:
    tags = set()
    for pack in _packs():
        tags.update(pack.tags)
    return sorted(tags)
