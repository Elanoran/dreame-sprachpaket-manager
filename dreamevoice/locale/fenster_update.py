from ..i18n import register

register({
    "fenster_update.window_title": {
        "de": "Aktualisierung",
        "en": "Updates",
    },
    "fenster_update.close_button": {
        "de": "Schließen",
        "en": "Close",
    },
    "fenster_update.card_title": {
        "de": "Aktualisierung",
        "en": "Updates",
    },
    "fenster_update.card_subtitle": {
        "de": "Nachsehen, ob es eine neuere Fassung gibt",
        "en": "Check whether a newer version is available",
    },
    "fenster_update.version_info": {
        "de": ("Diese Fassung: {version}\n\n"
               "Die App fragt bei GitHub nach der neuesten Fassung. Dabei "
               "wird nichts über dich oder deinen Roboter übermittelt - "
               "aber wie bei jedem Seitenaufruf sieht die Gegenseite deine "
               "IP-Adresse. Deshalb ist die Abfrage ausgeschaltet, solange "
               "du sie nicht einschaltest."),
        "en": ("This version: {version}\n\n"
               "The app asks GitHub for the latest version. This doesn't "
               "transmit anything about you or your robot - but as with "
               "any page request, the other side sees your IP address. "
               "That's why the check is off until you turn it on."),
    },
    "fenster_update.checkbox_startup": {
        "de": "Beim Start nachsehen, ob es eine neuere Fassung gibt",
        "en": "Check for a newer version on startup",
    },
    "fenster_update.check_now_button": {
        "de": "Jetzt nach Aktualisierung suchen",
        "en": "Check for Updates Now",
    },
    "fenster_update.auto_install_note": {
        "de": ("Gefunden wird nichts von selbst installiert. Die App zeigt, "
               "was neu ist, und fragt. Erst dann lädt sie die neue Datei, "
               "prüft ihre Prüfsumme und ersetzt sich selbst - ohne "
               "Installation, ohne Administratorrechte. Dein Datenordner "
               "bleibt unberührt."),
        "en": ("Nothing found gets installed automatically. The app shows "
               "what's new and asks first. Only then does it download the "
               "new file, verify its checksum, and replace itself - no "
               "installer, no admin rights needed. Your data folder stays "
               "untouched."),
    },
    "fenster_update.status_checking": {
        "de": "Sehe nach ...",
        "en": "Checking ...",
    },
    "fenster_update.status_latest": {
        "de": "{version} ist die neueste Fassung.",
        "en": "{version} is the latest version.",
    },
    "fenster_update.status_version_available": {
        "de": "Version {version} ist da.",
        "en": "Version {version} is available.",
    },
    "fenster_update.check_failed_title": {
        "de": "Suche fehlgeschlagen",
        "en": "Check Failed",
    },
    "fenster_update.version_available_title": {
        "de": "Version {version} ist da",
        "en": "Version {version} is available",
    },
    "fenster_update.source_run_message": {
        "de": "Diese App läuft aus dem Quellcode - ein Austausch der "
              "Programmdatei ergibt hier keinen Sinn.",
        "en": "This app is running from source - replacing the "
              "program file doesn't make sense here.",
    },
    "fenster_update.source_run_hint": {
        "de": "Hol dir die neue Fassung über git.\n\n{notes}",
        "en": "Get the new version via git.\n\n{notes}",
    },
    "fenster_update.no_checksum_message": {
        "de": "Zu dieser Fassung liegt keine Prüfsumme vor.",
        "en": "No checksum is available for this version.",
    },
    "fenster_update.no_checksum_hint": {
        "de": ("Ohne sie wird nichts ausgetauscht - eine "
               "Programmdatei ungeprüft über die eigene zu "
               "schreiben, wäre genau der Weg, den man einem "
               "Angreifer nicht offenlassen darf.\n\n"
               "Lade sie von der Projektseite:\n{url}"),
        "en": ("Without one, nothing gets replaced - writing over "
               "the program file unverified would be exactly the "
               "opening an attacker shouldn't be given.\n\n"
               "Download it from the project page:\n{url}"),
    },
    "fenster_update.folder_not_writable_message": {
        "de": "In diesem Ordner darf die App nichts schreiben.",
        "en": "The app isn't allowed to write in this folder.",
    },
    "fenster_update.folder_not_writable_hint": {
        "de": ("Deshalb kann sie sich hier nicht selbst ersetzen. "
               "Verschiebe sie in einen eigenen Ordner - etwa auf "
               "den Schreibtisch - oder lade die neue Fassung von "
               "der Projektseite:\n{url}"),
        "en": ("So it can't replace itself here. Move it to a "
               "folder of your own - the desktop, say - or "
               "download the new version from the project "
               "page:\n{url}"),
    },
    "fenster_update.confirm_update_body": {
        "de": ("Du hast {current}, neu ist {new} "
               "({size} MB).\n\n"
               "Die App lädt die neue Datei, prüft ihre Prüfsumme und legt "
               "sich selbst beiseite. Danach startet sie neu. Dein "
               "Datenordner und deine Pakete bleiben unberührt.\n\n"),
        "en": ("You have {current}, {new} "
               "({size} MB) is new.\n\n"
               "The app downloads the new file, verifies its checksum, "
               "and sets itself aside. It then restarts. Your data "
               "folder and packages stay untouched.\n\n"),
    },
    "fenster_update.whats_new_segment": {
        "de": "Was neu ist:\n{notes}\n\n",
        "en": "What's new:\n{notes}\n\n",
    },
    "fenster_update.update_now_question": {
        "de": "Jetzt aktualisieren?",
        "en": "Update now?",
    },
    "fenster_update.status_downloading": {
        "de": "Lade ...",
        "en": "Downloading ...",
    },
    "fenster_update.status_downloading_progress": {
        "de": "Lade ... {percent} %",
        "en": "Downloading ... {percent} %",
    },
    "fenster_update.status_ready": {
        "de": "Version {version} ist bereit.",
        "en": "Version {version} is ready.",
    },
    "fenster_update.done_title": {
        "de": "Fertig",
        "en": "Done",
    },
    "fenster_update.done_body": {
        "de": ("Version {version} ist eingespielt.\n\n"
               "Jetzt neu starten? Die alte Fassung wird beim nächsten "
               "Start weggeräumt."),
        "en": ("Version {version} has been installed.\n\n"
               "Restart now? The old version will be cleaned up on "
               "the next start."),
    },
    "fenster_update.restart_title": {
        "de": "Neustart",
        "en": "Restart",
    },
    "fenster_update.restart_message": {
        "de": "Die neue Fassung ließ sich nicht starten.",
        "en": "The new version couldn't be started.",
    },
    "fenster_update.restart_hint": {
        "de": "Schließe die App und starte sie von Hand.",
        "en": "Close the app and start it manually.",
    },
    "fenster_update.manual_action_title": {
        "de": "Bitte von Hand nachhelfen",
        "en": "Manual Action Needed",
    },
    "fenster_update.not_updated_title": {
        "de": "Nicht aktualisiert",
        "en": "Not Updated",
    },
    "fenster_update.not_updated_hint": {
        "de": ("Es wurde nichts ausgetauscht. Die Datei liegt "
               "weiterhin auf der Projektseite bereit:\n{url}"),
        "en": ("Nothing was replaced. The file is still "
               "waiting on the project page:\n{url}"),
    },
})
