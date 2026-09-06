"""German/English strings for ffmpeg_setup.py (ffmpeg auto-download helper)."""

from __future__ import annotations

from ..i18n import register

register({
    "ffmpeg_setup.describe_source": {
        "de": ("ffmpeg wird von GitHub geladen:\n\n{url}\n\n"
               "Das ist das offizielle Windows-Build-Projekt, das auch ffmpeg.org "
               "verlinkt ({project_url}).\n\n"
               "Größe: etwa {size_mb} MB. Aus dem Archiv werden nur "
               "ffmpeg.exe und ffprobe.exe entnommen und in den Datenordner der App "
               "gelegt. Am System wird nichts verändert, es wird nichts installiert "
               "und nichts in die Registry geschrieben.\n\n"
               "Alternative ohne Download: eine vorhandene ffmpeg.exe einfach in den "
               "Ordner dieser App kopieren."),
        "en": ("ffmpeg will be downloaded from GitHub:\n\n{url}\n\n"
               "That's the official Windows build project, also linked by "
               "ffmpeg.org ({project_url}).\n\n"
               "Size: about {size_mb} MB. Only ffmpeg.exe and ffprobe.exe "
               "are extracted from the archive and placed in the app's data "
               "folder. Nothing on the system is changed, nothing is installed, "
               "and nothing is written to the registry.\n\n"
               "Alternative without downloading: just copy an existing "
               "ffmpeg.exe into this app's folder."),
    },

    "ffmpeg_setup.log_downloading_from": {
        "de": "Lade von {url}", "en": "Downloading from {url}",
    },

    "ffmpeg_setup.download_failed_title": {
        "de": "Der Download ist fehlgeschlagen (HTTP {status}).",
        "en": "The download failed (HTTP {status}).",
    },
    "ffmpeg_setup.download_failed_detail": {
        "de": "Quelle: {url}", "en": "Source: {url}",
    },

    "ffmpeg_setup.file_too_large_title": {
        "de": "Die angebotene Datei ist unerwartet groß.",
        "en": "The offered file is unexpectedly large.",
    },
    "ffmpeg_setup.file_too_large_detail": {
        "de": "{size_mb} MB - der Download wurde abgebrochen.",
        "en": "{size_mb} MB - the download was aborted.",
    },

    "ffmpeg_setup.cancelled_by_user": {
        "de": "Vom Benutzer abgebrochen.", "en": "Cancelled by the user.",
    },
    "ffmpeg_setup.download_grew_too_large": {
        "de": "Der Download wurde unerwartet groß und wurde abgebrochen.",
        "en": "The download became unexpectedly large and was aborted.",
    },

    "ffmpeg_setup.download_error_title": {
        "de": "ffmpeg konnte nicht geladen werden.",
        "en": "ffmpeg couldn't be downloaded.",
    },
    "ffmpeg_setup.technical_details_detail": {
        "de": "Technische Details: {error}", "en": "Technical details: {error}",
    },

    "ffmpeg_setup.log_downloaded": {
        "de": "Heruntergeladen: {size_mb} MB", "en": "Downloaded: {size_mb} MB",
    },
    "ffmpeg_setup.log_extracting": {
        "de": "Entnehme ffmpeg.exe und ffprobe.exe ...",
        "en": "Extracting ffmpeg.exe and ffprobe.exe ...",
    },

    "ffmpeg_setup.invalid_archive_title": {
        "de": "Die heruntergeladene Datei ist kein gültiges Archiv.",
        "en": "The downloaded file isn't a valid archive.",
    },

    "ffmpeg_setup.exe_missing_title": {
        "de": "Im Archiv war keine ffmpeg.exe enthalten.",
        "en": "No ffmpeg.exe was in the archive.",
    },
    "ffmpeg_setup.exe_missing_detail": {
        "de": "Gefunden wurde: {found}. Bitte ffmpeg von Hand besorgen und neben die App legen.",
        "en": "Found: {found}. Please get ffmpeg manually and place it next to the app.",
    },
    "ffmpeg_setup.nothing_found": {"de": "nichts", "en": "nothing"},

    "ffmpeg_setup.log_extracted": {
        "de": "Entpackt: {files}", "en": "Extracted: {files}",
    },

    "ffmpeg_setup.exe_wont_start_title": {
        "de": "Die entpackte ffmpeg.exe lässt sich nicht starten.",
        "en": "The extracted ffmpeg.exe won't start.",
    },
    "ffmpeg_setup.exe_error_title": {
        "de": "Die entpackte ffmpeg.exe meldet einen Fehler.",
        "en": "The extracted ffmpeg.exe reports an error.",
    },
    "ffmpeg_setup.ffmpeg_started_fallback": {
        "de": "ffmpeg gestartet", "en": "ffmpeg started",
    },

    "ffmpeg_setup.vorbis_missing_title": {
        "de": "Diesem ffmpeg fehlt der Vorbis-Kodierer (libvorbis).",
        "en": "This ffmpeg is missing the Vorbis encoder (libvorbis).",
    },
    "ffmpeg_setup.vorbis_missing_detail": {
        "de": ("Ohne ihn lassen sich keine Dreame-Sprachpakete erzeugen. "
               "Bitte einen vollständigen ffmpeg-Build verwenden."),
        "en": ("Without it, no Dreame voice packs can be generated. "
               "Please use a complete ffmpeg build."),
    },
    "ffmpeg_setup.log_vorbis_ready": {
        "de": "Vorbis-Kodierer vorhanden - ffmpeg ist einsatzbereit.",
        "en": "Vorbis encoder present - ffmpeg is ready to use.",
    },
})
