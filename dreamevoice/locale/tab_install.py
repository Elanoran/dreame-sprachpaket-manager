"""German/English strings for ui/tab_install.py ('Build and Install')."""

from __future__ import annotations

from ..i18n import register

register({
    "tab_install.app_hinweis": {
        "de": (
            "Wichtig zur Dreamehome-App: Dein Paket taucht dort unter 'Sprachton' "
            "NICHT auf. Die App listet nur Sprachen aus Dreames eigenem Katalog, und "
            "eine selbst vergebene Kennung steht da nicht drin.\n\n"
            "Dass die App beim Öffnen meldet, Roboter und App hätten verschiedene "
            "Spracheinstellungen, ist deshalb genau das erwartete Zeichen dafür, dass "
            "dein Paket läuft.\n\n"
            "Wähle in der Dreamehome-App jetzt KEINE Sprache aus - damit würde der "
            "Roboter das offizielle Paket nachladen und deines überschreiben.\n\n"
            "Zurück zur Originalstimme geht es jederzeit über "
            "'Originalstimme wiederherstellen'."
        ),
        "en": (
            "Important regarding the Dreamehome app: your pack will NOT show up "
            "there under 'Voice'. The app only lists languages from Dreame's own "
            "catalog, and a self-assigned identifier isn't in it.\n\n"
            "So if the app reports on opening that the robot and app have "
            "different language settings, that's exactly the expected sign that "
            "your pack is running.\n\n"
            "Don't pick a language in the Dreamehome app now - that would make the "
            "robot re-download the official pack and overwrite yours.\n\n"
            "You can go back to the original voice any time via "
            "'Restore Original Voice'."
        ),
    },
    "tab_install.info_banner": {
        "de": (
            "So läuft die Installation: Die App baut das Paket, startet kurz "
            "einen kleinen Webserver auf diesem PC und schickt dem Roboter über "
            "die Dreame-Cloud den Auftrag, es dort abzuholen. Der Roboter prüft "
            "die Prüfsumme selbst - passt sie nicht, verwirft er das Paket und "
            "behält seine bisherige Stimme.\n"
            "Dein Paket erscheint danach NICHT in der Dreamehome-App unter "
            "'Sprachton' - die zeigt nur Dreames eigene Sprachen. Ob es läuft, "
            "verrät der Knopf 'Sprachpaket am Roboter abfragen'."
        ),
        "en": (
            "How the install works: the app builds the pack, briefly starts "
            "a small web server on this PC, and tells the robot via the "
            "Dreame cloud to fetch it there. The robot checks the checksum "
            "itself - if it doesn't match, it discards the pack and keeps "
            "its current voice.\n"
            "Your pack will NOT appear in the Dreamehome app under "
            "'Voice' afterward - that only shows Dreame's own languages. "
            "The 'Check Voice Pack on Robot' button tells you whether it's "
            "running."
        ),
    },
    "tab_install.summary_title": {"de": "Übersicht", "en": "Summary"},
    "tab_install.summary_robot": {"de": "Roboter", "en": "Robot"},
    "tab_install.summary_original_pack": {"de": "Originalpaket", "en": "Original Pack"},
    "tab_install.summary_custom_announcements": {
        "de": "Eigene Ansagen", "en": "Custom Announcements",
    },
    "tab_install.summary_built_pack": {"de": "Gebautes Paket", "en": "Built Pack"},
    "tab_install.summary_md5": {"de": "MD5-Prüfsumme", "en": "MD5 Checksum"},
    "tab_install.build_own_pack_button": {
        "de": "Stattdessen mein eigenes Paket bauen",
        "en": "Build My Own Pack Instead",
    },
    "tab_install.saved_packs_label": {"de": "Gespeicherte Pakete", "en": "Saved Packs"},
    "tab_install.settings_title": {"de": "Einstellungen", "en": "Settings"},
    "tab_install.identifier_label": {"de": "Kennung", "en": "Identifier"},
    "tab_install.pc_address_label": {"de": "PC-Adresse", "en": "PC Address"},
    "tab_install.port_empty_hint": {
        "de": "leer = automatisch", "en": "empty = automatic",
    },
    "tab_install.custom_url_label": {"de": "Eigene URL", "en": "Custom URL"},
    "tab_install.custom_url_hint": {
        "de": ("nur nötig, wenn der Roboter diesen PC nicht "
               "erreicht (dann Paket selbst hochladen)"),
        "en": ("only needed if the robot can't reach this PC "
               "(then upload the pack yourself)"),
    },
    "tab_install.step3_title": {
        "de": "Schritt 3: Auf den Roboter übertragen",
        "en": "Step 3: Transfer to the Robot",
    },
    "tab_install.install_button": {
        "de": "Sprachpaket auf Roboter installieren",
        "en": "Install Voice Pack on Robot",
    },
    "tab_install.build_only_button": {"de": "Nur bauen", "en": "Build Only"},
    "tab_install.cancel_button": {"de": "Abbrechen", "en": "Cancel"},
    "tab_install.open_pack_folder_button": {
        "de": "Paketordner öffnen", "en": "Open Pack Folder",
    },
    "tab_install.choose_ready_pack_button": {
        "de": "Fertiges Paket wählen ...", "en": "Choose Ready-Made Pack ...",
    },
    "tab_install.status_ready": {"de": "Bereit", "en": "Ready"},
    "tab_install.check_status_button": {
        "de": "Sprachpaket am Roboter abfragen", "en": "Check Voice Pack on Robot",
    },
    "tab_install.restore_card_title": {
        "de": "Notausgang: Originalstimme zurückholen",
        "en": "Emergency Exit: Restore Original Voice",
    },
    "tab_install.restore_card_desc": {
        "de": ("Installiert das offizielle Dreame-Sprachpaket erneut - der "
               "Roboter lädt es direkt beim Hersteller, dieser PC ist "
               "dabei gar nicht beteiligt."),
        "en": ("Installs the official Dreame voice pack again - the "
               "robot loads it directly from the manufacturer, this "
               "PC isn't involved at all."),
    },
    "tab_install.language_label": {"de": "Sprache", "en": "Language"},
    "tab_install.restore_button": {
        "de": "Originalstimme wiederherstellen", "en": "Restore Original Voice",
    },
    "tab_install.no_packs_built": {
        "de": ("Noch keine Pakete gebaut. Unter 'Eigene Stimmen' entsteht ein "
               "Dialektpaket, unter 'Einzelne Ansagen' ein eigenes."),
        "en": ("No packs built yet. 'Custom Voices' creates a dialect "
               "pack, 'Individual Announcements' a custom one."),
    },
    "tab_install.saved_packs_summary": {
        "de": ("{count} gespeicherte Pakete. Jede Stimme liegt "
               "in einer eigenen Datei - eine neue Fassung überschreibt "
               "nie eine ältere."),
        "en": ("{count} saved packs. Each voice lives in its "
               "own file - a new version never overwrites an older one."),
    },
    "tab_install.log_selected": {
        "de": "Ausgewählt: {name}", "en": "Selected: {name}",
    },
    "tab_install.log_voice": {"de": "Stimme: {voice}", "en": "Voice: {voice}"},
    "tab_install.device_not_selected": {
        "de": "nicht ausgewählt", "en": "not selected",
    },
    "tab_install.base_pack_not_loaded": {
        "de": "noch nicht geladen", "en": "not loaded yet",
    },
    "tab_install.missing_files_suffix": {
        "de": "  ({count} Datei(en) fehlen!)", "en": "  ({count} file(s) missing!)",
    },
    "tab_install.pack_not_built": {"de": "noch nicht gebaut", "en": "not built yet"},
    "tab_install.prebuilt_queued": {
        "de": ("Fertiges Paket '{name}' liegt bereit und "
               "wird installiert. Deine eigenen Zuweisungen bleiben "
               "gespeichert, werden aber gerade nicht verwendet."),
        "en": ("The ready-made pack '{name}' is "
               "queued for install. Your own assignments stay saved "
               "but aren't being used right now."),
    },
    "tab_install.query_status_no_robot_title": {
        "de": "Kein Roboter ausgewählt", "en": "No Robot Selected",
    },
    "tab_install.query_status_no_robot_message": {
        "de": "Melde dich zuerst unter 'Verbindung' an.",
        "en": "Sign in under 'Connection' first.",
    },
    "tab_install.query_status_asking": {
        "de": "Frage den Roboter ...", "en": "Asking the robot ...",
    },
    "tab_install.query_status_unknown": {"de": "unbekannt", "en": "unknown"},
    "tab_install.query_status_active_pack_log": {
        "de": "Aktives Sprachpaket laut Roboter: {value}",
        "en": "Active voice pack per the robot: {value}",
    },
    "tab_install.query_status_state_log": {
        "de": "Zustand: {state}", "en": "State: {state}",
    },
    "tab_install.query_status_no_response_badge": {
        "de": "Keine Antwort - Roboter im Standby?",
        "en": "No Response - Robot Asleep?",
    },
    "tab_install.query_status_no_response_title": {
        "de": "Keine Antwort", "en": "No Response",
    },
    "tab_install.query_status_no_response_message": {
        "de": "Der Roboter hat nicht geantwortet.",
        "en": "The robot didn't respond.",
    },
    "tab_install.query_status_no_response_hint": {
        "de": "Wecke ihn in der Dreamehome-App auf und versuche es erneut.",
        "en": "Wake it in the Dreamehome app and try again.",
    },
    "tab_install.query_status_active_badge": {
        "de": "Aktiv: {value}", "en": "Active: {value}",
    },
    "tab_install.query_status_official_title": {
        "de": "Offizielles Paket aktiv", "en": "Official Pack Active",
    },
    "tab_install.query_status_official_message": {
        "de": "Der Roboter benutzt gerade '{value}' - ein Paket von Dreame.",
        "en": "The robot is currently using '{value}' - a pack from Dreame.",
    },
    "tab_install.query_status_official_hint": {
        "de": ("Dein eigenes Paket ist damit nicht aktiv. Das passiert, "
               "wenn in der Dreamehome-App eine Sprache ausgewählt wurde: "
               "der Roboter lädt sie dann nach und überschreibt das eigene "
               "Paket. Installiere es einfach erneut."),
        "en": ("Your custom pack isn't active as a result. This happens "
               "when a language was selected in the Dreamehome app: the "
               "robot then re-downloads it and overwrites the custom "
               "pack. Just install it again."),
    },
    "tab_install.query_status_own_title": {
        "de": "Dein Paket ist aktiv", "en": "Your Pack Is Active",
    },
    "tab_install.query_status_own_message": {
        "de": ("Der Roboter benutzt gerade '{value}' - das ist deine "
               "eigene Kennung, kein Paket von Dreame."),
        "en": ("The robot is currently using '{value}' - that's your "
               "own identifier, not a pack from Dreame."),
    },
    "tab_install.query_status_failed_badge": {
        "de": "Abfrage fehlgeschlagen", "en": "Check Failed",
    },
    "tab_install.query_status_failed_title": {
        "de": "Abfrage fehlgeschlagen", "en": "Check Failed",
    },
    "tab_install.pick_pack_dialog_title": {
        "de": "Gebautes Sprachpaket wählen (.tar.gz)",
        "en": "Choose a Built Voice Pack (.tar.gz)",
    },
    "tab_install.pick_pack_filetype_pack": {
        "de": "Gebautes Sprachpaket", "en": "Built voice pack",
    },
    "tab_install.pick_pack_filetype_all": {
        "de": "Alle Dateien", "en": "All files",
    },
    "tab_install.pick_pack_wrong_format_title": {
        "de": "Das sind Aufnahmen, kein fertiges Paket",
        "en": "That's Recordings, Not a Ready-Made Pack",
    },
    "tab_install.pick_pack_wrong_format_message": {
        "de": ("{name} enthält einzelne Sprachdateien. Hier "
               "wird ein bereits gebautes Paket erwartet - eine "
               ".tar.gz-Datei."),
        "en": ("{name} contains individual voice files. This "
               "expects an already-built pack - a .tar.gz file."),
    },
    "tab_install.pick_pack_wrong_format_hint": {
        "de": ("So kommst du weiter: Sind es die Aufnahmen von der "
               "Projektseite, stehen sie ohnehin schon bereit. "
               "Nimm dafür in der Leiste 'Fertige Stimmen' "
               "- dort aussuchen, anhören, aufspielen.\n\n"
               "Sind es eigene Aufnahmen, nimm 'Eigene Stimmen' und klicke "
               "dort 'Aufnahmen einlesen ...'. Die App baut daraus das "
               "Paket für dein Modell; danach steht es auch hier zur "
               "Auswahl. Entpacken musst du nichts."),
        "en": ("How to proceed: if these are the recordings from the "
               "project page, they're already ready to go. Use the "
               "'Ready-Made Voices' sidebar item instead - choose, "
               "preview, install there.\n\n"
               "If these are your own recordings, use 'Custom Voices' and "
               "click 'Import Recordings ...' there. The app builds the "
               "pack for your model from them; it then shows up here too. "
               "You don't need to unpack anything."),
    },
    "tab_install.pick_pack_loaded_log": {
        "de": "Übernommen: {name}", "en": "Loaded: {name}",
    },
    "tab_install.pick_pack_summary_log": {
        "de": "{count} Ansagen, {size:.1f} MB, MD5 {md5}",
        "en": "{count} announcements, {size:.1f} MB, MD5 {md5}",
    },
    "tab_install.pick_pack_loaded_badge": {
        "de": "Paket übernommen - bereit zur Installation",
        "en": "Pack Loaded - Ready to Install",
    },
    "tab_install.cancel_requested_log": {
        "de": "Abbruch angefordert ...", "en": "Cancellation requested ...",
    },
    "tab_install.preflight_no_robot_title": {
        "de": "Kein Roboter ausgewählt", "en": "No Robot Selected",
    },
    "tab_install.preflight_no_robot_message": {
        "de": "Melde dich unter 'Verbindung' an und wähle deinen Roboter aus.",
        "en": "Sign in under 'Connection' and choose your robot.",
    },
    "tab_install.preflight_no_base_title": {
        "de": "Originalpaket fehlt", "en": "Original Pack Missing",
    },
    "tab_install.preflight_no_base_message": {
        "de": ("Lade unter 'Einzelne Ansagen' zuerst das offizielle "
               "Sprachpaket deines Roboters herunter. Es ist die Grundlage "
               "deines eigenen Pakets."),
        "en": ("First download your robot's official voice pack under "
               "'Individual Announcements'. It's the foundation for your "
               "own pack."),
    },
    "tab_install.preflight_nothing_title": {
        "de": "Nichts zu tun", "en": "Nothing to Do",
    },
    "tab_install.preflight_nothing_message": {
        "de": ("Es ist noch keine einzige Ansage ausgetauscht. Weise unter "
               "'Einzelne Ansagen' mindestens einer Ansage eine Audiodatei zu "
               "- oder hole dir unter 'Eigene Stimmen' ein vorgefertigtes Paket."),
        "en": ("Not a single announcement has been replaced yet. Assign at "
               "least one announcement an audio file under 'Individual "
               "Announcements' - or get a ready-made pack under 'Custom "
               "Voices'."),
    },
    "tab_install.preflight_missing_line": {
        "de": "  Ansage {index}: {path}", "en": "  Announcement {index}: {path}",
    },
    "tab_install.preflight_missing_more": {
        "de": "\n  ... und {count} weitere", "en": "\n  ... and {count} more",
    },
    "tab_install.preflight_missing_title": {
        "de": "Dateien fehlen", "en": "Files Missing",
    },
    "tab_install.preflight_missing_message": {
        "de": ("{count} zugewiesene Datei(en) existieren nicht mehr:\n\n"
               "{preview}{more}\n\nDiese Ansagen bleiben auf der Originalstimme. "
               "Trotzdem fortfahren?"),
        "en": ("{count} assigned file(s) no longer exist:\n\n"
               "{preview}{more}\n\nThese announcements will stay on the "
               "original voice. Continue anyway?"),
    },
    "tab_install.build_pack_using_prepared_log": {
        "de": "Verwende das vorbereitete Paket '{name}'.",
        "en": "Using the prepared pack '{name}'.",
    },
    "tab_install.build_pack_already_adapted_log": {
        "de": ("Es wurde bereits auf dein Modell angepasst - es muss nichts "
               "neu gebaut werden."),
        "en": ("It's already adapted to your model - nothing needs "
               "to be built again."),
    },
    "tab_install.step_building_pack": {"de": "Baue Paket", "en": "Building pack"},
    "tab_install.build_only_log_start": {
        "de": "Baue Paket (ohne Installation) ...",
        "en": "Building pack (without installing) ...",
    },
    "tab_install.build_only_badge_done": {"de": "Paket gebaut", "en": "Pack Built"},
    "tab_install.build_only_saved_log": {
        "de": "Gespeichert unter: {path}", "en": "Saved to: {path}",
    },
    "tab_install.install_invalid_port_title": {
        "de": "Ungültiger Port", "en": "Invalid Port",
    },
    "tab_install.install_invalid_port_message": {
        "de": "Der Port muss eine Zahl sein (oder leer bleiben).",
        "en": "The port must be a number (or left empty).",
    },
    "tab_install.install_starting_log": {
        "de": "Starte Installation", "en": "Starting installation",
    },
    "tab_install.install_transferring_log": {
        "de": "Übertrage auf den Roboter", "en": "Transferring to the robot",
    },
    "tab_install.install_success_badge": {
        "de": "Erfolgreich installiert", "en": "Installed Successfully",
    },
    "tab_install.install_transferred_badge": {
        "de": "Übertragen, nicht bestätigt", "en": "Transferred, Not Confirmed",
    },
    "tab_install.install_done_title": {"de": "Fertig", "en": "Done"},
    "tab_install.install_transferred_title": {"de": "Übertragen", "en": "Transferred"},
    "tab_install.install_try_it_out": {
        "de": ("Probier es aus: lass den Roboter eine "
               "Reinigung starten - er sollte jetzt anders klingen."),
        "en": ("Try it out: have the robot start "
               "a cleaning run - it should sound different now."),
    },
    "tab_install.install_not_completed_title": {
        "de": "Nicht abgeschlossen", "en": "Not Completed",
    },
    "tab_install.restore_no_robot_title": {
        "de": "Kein Roboter ausgewählt", "en": "No Robot Selected",
    },
    "tab_install.restore_no_robot_message": {
        "de": "Melde dich zuerst unter 'Verbindung' an.",
        "en": "Sign in under 'Connection' first.",
    },
    "tab_install.restore_no_lang_title": {
        "de": "Keine Sprache gewählt", "en": "No Language Chosen",
    },
    "tab_install.restore_no_lang_message": {
        "de": "Bitte wähle das wiederherzustellende Paket aus.",
        "en": "Please choose the pack to restore.",
    },
    "tab_install.restore_confirm_title": {
        "de": "Originalstimme wiederherstellen", "en": "Restore Original Voice",
    },
    "tab_install.restore_confirm_message": {
        "de": ("Der Roboter lädt '{label}' direkt von Dreame und stellt "
               "damit die Originalstimme wieder her.\n\nFortfahren?"),
        "en": ("The robot will load '{label}' directly from Dreame, "
               "restoring the original voice.\n\nContinue?"),
    },
    "tab_install.restore_log_start": {
        "de": "Stelle Originalstimme wieder her", "en": "Restoring original voice",
    },
    "tab_install.error_failed_badge": {"de": "Fehlgeschlagen", "en": "Failed"},
    "tab_install.error_title": {"de": "Fehler", "en": "Error"},
})
