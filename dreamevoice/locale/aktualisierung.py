"""German/English strings for aktualisierung.py (self-update mechanism)."""

from __future__ import annotations

from ..i18n import register

register({
    "aktualisierung.no_project_address": {
        "de": "Es ist keine Projektadresse hinterlegt.",
        "en": "No project address is configured.",
    },
    "aktualisierung.no_project_address_hint": {
        "de": "Ohne sie weiß die App nicht, wo sie nachsehen soll.",
        "en": "Without it, the app doesn't know where to look.",
    },
    "aktualisierung.search_failed": {
        "de": "Die Suche nach Aktualisierungen ist fehlgeschlagen.",
        "en": "The search for updates failed.",
    },
    "aktualisierung.search_failed_hint": {
        "de": "Technische Details: {exc}",
        "en": "Technical details: {exc}",
    },
    "aktualisierung.github_http_error": {
        "de": "GitHub antwortete mit HTTP {status}.",
        "en": "GitHub responded with HTTP {status}.",
    },
    "aktualisierung.github_http_error_hint": {
        "de": "Versuche es später noch einmal, oder sieh auf der Projektseite selbst nach.",
        "en": "Try again later, or check the project page yourself.",
    },
    "aktualisierung.github_unreadable": {
        "de": "Die Antwort von GitHub war nicht lesbar.",
        "en": "GitHub's response was unreadable.",
    },
    "aktualisierung.github_unreadable_hint": {
        "de": "Technische Details: {exc}",
        "en": "Technical details: {exc}",
    },
    "aktualisierung.version_no_file": {
        "de": "Version {version} ist da, aber ohne Programmdatei.",
        "en": "Version {version} is available, but without a program file.",
    },
    "aktualisierung.version_no_file_hint": {
        "de": (
            "Vermutlich wird sie gerade hochgeladen. Sieh in ein paar "
            "Minuten noch einmal nach, oder hol sie dir hier:\n{url}"
        ),
        "en": (
            "It's probably still being uploaded. Check again in a few "
            "minutes, or get it here:\n{url}"
        ),
    },
    "aktualisierung.no_checksum": {
        "de": "Zu dieser Fassung liegt keine Prüfsumme vor.",
        "en": "No checksum is available for this version.",
    },
    "aktualisierung.no_checksum_hint": {
        "de": (
            "Ohne sie wird nichts ausgetauscht. Lade die Datei von der "
            "Projektseite und ersetze sie von Hand."
        ),
        "en": (
            "Nothing will be replaced without it. Download the file from "
            "the project page and replace it manually."
        ),
    },
    "aktualisierung.running_from_source": {
        "de": "Die App läuft aus dem Quellcode.",
        "en": "The app is running from source.",
    },
    "aktualisierung.running_from_source_hint": {
        "de": (
            "Ein Austausch der Programmdatei ergibt hier keinen Sinn - "
            "hol dir die neue Fassung über git."
        ),
        "en": (
            "Replacing the program file doesn't make sense here - "
            "get the new version via git."
        ),
    },
    "aktualisierung.source_not_allowed": {
        "de": "Die Bezugsadresse der neuen Fassung ist nicht zulässig.",
        "en": "The new version's source address isn't allowed.",
    },
    "aktualisierung.source_not_allowed_hint": {
        "de": (
            "Erwartet wird eine gesicherte Adresse bei GitHub, "
            "angegeben war:\n{url}\n\nEs wurde nichts geladen."
        ),
        "en": (
            "A secure GitHub address was expected, but got:\n"
            "{url}\n\nNothing was downloaded."
        ),
    },
    "aktualisierung.download_failed": {
        "de": "Der Download ist fehlgeschlagen (HTTP {status}).",
        "en": "The download failed (HTTP {status}).",
    },
    "aktualisierung.download_failed_hint": {
        "de": "Quelle: {url}",
        "en": "Source: {url}",
    },
    "aktualisierung.cancelled": {
        "de": "Vom Benutzer abgebrochen.",
        "en": "Cancelled by the user.",
    },
    "aktualisierung.file_too_large": {
        "de": "Die Datei ist unerwartet groß.",
        "en": "The file is unexpectedly large.",
    },
    "aktualisierung.file_too_large_hint": {
        "de": "Der Download wurde abgebrochen.",
        "en": "The download was aborted.",
    },
    "aktualisierung.download_interrupted": {
        "de": "Der Download ist abgebrochen.",
        "en": "The download was interrupted.",
    },
    "aktualisierung.download_interrupted_hint": {
        "de": "Technische Details: {exc}",
        "en": "Technical details: {exc}",
    },
    "aktualisierung.checksum_mismatch": {
        "de": "Die heruntergeladene Datei stimmt nicht mit der Prüfsumme überein.",
        "en": "The downloaded file doesn't match the checksum.",
    },
    "aktualisierung.checksum_mismatch_hint": {
        "de": "Erwartet {expected}…, erhalten {got}…. Es wurde nichts ausgetauscht.",
        "en": "Expected {expected}…, got {got}…. Nothing was replaced.",
    },
    "aktualisierung.no_exe_to_replace": {
        "de": "Es gibt keine Programmdatei zum Austauschen.",
        "en": "There's no program file to replace.",
    },
    "aktualisierung.new_version_not_found": {
        "de": "Die neue Fassung wurde nicht gefunden.",
        "en": "The new version wasn't found.",
    },
    "aktualisierung.checksum_changed": {
        "de": "Die vorbereitete Datei hat sich seit der Prüfung veraendert.",
        "en": "The prepared file has changed since it was checked.",
    },
    "aktualisierung.checksum_changed_hint": {
        "de": "Sie wurde verworfen, es wurde nichts ausgetauscht. Versuche es erneut.",
        "en": "It was discarded, nothing was replaced. Try again.",
    },
    "aktualisierung.old_version_locked": {
        "de": "Die vorige Fassung lässt sich nicht beiseiteräumen.",
        "en": "The previous version can't be set aside.",
    },
    "aktualisierung.old_version_locked_hint": {
        "de": (
            "Vermutlich läuft sie noch oder wird von einem anderen "
            "Programm festgehalten. Schließe sie und versuche es erneut - "
            "oder lösche die Datei von Hand:\n{path}\n\n"
            "Technische Details: {exc}"
        ),
        "en": (
            "It's probably still running or held open by another "
            "program. Close it and try again - or delete the file "
            "manually:\n{path}\n\n"
            "Technical details: {exc}"
        ),
    },
    "aktualisierung.swap_stuck": {
        "de": "Die Aktualisierung ist mitten im Austausch steckengeblieben.",
        "en": "The update got stuck in the middle of replacing the file.",
    },
    "aktualisierung.swap_stuck_hint": {
        "de": (
            "Am gewohnten Platz liegt gerade KEINE startfähige "
            "Programmdatei. So bekommst du sie zurück: Benenne\n"
            "  {alt_name}\n"
            "wieder in\n  {exe_name}\n"
            "um. Beide liegen in:\n{parent}\n\n"
            "Technische Details: {exc1} / {exc2}"
        ),
        "en": (
            "There is currently NO runnable program file in the "
            "usual place. Here's how to get it back: rename\n"
            "  {alt_name}\n"
            "back to\n  {exe_name}\n"
            "Both are in:\n{parent}\n\n"
            "Technical details: {exc1} / {exc2}"
        ),
    },
})
