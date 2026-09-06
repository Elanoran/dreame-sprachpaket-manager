"""Einrichtungshilfe für ffmpeg - der Notnagel, nicht der Regelfall.

ffmpeg wird gebraucht, um mp3-, wav- oder m4a-Dateien in das Format zu
bringen, das der Roboter versteht (OGG Vorbis, mono, 16000 Hz). Fertige
.ogg-Dateien im richtigen Format funktionieren auch ohne ffmpeg.

**In der EXE ist ffmpeg bereits enthalten** (siehe embedded.py) und wird
beim ersten Bedarf ausgepackt - dieser Weg hier kommt dann gar nicht zum
Zug. Gebraucht wird er nur, wenn die App aus dem Quellcode läuft und
weder neben der App noch im PATH ein ffmpeg liegt.

Diese Datei lädt nichts von allein herunter. Der Download startet
ausschließlich, wenn der Nutzer ihn in der Oberfläche ausdrücklich
bestätigt - dort steht vorher, von welcher Adresse geladen wird und wie
groß die Datei ist.

Quelle ist das öffentliche Release-Verzeichnis von BtbN/FFmpeg-Builds auf
GitHub. Das ist die von ffmpeg.org selbst verlinkte Bezugsquelle für
Windows-Builds.

Aus dem Archiv wird bewusst nicht alles entpackt, sondern gezielt nur
ffmpeg.exe und ffprobe.exe - und zwar nur anhand ihres Dateinamens, ohne
die im Archiv hinterlegten Pfade zu übernehmen. Ein manipuliertes Archiv
kann so nichts an anderer Stelle im Dateisystem ablegen.
"""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path
from typing import Callable, Optional

import requests

from .audio import _run, find_ffmpeg
from .errors import AudioError, NetworkError
from .i18n import t
from .paths import data_dir

_LOG = logging.getLogger(__name__)

ProgressFn = Callable[[int, int], None]
LogFn = Callable[[str], None]

DOWNLOAD_URL = ("https://github.com/BtbN/FFmpeg-Builds/releases/download/"
                "latest/ffmpeg-master-latest-win64-gpl.zip")
PROJECT_URL = "https://github.com/BtbN/FFmpeg-Builds"
APPROX_SIZE_MB = 170

WANTED = {"ffmpeg.exe", "ffprobe.exe"}
MAX_ARCHIVE_BYTES = 400 * 1024 * 1024
MAX_MEMBER_BYTES = 250 * 1024 * 1024


def target_dir() -> Path:
    return data_dir() / "ffmpeg"


def installed_path() -> Optional[Path]:
    candidate = target_dir() / "ffmpeg.exe"
    return candidate if candidate.is_file() else None


def describe_source() -> str:
    """Text für den Bestätigungsdialog."""
    return t("ffmpeg_setup.describe_source", url=DOWNLOAD_URL,
             project_url=PROJECT_URL, size_mb=APPROX_SIZE_MB)


def _noop_log(_: str) -> None:
    pass


def download_and_install(progress: Optional[ProgressFn] = None,
                         log: LogFn = _noop_log,
                         cancelled: Optional[Callable[[], bool]] = None) -> Path:
    """Lädt ffmpeg und legt ffmpeg.exe im Datenordner ab.

    Nur nach ausdrücklicher Bestätigung durch den Nutzer aufrufen.
    """
    cancelled = cancelled or (lambda: False)
    dest = target_dir()
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / "_download.zip"

    log(t("ffmpeg_setup.log_downloading_from", url=DOWNLOAD_URL))
    try:
        with requests.get(DOWNLOAD_URL, stream=True, timeout=120,
                          headers={"User-Agent": "DreameSprachpakete/1.0"}) as resp:
            if resp.status_code != 200:
                raise NetworkError(
                    t("ffmpeg_setup.download_failed_title", status=resp.status_code),
                    t("ffmpeg_setup.download_failed_detail", url=DOWNLOAD_URL))

            total = int(resp.headers.get("Content-Length") or 0)
            if total and total > MAX_ARCHIVE_BYTES:
                raise NetworkError(
                    t("ffmpeg_setup.file_too_large_title"),
                    t("ffmpeg_setup.file_too_large_detail",
                      size_mb=total // (1024 * 1024)))

            done = 0
            with archive.open("wb") as fh:
                for block in resp.iter_content(chunk_size=1 << 18):
                    if cancelled():
                        raise NetworkError(t("ffmpeg_setup.cancelled_by_user"))
                    if not block:
                        continue
                    fh.write(block)
                    done += len(block)
                    if done > MAX_ARCHIVE_BYTES:
                        raise NetworkError(t("ffmpeg_setup.download_grew_too_large"))
                    if progress:
                        progress(done, total)
    except requests.exceptions.RequestException as exc:
        archive.unlink(missing_ok=True)
        raise NetworkError(t("ffmpeg_setup.download_error_title"),
                           t("ffmpeg_setup.technical_details_detail", error=exc)) from exc
    except Exception:
        archive.unlink(missing_ok=True)
        raise

    log(t("ffmpeg_setup.log_downloaded",
          size_mb=archive.stat().st_size // (1024 * 1024)))
    log(t("ffmpeg_setup.log_extracting"))

    extracted: list[str] = []
    try:
        with zipfile.ZipFile(archive) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                # Nur der reine Dateiname zählt - Pfade aus dem Archiv werden
                # verworfen, damit nichts außerhalb von dest landen kann.
                name = Path(info.filename.replace("\\", "/")).name
                if name.lower() not in WANTED:
                    continue
                if info.file_size > MAX_MEMBER_BYTES:
                    continue
                with zf.open(info) as src, (dest / name).open("wb") as out:
                    while True:
                        chunk = src.read(1 << 20)
                        if not chunk:
                            break
                        out.write(chunk)
                extracted.append(name)
    except zipfile.BadZipFile as exc:
        archive.unlink(missing_ok=True)
        raise AudioError(t("ffmpeg_setup.invalid_archive_title"),
                         t("ffmpeg_setup.technical_details_detail", error=exc)) from exc
    finally:
        archive.unlink(missing_ok=True)

    exe = dest / "ffmpeg.exe"
    if not exe.is_file():
        raise AudioError(
            t("ffmpeg_setup.exe_missing_title"),
            t("ffmpeg_setup.exe_missing_detail",
              found=', '.join(extracted) or t("ffmpeg_setup.nothing_found")))

    log(t("ffmpeg_setup.log_extracted", files=', '.join(extracted)))

    # Funktionsprobe: läuft die Datei, und kann sie Vorbis kodieren?
    try:
        version = _run([str(exe), "-version"], timeout=30)
    except Exception as exc:
        raise AudioError(t("ffmpeg_setup.exe_wont_start_title"),
                         t("ffmpeg_setup.technical_details_detail", error=exc)) from exc

    if version.returncode != 0:
        raise AudioError(t("ffmpeg_setup.exe_error_title"),
                         (version.stderr or "")[:300])

    first_line = (version.stdout or "").splitlines()
    log(first_line[0] if first_line else t("ffmpeg_setup.ffmpeg_started_fallback"))

    encoders = _run([str(exe), "-hide_banner", "-encoders"], timeout=30)
    if "libvorbis" not in (encoders.stdout or ""):
        raise AudioError(
            t("ffmpeg_setup.vorbis_missing_title"),
            t("ffmpeg_setup.vorbis_missing_detail"))

    log(t("ffmpeg_setup.log_vorbis_ready"))
    return exe


def ensure() -> Optional[Path]:
    """Sucht ffmpeg (auch das selbst eingerichtete) - ohne Download."""
    return find_ffmpeg()
