"""German/English strings for ui/tab_connect.py ('Connection')."""

from __future__ import annotations

from ..i18n import register

register({
    "tab_connect.info_banner": {
        "de": ("Die App meldet sich mit denselben Zugangsdaten an, die du in "
               "deiner Handy-App benutzt - Dreamehome, MOVA Home oder Trouver. "
               "Welche es ist, stellst du unten unter 'App' ein. Die Daten gehen "
               "ausschließlich an Dreame (MOVA und Trouver gehören dazu), nicht "
               "an Dritte. Ohne Anmeldung kennt die App weder dein Robotermodell "
               "noch kann sie ihm etwas schicken."),
        "en": ("The app signs in with the same credentials you use in your "
               "phone app - Dreamehome, MOVA Home, or Trouver. You set which "
               "one below under 'App'. The data goes exclusively to Dreame "
               "(MOVA and Trouver belong to it), never to third parties. "
               "Without signing in, the app knows neither your robot's model "
               "nor can it send it anything."),
    },
    "tab_connect.account_card_title": {
        "de": "Herstellerkonto", "en": "Manufacturer Account",
    },
    "tab_connect.account_card_desc": {
        "de": "E-Mail und Passwort wie in deiner Hersteller-App.",
        "en": "Email and password, same as in your manufacturer app.",
    },
    "tab_connect.email_label": {"de": "E-Mail", "en": "Email"},
    "tab_connect.password_label": {"de": "Passwort", "en": "Password"},
    "tab_connect.show_password_check": {"de": "zeigen", "en": "show"},
    "tab_connect.autoregion_check": {
        "de": "automatisch suchen", "en": "detect automatically",
    },
    "tab_connect.remember_password_check": {
        "de": "Passwort auf diesem PC merken", "en": "Remember password on this PC",
    },
    "tab_connect.remember_password_windows_only": {
        "de": "(nur unter Windows verfügbar)", "en": "(only available on Windows)",
    },
    "tab_connect.remember_password_encrypted": {
        "de": "(verschlüsselt mit deinem Windows-Konto)",
        "en": "(encrypted with your Windows account)",
    },
    "tab_connect.login_button": {
        "de": "Anmelden und Roboter suchen", "en": "Sign In and Find Robot",
    },
    "tab_connect.status_not_signed_in": {
        "de": "Nicht angemeldet", "en": "Not signed in",
    },
    "tab_connect.devices_card_title": {
        "de": "Gefundene Roboter", "en": "Robots Found",
    },
    "tab_connect.devices_card_desc": {
        "de": "Wähle den Roboter aus, dessen Stimme du ändern willst.",
        "en": "Choose the robot whose voice you want to change.",
    },
    "tab_connect.column_model": {"de": "Modell", "en": "Model"},
    "tab_connect.column_device_id": {"de": "Geräte-ID", "en": "Device ID"},
    "tab_connect.no_robots_placeholder": {
        "de": "Noch keine Roboter geladen - melde dich oben an.",
        "en": "No robots loaded yet - sign in above.",
    },
    "tab_connect.details_card_title": {
        "de": "Ausgewählter Roboter", "en": "Selected Robot",
    },
    "tab_connect.model_identifier_label": {
        "de": "Modell-Kennung", "en": "Model Identifier",
    },
    "tab_connect.device_id_label": {"de": "Geräte-ID (did)", "en": "Device ID (did)"},
    "tab_connect.mac_address_label": {"de": "MAC-Adresse", "en": "MAC Address"},
    "tab_connect.active_voice_pack_label": {
        "de": "Aktives Sprachpaket", "en": "Active Voice Pack",
    },
    "tab_connect.no_token_note": {
        "de": ("Kein lokales Token? Das ist richtig so. Modelle, die in der "
               "Dreamehome-App laufen - wie der X50 Ultra - bieten im Heimnetz "
               "keinen direkten Zugang mehr an und geben auch kein 32-stelliges "
               "miio-Token heraus. Befehle laufen über die Dreame-Cloud, das "
               "Sprachpaket selbst holt sich der Roboter danach direkt von "
               "diesem PC."),
        "en": ("No local token? That's correct. Models running in the "
               "Dreamehome app - like the X50 Ultra - no longer offer "
               "direct access on the home network and don't hand out a "
               "32-character miio token either. Commands go through the "
               "Dreame cloud; the robot then fetches the voice pack "
               "itself, directly from this PC."),
    },
    "tab_connect.open_help_page_button": {
        "de": "Dreame-Hilfeseite öffnen", "en": "Open Dreame Help Page",
    },
    "tab_connect.updates_card_title": {"de": "Aktualisierung", "en": "Updates"},
    "tab_connect.updates_card_desc": {
        "de": "Nachsehen, ob es eine neuere Fassung gibt",
        "en": "Check whether a newer version is available",
    },
    "tab_connect.updates_version_note": {
        "de": ("Diese Fassung: {version}\n\n"
               "Das Nachsehen und der Schalter 'beim Start nachsehen' "
               "stehen jetzt oben rechts unter 'Aktualisierung'."),
        "en": ("This version: {version}\n\n"
               "The check and the 'check on startup' switch now live "
               "top right under 'Updates'."),
    },
    "tab_connect.open_updates_button": {
        "de": "Aktualisierung öffnen ...", "en": "Open Updates ...",
    },
    "tab_connect.share_card_title": {"de": "App weitergeben", "en": "Share the App"},
    "tab_connect.share_card_desc": {
        "de": "Persönliche Spuren entfernen, bevor jemand anderes sie bekommt",
        "en": "Remove personal traces before someone else gets it",
    },
    "tab_connect.share_details_1": {
        "de": ("Dein Passwort und der ElevenLabs-Schlüssel liegen im "
               "Windows-Anmeldeinformationsspeicher, nicht in einer Datei - "
               "die wandern beim Kopieren also gar nicht erst mit.\n\n"
               "Im Datenordner steht trotzdem einiges, was auf dich zeigt: "
               "deine E-Mail-Adresse, Name, Geräte-ID und MAC deines "
               "Roboters, die IP dieses PCs, die zuletzt benutzte "
               "ElevenLabs-Stimme und das Protokoll. Der Knopf löscht "
               "genau das."),
        "en": ("Your password and ElevenLabs key live in the Windows "
               "Credential Manager, not in a file - so they don't travel "
               "along when you copy things.\n\n"
               "The data folder still holds a fair bit that points to "
               "you: your email address, your robot's name, device ID, "
               "and MAC address, this PC's IP, the last-used ElevenLabs "
               "voice, and the log. This button removes exactly that."),
    },
    "tab_connect.share_details_2": {
        "de": ("Deine gebauten Sprachpakete, die Dialekttexte und die "
               "mitgelieferten Aufnahmen bleiben erhalten - da steckt nichts "
               "Persönliches drin."),
        "en": ("Your built voice packs, the dialect texts, and the "
               "bundled recordings are kept - there's nothing personal "
               "in those."),
    },
    "tab_connect.remove_personal_button": {
        "de": "Persönliche Daten entfernen ...", "en": "Remove Personal Data ...",
    },
    "tab_connect.forget_confirm_title": {
        "de": "Persönliche Daten entfernen?", "en": "Remove Personal Data?",
    },
    "tab_connect.forget_confirm_message": {
        "de": ("Entfernt werden:\n\n"
               "  • E-Mail-Adresse und gespeichertes Passwort\n"
               "  • der ElevenLabs-Schlüssel\n"
               "  • Name, Geräte-ID und MAC deines Roboters\n"
               "  • die IP-Adresse dieses PCs\n"
               "  • die zuletzt benutzte ElevenLabs-Stimme\n"
               "  • das Protokoll\n\n"
               "Deine gebauten Sprachpakete und Dialekttexte bleiben.\n\n"
               "Beim nächsten Start musst du dich neu anmelden. "
               "Fortfahren?"),
        "en": ("This removes:\n\n"
               "  • Email address and saved password\n"
               "  • The ElevenLabs key\n"
               "  • Your robot's name, device ID, and MAC address\n"
               "  • This PC's IP address\n"
               "  • The last-used ElevenLabs voice\n"
               "  • The log\n\n"
               "Your built voice packs and dialect texts stay.\n\n"
               "You'll need to sign in again next time. "
               "Continue?"),
    },
    "tab_connect.forget_removed_count": {
        "de": "{count} Angaben entfernt.", "en": "{count} items removed.",
    },
    "tab_connect.forget_nothing_removed": {
        "de": "Es war nichts zu entfernen.", "en": "There was nothing to remove.",
    },
    "tab_connect.forget_done_details": {
        "de": ("Die App lässt sich jetzt samt Datenordner weitergeben, "
               "ohne dass etwas über dich mitgeht."),
        "en": ("You can now share the app along with its data "
               "folder without anything about you tagging along."),
    },
    "tab_connect.forget_removed_prefix": {
        "de": "\n\nEntfernt: ", "en": "\n\nRemoved: ",
    },
    "tab_connect.forget_done_title": {"de": "Erledigt", "en": "Done"},
    "tab_connect.last_saved_robot_badge": {
        "de": "Zuletzt gespeicherter Roboter geladen", "en": "Last saved robot loaded",
    },
    "tab_connect.missing_info_title": {
        "de": "Angaben fehlen", "en": "Missing Information",
    },
    "tab_connect.missing_info_message": {
        "de": "Bitte E-Mail und Passwort eintragen.",
        "en": "Please enter email and password.",
    },
    "tab_connect.signing_in_badge": {"de": "Melde an ...", "en": "Signing in ..."},
    "tab_connect.no_vacuum_badge": {
        "de": "Angemeldet, aber kein Saugroboter gefunden",
        "en": "Signed in, but no vacuum robot found",
    },
    "tab_connect.no_vacuum_message": {
        "de": ("In diesem Konto ist kein Saugroboter hinterlegt. "
               "Prüfe, ob du dieselbe E-Mail wie in deiner "
               "Hersteller-App nutzt und ob der Roboter dort "
               "auftaucht."),
        "en": ("No vacuum robot is registered in this account. "
               "Check that you're using the same email as in "
               "your manufacturer app and that the robot shows "
               "up there."),
    },
    "tab_connect.last_used_robot_message": {
        "de": ("Der zuletzt benutzte Roboter steht unten. Für die "
               "vollständige Liste oben anmelden."),
        "en": ("The last-used robot is shown below. Sign in "
               "above for the full list."),
    },
    "tab_connect.signed_in_count_badge": {
        "de": "Angemeldet{region} - {count} Roboter gefunden",
        "en": "Signed in{region} - {count} robots found",
    },
    "tab_connect.login_failed": {
        "de": "Anmeldung fehlgeschlagen", "en": "Sign-in Failed",
    },
    "tab_connect.device_checking": {"de": "wird abgefragt ...", "en": "checking ..."},
    "tab_connect.voice_unknown": {"de": "unbekannt", "en": "unknown"},
    "tab_connect.voice_unavailable": {
        "de": "nicht abfragbar (Roboter im Standby?)",
        "en": "not available (robot asleep?)",
    },
    "tab_connect.require_device_message": {
        "de": "Es ist kein Roboter ausgewählt.", "en": "No robot is selected.",
    },
    "tab_connect.require_device_hint": {
        "de": "Melde dich unter 'Verbindung' an und wähle deinen Roboter.",
        "en": "Sign in under 'Connection' and choose your robot.",
    },
})
