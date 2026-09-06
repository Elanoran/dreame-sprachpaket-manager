"""German/English strings for dreamevoice/dialect.py.

Scope: the user-facing strings in that module - the Windows-voice note
shown per dialect, the progress-log lines passed to `log()`, and the
error/warning messages raised or appended for the user to see.
"""

from __future__ import annotations

from ..i18n import register

register({
    "dialect.note_windows": {
        "de": (
            "Mit der Windows-Stimme steckt der Dialekt nur in Wortwahl und "
            "Schreibweise - die Aussprache bleibt hochdeutsch. Für echten Dialekt "
            "unten auf ElevenLabs umschalten."
        ),
        "en": (
            "With the Windows voice, the dialect only lives in the wording and "
            "spelling - the pronunciation stays standard German. For genuine "
            "dialect, switch to ElevenLabs below."
        ),
    },
    "dialect.err_base_pack_missing_message": {
        "de": "Das Originalpaket deines Roboters fehlt.",
        "en": "Your robot's original pack is missing.",
    },
    "dialect.err_base_pack_missing_hint": {
        "de": "Lade es unter 'Einzelne Ansagen' herunter - es ist die Grundlage jedes Pakets.",
        "en": "Download it under 'Individual Announcements' - it's the foundation of every pack.",
    },
    "dialect.err_ffmpeg_missing_message": {
        "de": "Für die Umwandlung wird ffmpeg gebraucht.",
        "en": "ffmpeg is needed for the conversion.",
    },
    "dialect.err_ffmpeg_missing_hint": {
        "de": (
            "Richte ffmpeg unter 'Einzelne Ansagen' ein - ohne den Vorbis-Kodierer lässt sich "
            "aus der Sprachausgabe kein Sprachpaket bauen."
        ),
        "en": (
            "Set up ffmpeg under 'Individual Announcements' - without the Vorbis "
            "encoder, no voice pack can be built from the speech output."
        ),
    },
    "dialect.log_unsupported_skipped": {
        "de": "{count} Ansagen gibt es bei diesem Modell nicht und werden übersprungen.",
        "en": "{count} announcements don't exist on this model and will be skipped.",
    },
    "dialect.log_recordings_adopted": {
        "de": (
            "{count} vorhandene Aufnahmen ohne Herkunftsvermerk übernommen "
            "(z. B. aus einer Sicherung) - sie werden nicht neu gesprochen."
        ),
        "en": (
            "{count} existing recordings without a manifest entry taken over "
            "(e.g. from a backup) - they won't be re-spoken."
        ),
    },
    "dialect.log_recordings_stale": {
        "de": "{count} Aufnahmen gehören zu einem inzwischen geänderten Text und werden neu gesprochen.",
        "en": "{count} recordings belong to text that has since changed and will be re-spoken.",
    },
    "dialect.log_existing_and_remaining": {
        "de": "{existing} Ansagen liegen schon vor, {remaining} sind zu sprechen.",
        "en": "{existing} announcements already exist, {remaining} need to be spoken.",
    },
    "dialect.log_speaking_start": {
        "de": "Spreche {remaining} von {total} Ansagen auf {name} ...",
        "en": "Speaking {remaining} of {total} announcements for {name} ...",
    },
    "dialect.log_all_exist": {
        "de": "Alle Ansagen liegen bereits vor - es wird nichts neu gesprochen.",
        "en": "All announcements already exist - nothing new will be spoken.",
    },
    "dialect.log_speech_service_elevenlabs": {
        "de": "Sprachdienst: ElevenLabs ({chars} Zeichen)",
        "en": "Speech service: ElevenLabs ({chars} characters)",
    },
    "dialect.err_cancelled": {
        "de": "Vom Benutzer abgebrochen.",
        "en": "Cancelled by the user.",
    },
    "dialect.log_converting": {
        "de": "Wandle in das Format des Roboters um (OGG Vorbis, mono, 16 kHz) ...",
        "en": "Converting to the robot's format (OGG Vorbis, mono, 16 kHz) ...",
    },
    "dialect.log_converted_count": {
        "de": "{count} Ansagen umgewandelt.",
        "en": "{count} announcements converted.",
    },
    "dialect.log_missing_note": {
        "de": "Hinweis: {count} Ansagen fehlen noch und bleiben auf der deutschen Originalstimme.",
        "en": "Note: {count} announcements are still missing and stay on the German original voice.",
    },
    "dialect.warning_incomplete": {
        "de": (
            "{missing} von {total} Ansagen konnten nicht gesprochen werden und "
            "bleiben Hochdeutsch. Starte die Erzeugung später einfach erneut - "
            "die App macht dort weiter, wo sie aufgehört hat."
        ),
        "en": (
            "{missing} of {total} announcements couldn't be spoken and stay in "
            "standard German. Just start generating again later - the app picks "
            "up where it left off."
        ),
    },
    "dialect.log_done": {
        "de": "Fertig: {summary}",
        "en": "Done: {summary}",
    },
    "dialect.err_text_empty": {
        "de": "Der Text ist leer.",
        "en": "The text is empty.",
    },
    "dialect.err_sentence_failed": {
        "de": "Der Satz konnte nicht gesprochen werden.",
        "en": "The sentence couldn't be spoken.",
    },
    "dialect.err_no_samples": {
        "de": "Für diesen Dialekt gibt es keine Beispielsätze.",
        "en": "There are no sample sentences for this dialect.",
    },
    "dialect.log_sample_elevenlabs": {
        "de": "Hörprobe über ElevenLabs ({chars} Zeichen)",
        "en": "Sample via ElevenLabs ({chars} characters)",
    },
    "dialect.log_sample_windows": {
        "de": "Hörprobe über die Windows-Sprachausgabe",
        "en": "Sample via the Windows text-to-speech voice",
    },
    "dialect.log_sample_combined": {
        "de": "{count} Sätze zu einer Hörprobe zusammengefügt.",
        "en": "{count} sentences combined into one sample.",
    },
    "dialect.log_sample_combine_failed": {
        "de": "Sätze konnten nicht zusammengefügt werden - es läuft nur der erste.",
        "en": "Sentences couldn't be combined - only the first one will play.",
    },
})
