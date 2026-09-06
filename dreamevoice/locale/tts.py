"""German/English strings for dreamevoice/tts.py."""

from ..i18n import register

register({
    "tts.gender_male": {
        "de": "männlich",
        "en": "male",
    },
    "tts.gender_female": {
        "de": "weiblich",
        "en": "female",
    },
    "tts.err_windows_only_msg": {
        "de": "Sprachsynthese ist nur unter Windows verfügbar.",
        "en": "Speech synthesis is only available on Windows.",
    },
    "tts.err_windows_only_hint": {
        "de": "Auf diesem System lässt sich kein Paket automatisch erzeugen. "
              "Du kannst Ansagen aber selbst aufnehmen und zuweisen.",
        "en": "No pack can be generated automatically on this system. "
              "You can, however, record and assign announcements yourself.",
    },
    "tts.err_no_texts": {
        "de": "Es wurden keine Texte übergeben.",
        "en": "No texts were provided.",
    },
    "tts.err_no_voice_msg": {
        "de": "Es ist keine deutsche Sprachausgabe-Stimme installiert.",
        "en": "No German text-to-speech voice is installed.",
    },
    "tts.err_no_voice_hint": {
        "de": "Windows-Einstellungen > Zeit und Sprache > Sprache > Deutsch > "
              "Optionen > Sprachausgabe hinzufügen. Danach die App neu starten.",
        "en": "Windows Settings > Time and Language > Language > German > "
              "Options > Add speech. Then restart the app.",
    },
    "tts.err_timeout": {
        "de": "Die Sprachsynthese hat zu lange gedauert.",
        "en": "Speech synthesis took too long.",
    },
    "tts.err_could_not_start_msg": {
        "de": "Die Sprachsynthese konnte nicht gestartet werden.",
        "en": "Speech synthesis couldn't be started.",
    },
    "tts.err_technical_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "tts.err_failed_msg": {
        "de": "Die Sprachsynthese ist fehlgeschlagen.",
        "en": "Speech synthesis failed.",
    },
    "tts.err_no_files_produced": {
        "de": "Es wurde keine einzige Sprachdatei erzeugt.",
        "en": "Not a single audio file was produced.",
    },
    "tts.log_chosen_voice": {
        "de": "Stimme: {voice}",
        "en": "Voice: {voice}",
    },
    "tts.log_spoken_summary": {
        "de": "{count} von {total} Ansagen gesprochen.",
        "en": "{count} of {total} announcements spoken.",
    },
})
