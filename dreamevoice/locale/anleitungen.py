"""German/English strings for anleitungen.py (Help window guide pages)."""

from __future__ import annotations

from ..i18n import register

register({
    "anleitungen.problemloesung_titel": {
        "de": "Wenn etwas nicht klappt",
        "en": "When Something Doesn't Work",
    },
    "anleitungen.problemloesung_inhalt": {
        "de": (
            "Der Roboter holt das Paket nicht ab, die Anmeldung "
            "scheitert, die Stimme ist zu leise."
        ),
        "en": (
            "The robot doesn't pick up the pack, sign-in fails, the "
            "voice is too quiet."
        ),
    },
    "anleitungen.modelle_titel": {
        "de": "Welche Roboter funktionieren",
        "en": "Which Robots Work",
    },
    "anleitungen.modelle_inhalt": {
        "de": (
            "Geprüfte Modelle und woran man erkennt, ob der eigene "
            "dazugehört."
        ),
        "en": (
            "Verified models and how to tell whether yours is one of "
            "them."
        ),
    },
    "anleitungen.sicherheit_titel": {
        "de": "Warum das den Roboter nicht beschädigt",
        "en": "Why This Doesn't Damage the Robot",
    },
    "anleitungen.sicherheit_inhalt": {
        "de": (
            "Was die App anfasst, was sie nicht anfasst und wie der "
            "Rückweg aussieht."
        ),
        "en": (
            "What the app touches, what it doesn't, and what the way "
            "back looks like."
        ),
    },
    "anleitungen.eigene_stimmen_titel": {
        "de": "Eigene Stimmen und Dialekte",
        "en": "Custom Voices and Dialects",
    },
    "anleitungen.eigene_stimmen_inhalt": {
        "de": (
            "Eigene Texte, eigene Aufnahmen, Windows-Sprachausgabe "
            "und ElevenLabs."
        ),
        "en": (
            "Your own text, your own recordings, Windows text-to-speech "
            "and ElevenLabs."
        ),
    },
    "anleitungen.technik_titel": {
        "de": "Technische Hintergründe",
        "en": "Technical Background",
    },
    "anleitungen.technik_inhalt": {
        "de": (
            "Paketformat, Cloud-Befehle und was beim Aufspielen "
            "wirklich passiert."
        ),
        "en": (
            "Package format, cloud commands, and what really happens "
            "during install."
        ),
    },
    "anleitungen.entwicklung_titel": {
        "de": "Entwicklung",
        "en": "Development",
    },
    "anleitungen.entwicklung_inhalt": {
        "de": "Aus dem Quellcode starten, Selbsttest, EXE bauen.",
        "en": "Running from source, self-test, building the EXE.",
    },
})
