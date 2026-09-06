"""German/English strings for audio.py (ffmpeg wrapper)."""

from __future__ import annotations

from ..i18n import register

register({
    "audio.channel_count": {
        "de": "{codec}, {channels} Kanal/Kanäle, {rate} Hz",
        "en": "{codec}, {channels} channel(s), {rate} Hz",
    },
    "audio.ffmpeg_not_found": {
        "de": "ffmpeg wurde nicht gefunden.",
        "en": "ffmpeg wasn't found.",
    },
    "audio.ffmpeg_not_found_hint": {
        "de": (
            "ffmpeg wird gebraucht, um deine Audiodatei in das Format zu "
            "bringen, das der Roboter versteht (OGG Vorbis, mono, 16 kHz). "
            "Lege ffmpeg.exe einfach neben die App - oder wähle bereits "
            "passend vorbereitete .ogg-Dateien aus."
        ),
        "en": (
            "ffmpeg is needed to bring your audio file into the format "
            "the robot understands (OGG Vorbis, mono, 16 kHz). Just place "
            "ffmpeg.exe next to the app - or choose .ogg files that are "
            "already in the right format."
        ),
    },
    "audio.file_not_found": {
        "de": "Die Datei wurde nicht gefunden:\n{path}",
        "en": "The file wasn't found:\n{path}",
    },
    "audio.conversion_too_slow": {
        "de": "Die Umwandlung von {name} hat zu lange gedauert.",
        "en": "Converting {name} took too long.",
    },
    "audio.ffmpeg_start_failed": {
        "de": "ffmpeg konnte nicht gestartet werden: {exc}",
        "en": "ffmpeg couldn't be started: {exc}",
    },
    "audio.conversion_failed": {
        "de": "Die Datei {name} konnte nicht umgewandelt werden.",
        "en": "The file {name} couldn't be converted.",
    },
    "audio.conversion_failed_hint": {
        "de": (
            "ffmpeg hat keine Begründung geliefert. Ist die Datei "
            "vielleicht beschädigt oder gar keine Audiodatei?"
        ),
        "en": (
            "ffmpeg gave no explanation. Is the file perhaps "
            "damaged, or not an audio file at all?"
        ),
    },
    "audio.result_not_vorbis": {
        "de": "Das Ergebnis für {name} ist kein OGG Vorbis.",
        "en": "The result for {name} isn't OGG Vorbis.",
    },
    "audio.result_not_vorbis_hint": {
        "de": (
            "Vermutlich fehlt deinem ffmpeg der Vorbis-Encoder (libvorbis). "
            "Nutze einen vollständigen ffmpeg-Build."
        ),
        "en": (
            "Your ffmpeg is probably missing the Vorbis encoder "
            "(libvorbis). Use a complete ffmpeg build."
        ),
    },
    "audio.file_too_large": {
        "de": "{name} ist mit {size} KB sehr groß.",
        "en": "{name} is very large at {size} KB.",
    },
    "audio.file_too_large_hint": {
        "de": (
            "Ansagen des Roboters sind nur wenige Sekunden lang. Bitte kürze "
            "die Datei, bevor du sie verwendest."
        ),
        "en": (
            "The robot's announcements are only a few seconds long. "
            "Please trim the file before using it."
        ),
    },
    "audio.nothing_to_combine": {
        "de": "Es gibt nichts zusammenzufügen.",
        "en": "There's nothing to combine.",
    },
    "audio.format_not_supported": {
        "de": (
            "Das Format {suffix} ist nicht vorgesehen. Erwartet werden "
            "z. B. {examples}."
        ),
        "en": (
            "The format {suffix} isn't supported. Expected are e.g. "
            "{examples}."
        ),
    },
    "audio.file_very_large_short": {
        "de": "Die Datei ist sehr groß - Ansagen sollten nur Sekunden dauern.",
        "en": "The file is very large - announcements should only be seconds long.",
    },
    "audio.will_convert": {
        "de": (
            "Die Datei ist {description}. Sie wird beim Bauen "
            "automatisch nach mono/16000 Hz umgewandelt."
        ),
        "en": (
            "The file is {description}. It will be converted "
            "to mono/16000 Hz automatically when building."
        ),
    },
    "audio.not_valid_ogg": {
        "de": "Die Datei sieht nicht wie eine gültige Ogg-Datei aus.",
        "en": "The file doesn't look like a valid Ogg file.",
    },
    "audio.no_extension": {
        "de": "(ohne Endung)",
        "en": "(no extension)",
    },
})
