"""Bauen des eigenen Sprachpakets.

Grundgedanke: **nichts wegwerfen, was man nicht ersetzt.**

Ein Dreame-Sprachpaket ist ein gzip-komprimiertes tar-Archiv, in dem alle
Dateien flach nebeneinander liegen:

    0.ogg 1.ogg 2.ogg ... 864.ogg
    voice_mapping.json tts.json dmr_audio.json
    first_audio.json mini_broad.json time.txt

Die JSON-Dateien steuern, welche Ansage wann und wie abgespielt wird und
wie Nummern zwischen Modellvarianten umgesetzt werden. Würde man ein
Paket nur aus ein paar selbst aufgenommenen Dateien bauen, fänden sich
alle übrigen Ansagen nicht mehr - der Roboter bliebe bei ihnen stumm.

Deshalb entsteht ein eigenes Paket hier immer als **Kopie des offiziellen
Pakets** des jeweiligen Modells, in der nur die ausgewählten Ogg-Dateien
überschrieben werden. Alle Steuerdateien und alle nicht angefassten
Ansagen bleiben Byte für Byte erhalten.
"""

from __future__ import annotations

import hashlib
import io
import logging
import tarfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .audio import prepare
from .errors import PackError
from .i18n import t
from .loudness import reference_levels, target_for
from .paths import build_dir

_LOG = logging.getLogger(__name__)

LogFn = Callable[[str], None]
ProgressFn = Callable[[int, int], None]


@dataclass
class BuildResult:
    """Ergebnis eines Paketbaus - genau das, was die Installation braucht."""

    path: Path
    md5: str
    size: int
    replaced: List[int] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    total_members: int = 0

    @property
    def size_mb(self) -> float:
        return self.size / (1024 * 1024)

    def summary(self) -> str:
        return (f"{self.path.name} - {self.size_mb:.1f} MB, "
                + t("packer.summary_replaced", replaced=len(self.replaced),
                    total=self.total_members))


def _noop_log(_: str) -> None:
    pass


def _md5_and_size(path: Path) -> tuple[str, int]:
    h = hashlib.md5()
    size = 0
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
            size += len(block)
    return h.hexdigest(), size


def _tarinfo(name: str, size: int) -> tarfile.TarInfo:
    """Eintrag exakt so, wie Dreame ihn auch schreibt."""
    info = tarfile.TarInfo(name=name)
    info.size = size
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = int(time.time())
    info.type = tarfile.REGTYPE
    return info


def apply_mapping(assignments: Dict[int, Path],
                  mapping: Optional[Dict[int, int]],
                  log: LogFn = _noop_log) -> Dict[int, Path]:
    """Spiegelt Zuweisungen entlang der Nummern-Umsetzung des Modells.

    Manche Modelle spielen für eine Ansage eine andere Nummer ab (siehe
    official.read_voice_mapping). Damit ein Austausch nicht ins Leere
    läuft, bekommt die Zielnummer dieselbe Datei - und umgekehrt. Welche
    Richtung das Gerät tatsächlich nutzt, spielt dann keine Rolle mehr.
    """
    if not mapping:
        return dict(assignments)

    ergebnis = dict(assignments)
    gespiegelt = []

    for quelle, ziel in sorted(mapping.items()):
        if quelle in assignments and ziel not in ergebnis:
            ergebnis[ziel] = assignments[quelle]
            gespiegelt.append(f"{quelle}->{ziel}")
        elif ziel in assignments and quelle not in ergebnis:
            ergebnis[quelle] = assignments[ziel]
            gespiegelt.append(f"{ziel}->{quelle}")

    if gespiegelt:
        log(f"Nummern-Umsetzung deines Modells beachtet: {', '.join(gespiegelt)}")
    return ergebnis


def build_pack(base_pack: Path,
               assignments: Dict[int, Path],
               out_name: str = "mein_sprachpaket.tar.gz",
               ffmpeg: Optional[Path] = None,
               work_dir: Optional[Path] = None,
               mapping: Optional[Dict[int, int]] = None,
               log: LogFn = _noop_log,
               progress: Optional[ProgressFn] = None) -> BuildResult:
    """Baut ein Paket aus `base_pack` mit den Ersetzungen aus `assignments`.

    `assignments` bildet Ansage-Nummer auf eine lokale Audiodatei ab. Die
    Dateien werden - falls nötig - vorher nach OGG Vorbis mono 16 kHz
    umgewandelt.

    `mapping` ist die Nummern-Umsetzung des Modells: damit landen
    ausgetauschte Ansagen auch auf der Nummer, die das Gerät wirklich
    abspielt.
    """
    assignments = apply_mapping(assignments, mapping, log)

    if not base_pack.is_file():
        raise PackError(
            t("packer.base_pack_missing_title"),
            t("packer.base_pack_missing_hint"),
        )
    if not assignments:
        raise PackError(
            t("packer.no_assignments_title"),
            t("packer.no_assignments_hint"),
        )

    work_dir = work_dir or (build_dir() / "_arbeit")
    work_dir.mkdir(parents=True, exist_ok=True)
    out_path = build_dir() / out_name

    # ---- Schritt 1: Audiodateien vorbereiten ---------------------------
    log(t("packer.log_preparing_audio"))
    prepared: Dict[int, Path] = {}
    warnings: List[str] = []

    # Lautheit der Originalansagen als Vorlage, damit die ausgetauschten
    # Ansagen genauso laut sind wie die, die stehen bleiben.
    pegel = reference_levels(base_pack, ffmpeg, log=log)

    items = sorted(assignments.items())
    for index, (sound_id, src) in enumerate(items, 1):
        src = Path(src)
        try:
            usable, converted = prepare(src, work_dir / f"{sound_id}.ogg", ffmpeg,
                                        target_lufs=target_for(pegel, sound_id))
        except Exception as exc:  # AudioError und alles Unerwartete
            raise PackError(
                t("packer.announcement_error", id=sound_id,
                  message=getattr(exc, "message", str(exc))),
                getattr(exc, "hint", ""),
            ) from exc

        prepared[sound_id] = usable
        log(f"  {sound_id:>4}  {src.name}"
            + (t("packer.converted_suffix") if converted else t("packer.asis_suffix")))
        if progress:
            progress(index, len(items))

    # ---- Schritt 2: Archiv neu schreiben --------------------------------
    log(t("packer.log_building_archive"))
    replaced: List[int] = []
    total_members = 0
    tmp_path = out_path.with_suffix(".part")

    try:
        with tarfile.open(base_pack, "r:gz") as src_tar, \
                tarfile.open(tmp_path, "w:gz", compresslevel=6) as dst_tar:

            members = [m for m in src_tar.getmembers() if m.isfile()]
            total = len(members)

            for index, member in enumerate(members, 1):
                name = member.name.rsplit("/", 1)[-1]
                stem = name[:-4] if name.endswith(".ogg") else ""
                sound_id = int(stem) if stem.isdigit() else None

                if name.endswith(".ogg"):
                    total_members += 1

                if sound_id is not None and sound_id in prepared:
                    payload = prepared[sound_id].read_bytes()
                    dst_tar.addfile(_tarinfo(name, len(payload)), io.BytesIO(payload))
                    replaced.append(sound_id)
                else:
                    extracted = src_tar.extractfile(member)
                    if extracted is None:
                        continue
                    payload = extracted.read()
                    info = _tarinfo(name, len(payload))
                    info.mtime = member.mtime
                    dst_tar.addfile(info, io.BytesIO(payload))

                if progress:
                    progress(index, total)

            # Ansagen, die es im Original nicht gibt, werden ergänzt.
            for sound_id, path in prepared.items():
                if sound_id in replaced:
                    continue
                payload = path.read_bytes()
                dst_tar.addfile(_tarinfo(f"{sound_id}.ogg", len(payload)), io.BytesIO(payload))
                replaced.append(sound_id)
                warnings.append(
                    t("packer.warning_new_announcement", id=sound_id)
                )
    except tarfile.TarError as exc:
        tmp_path.unlink(missing_ok=True)
        raise PackError(t("packer.archive_write_failed_title"),
                        t("packer.archive_write_failed_details", details=exc)) from exc
    except OSError as exc:
        tmp_path.unlink(missing_ok=True)
        raise PackError(t("packer.pack_save_failed_title"),
                        t("packer.pack_save_failed_details", details=exc)) from exc

    tmp_path.replace(out_path)

    md5, size = _md5_and_size(out_path)
    log(t("packer.log_done_md5", size=size / (1024 * 1024), md5=md5))

    result = BuildResult(path=out_path, md5=md5, size=size,
                         replaced=sorted(replaced), warnings=warnings,
                         total_members=total_members)
    _verify(result, base_pack)
    return result


def _verify(result: BuildResult, base_pack: Path) -> None:
    """Sicherheitsnetz: das fertige Paket muss lesbar und vollständig sein."""
    try:
        with tarfile.open(result.path, "r:gz") as tf:
            names = {m.name for m in tf.getmembers() if m.isfile()}
        with tarfile.open(base_pack, "r:gz") as tf:
            base_names = {m.name for m in tf.getmembers() if m.isfile()}
    except tarfile.TarError as exc:
        raise PackError(
            t("packer.reopen_failed_title"),
            t("packer.reopen_failed_hint", details=exc),
        ) from exc

    missing = base_names - names
    if missing:
        raise PackError(
            t("packer.missing_files_title", count=len(missing)),
            t("packer.missing_files_hint"),
        )


def load_existing(path: Path) -> BuildResult:
    """Nimmt eine bereits vorhandene Paketdatei entgegen und prüft sie.

    Damit lässt sich ein Paket installieren, das anderswo entstanden ist -
    etwa von einem Bekannten weitergegeben oder in einem früheren Durchlauf
    dieser App gebaut.
    """
    path = Path(path)
    if not path.is_file():
        raise PackError(t("packer.file_not_found", path=path))

    try:
        with tarfile.open(path, "r:*") as tf:
            names = [m.name.rsplit("/", 1)[-1] for m in tf.getmembers() if m.isfile()]
    except tarfile.TarError as exc:
        raise PackError(
            t("packer.unreadable_pack_title"),
            t("packer.unreadable_pack_hint", details=exc)) from exc

    sound_ids = sorted(int(n[:-4]) for n in names
                       if n.endswith(".ogg") and n[:-4].isdigit())
    if not sound_ids:
        raise PackError(
            t("packer.no_announcements_title"),
            t("packer.no_announcements_hint"))

    md5, size = _md5_and_size(path)
    warnings: List[str] = []
    if not any(n in METADATA_HINT for n in names):
        warnings.append(t("packer.warning_missing_metadata"))

    return BuildResult(path=path, md5=md5, size=size, replaced=sound_ids,
                       warnings=warnings, total_members=len(sound_ids))


METADATA_HINT = {"voice_mapping.json", "tts.json", "dmr_audio.json",
                 "first_audio.json", "mini_broad.json"}


def _read_ogg_archive(path: Path) -> Dict[str, bytes]:
    """Holt alle `<nummer>.ogg` aus einem tar.gz- oder zip-Archiv.

    Community-Projekte liefern mal ein fertiges tar.gz, mal nur das
    GitHub-Projektarchiv als zip mit den Ogg-Dateien in einem Unterordner.
    Beides wird hier auf dasselbe Ergebnis gebracht: Dateiname -> Inhalt.
    Der Pfad innerhalb des Archivs wird bewusst verworfen, es wird also
    nichts auf die Festplatte entpackt.
    """
    import zipfile

    result: Dict[str, bytes] = {}

    def keep(raw_name: str) -> Optional[str]:
        name = raw_name.replace("\\", "/").rsplit("/", 1)[-1]
        return name if name.endswith(".ogg") and name[:-4].isdigit() else None

    if zipfile.is_zipfile(path):
        try:
            with zipfile.ZipFile(path) as zf:
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    name = keep(info.filename)
                    if name and name not in result:
                        result[name] = zf.read(info)
        except (zipfile.BadZipFile, OSError) as exc:
            raise PackError(t("packer.foreign_pack_not_zip"),
                            t("packer.technical_details", details=exc)) from exc
        return result

    try:
        with tarfile.open(path, "r:*") as tf:
            for member in tf.getmembers():
                if not member.isfile():
                    continue
                name = keep(member.name)
                if name and name not in result:
                    extracted = tf.extractfile(member)
                    if extracted is not None:
                        result[name] = extracted.read()
    except tarfile.TarError as exc:
        raise PackError(
            t("packer.foreign_pack_not_zip_or_targz"),
            t("packer.technical_details", details=exc)) from exc
    return result


def overlay_pack(base_pack: Path, overlay_pack_path: Path,
                 out_name: str = "fremdpaket_angepasst.tar.gz",
                 mapping: Optional[Dict[int, int]] = None,
                 log: LogFn = _noop_log,
                 progress: Optional[ProgressFn] = None) -> BuildResult:
    """Legt ein fremdes Sprachpaket auf das Originalpaket des eigenen Modells.

    Community-Pakete sind meist für ein anderes Modell gebaut und
    enthalten nur Ogg-Dateien ohne die Steuerdateien. Direkt installiert
    fehlen dem Roboter dann Ansagen. Hier werden nur die Audiodateien
    übernommen, alles andere kommt aus dem eigenen Originalpaket.
    """
    if not base_pack.is_file():
        raise PackError(t("packer.overlay_base_missing_title"),
                        t("packer.overlay_base_missing_hint"))

    log(t("packer.log_reading_overlay"))
    overlay = _read_ogg_archive(Path(overlay_pack_path))

    if not overlay:
        raise PackError(t("packer.overlay_empty"))

    log(t("packer.log_overlay_count", count=len(overlay)))

    # Auch hier die Nummern-Umsetzung des Modells beachten.
    if mapping:
        als_pfade = {int(n[:-4]): n for n in overlay}
        for quelle, ziel in sorted(mapping.items()):
            if quelle in als_pfade and ziel not in als_pfade:
                overlay[f"{ziel}.ogg"] = overlay[als_pfade[quelle]]
            elif ziel in als_pfade and quelle not in als_pfade:
                overlay[f"{quelle}.ogg"] = overlay[als_pfade[ziel]]

    out_path = build_dir() / out_name
    tmp_path = out_path.with_suffix(".part")
    replaced: List[int] = []
    total_members = 0
    used: set[str] = set()

    try:
        with tarfile.open(base_pack, "r:gz") as src_tar, \
                tarfile.open(tmp_path, "w:gz", compresslevel=6) as dst_tar:
            members = [m for m in src_tar.getmembers() if m.isfile()]
            for index, member in enumerate(members, 1):
                name = member.name.rsplit("/", 1)[-1]
                if name.endswith(".ogg"):
                    total_members += 1

                if name in overlay:
                    payload = overlay[name]
                    dst_tar.addfile(_tarinfo(name, len(payload)), io.BytesIO(payload))
                    replaced.append(int(name[:-4]))
                    used.add(name)
                else:
                    extracted = src_tar.extractfile(member)
                    if extracted is None:
                        continue
                    payload = extracted.read()
                    info = _tarinfo(name, len(payload))
                    info.mtime = member.mtime
                    dst_tar.addfile(info, io.BytesIO(payload))
                if progress:
                    progress(index, len(members))
    except (tarfile.TarError, OSError) as exc:
        tmp_path.unlink(missing_ok=True)
        raise PackError(t("packer.overlay_build_failed_title"),
                        t("packer.overlay_build_failed_details", details=exc)) from exc

    tmp_path.replace(out_path)
    md5, size = _md5_and_size(out_path)

    warnings: List[str] = []
    unused = len(overlay) - len(used)
    if unused:
        warnings.append(
            t("packer.warning_unused_overlay", count=unused)
        )
    log(t("packer.log_overlay_done", size=size / (1024 * 1024), count=len(replaced)))

    result = BuildResult(path=out_path, md5=md5, size=size, replaced=sorted(replaced),
                         warnings=warnings, total_members=total_members)
    _verify(result, base_pack)
    return result
