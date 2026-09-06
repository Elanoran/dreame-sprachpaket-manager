"""German/English strings for dreamevoice/textfiles.py."""

from ..i18n import register

register({
    "textfiles.kopf": {
        "de": (
            "# {name} - Sprachpaket für Dreame-, MOVA- und Trouver-Saugroboter\n"
            "# {anzahl} Ansagen.\n"
            "#\n"
            "# Die Nummern gelten für alle Modelle: Dreame nutzt eine gemeinsame\n"
            "# Nummerierung, nachgeprüft an acht fremden Modellen. Ansagen, die dein\n"
            "# Roboter nicht kennt, übergeht die App beim Bauen.\n"
            "#\n"
            "# So arbeitest du damit:\n"
            "#   1. Diese Datei komplett kopieren und einer Sprach-KI geben. Ein\n"
            "#      Auftrag, der sich bewährt hat:\n"
            "#\n"
            "#        \"Unten stehen die Ansagen eines Saugroboters auf {name}.\n"
            "#         Bitte überarbeite ausschließlich die dritte Spalte, damit sie\n"
            "#         natürlich und einheitlich klingt. Nummer und Bedeutung\n"
            "#         unverändert lassen, den Aufbau der Zeilen beibehalten und alle\n"
            "#         Zeilen zurückgeben. Die Sätze bleiben kurz und werden\n"
            "#         gesprochen, nicht gelesen.\"\n"
            "#\n"
            "#   2. Die Antwort hier wieder einfügen und die Datei speichern.\n"
            "#   3. In der App auf \"Texte aus Datei einlesen\" klicken.\n"
            "#\n"
            "# Aufbau je Zeile:   Nummer | Bedeutung auf Hochdeutsch | Dialekttext\n"
            "#\n"
            "# Beim Einlesen zählt die Nummer und alles hinter dem zweiten\n"
            "# senkrechten Strich. Zeilen mit # und Leerzeilen werden überlesen.\n"
            "# Zeilen, die du löschst, bleiben unverändert - du kannst also auch\n"
            "# nur einen Teil überarbeiten lassen.\n"
            "#\n"
            "# Halte die Sätze kurz. Die Originalansagen sind zwei bis sechs\n"
            "# Sekunden lang; alles Längere wirkt am Roboter geschwätzig.\n"
        ),
        "en": (
            "# {name} - voice pack for Dreame, MOVA, and Trouver vacuum robots\n"
            "# {anzahl} announcements.\n"
            "#\n"
            "# The numbers apply to all models: Dreame uses a shared numbering scheme,\n"
            "# verified against eight different models. Announcements your robot\n"
            "# doesn't recognize are skipped by the app when building.\n"
            "#\n"
            "# How to work with this:\n"
            "#   1. Copy this whole file and hand it to a language AI. A prompt that\n"
            "#      has worked well:\n"
            "#\n"
            "#        \"Below are the announcements of a vacuum robot in {name}.\n"
            "#         Please rework only the third column so it sounds natural and\n"
            "#         consistent. Leave the number and meaning unchanged, keep the\n"
            "#         line structure, and return every line. Keep the sentences\n"
            "#         short - they're spoken, not read.\"\n"
            "#\n"
            "#   2. Paste the reply back in here and save the file.\n"
            "#   3. Click \"Import Texts from File\" in the app.\n"
            "#\n"
            "# Line format:   Number | Meaning in English | Dialect/custom text\n"
            "#\n"
            "# On import, only the number and everything after the second pipe\n"
            "# character counts. Lines starting with # and blank lines are ignored.\n"
            "# Lines you delete stay unchanged - so you can also have just a part\n"
            "# reworked.\n"
            "#\n"
            "# Keep the sentences short. The original announcements are two to six\n"
            "# seconds long; anything longer sounds chatty on the robot.\n"
        ),
    },
    "textfiles.abschnitt_ansagen": {
        "de": (
            "\n"
            "# ---------------------------------------------------------------------\n"
            "# Ansagen\n"
            "# ---------------------------------------------------------------------\n"
        ),
        "en": (
            "\n"
            "# ---------------------------------------------------------------------\n"
            "# Announcements\n"
            "# ---------------------------------------------------------------------\n"
        ),
    },
    "textfiles.abschnitt_schema": {
        "de": (
            "\n"
            "# ---------------------------------------------------------------------\n"
            "# Schematische Ansagen\n"
            "#\n"
            "# Diese entstehen aus zwei Satzmustern (Akkustand in Prozent,\n"
            "# Bestätigung je Zimmer) und unterscheiden sich nur in einem Wort. Für\n"
            "# eine sprachliche Überarbeitung sind sie meist uninteressant - dann\n"
            "# diesen Abschnitt einfach stehen lassen oder löschen.\n"
            "# ---------------------------------------------------------------------\n"
        ),
        "en": (
            "\n"
            "# ---------------------------------------------------------------------\n"
            "# Schematic announcements\n"
            "#\n"
            "# These are generated from two sentence templates (battery percentage,\n"
            "# per-room confirmation) and differ by only one word. They're usually\n"
            "# uninteresting for a wording rework - just leave this section as is or\n"
            "# delete it.\n"
            "# ---------------------------------------------------------------------\n"
        ),
    },
    "textfiles.summary_lines_read": {
        "de": "{n} Zeilen gelesen",
        "en": "{n} lines read",
    },
    "textfiles.summary_changed": {
        "de": "{n} Texte weichen vom mitgelieferten ab",
        "en": "{n} texts differ from the built-in ones",
    },
    "textfiles.summary_unchanged": {
        "de": "{n} unverändert",
        "en": "{n} unchanged",
    },
    "textfiles.summary_skipped_empty": {
        "de": "{n} ohne Text übersprungen",
        "en": "{n} skipped without text",
    },
    "textfiles.summary_unknown": {
        "de": "{n} unbekannte Nummern",
        "en": "{n} unknown numbers",
    },
})
