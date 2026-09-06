from ..i18n import register

register({
    "page_voice.page_title": {
        "de": "Fertige Stimmen",
        "en": "Ready-Made Voices",
    },
    "page_voice.page_subtitle": {
        "de": ("Aussuchen, anhören, aufspielen. Die Stimmen sind in der "
               "App enthalten - es wird nichts heruntergeladen."),
        "en": ("Choose, preview, install. The voices are built into the "
               "app - nothing gets downloaded."),
    },
    "page_voice.which_voice_title": {
        "de": "Welche Stimme?",
        "en": "Which Voice?",
    },
    "page_voice.listen_button": {
        "de": "▶ Anhören",
        "en": "▶ Listen",
    },
    "page_voice.send_card_title": {
        "de": "Auf den Roboter bringen",
        "en": "Send to the Robot",
    },
    "page_voice.identifier_label": {
        "de": "Kennung",
        "en": "Identifier",
    },
    "page_voice.identifier_note": {
        "de": ("Fest, und das mit Absicht: Jede Stimme landet an "
               "derselben Stelle im Roboter und überschreibt die "
               "vorige. Sonst sammeln sie sich dort an, und löschen "
               "kann man sie nicht. Die deutsche Originalstimme "
               "bleibt davon unberührt."),
        "en": ("Fixed, and on purpose: every voice lands in the same "
               "spot on the robot and overwrites the previous one. "
               "Otherwise they'd pile up there, with no way to "
               "delete them. The German original voice stays "
               "untouched by this."),
    },
    "page_voice.install_button": {
        "de": "Aufspielen",
        "en": "Install",
    },
    "page_voice.cancel_button": {
        "de": "Abbrechen",
        "en": "Cancel",
    },
    "page_voice.badge_ready": {
        "de": "Bereit",
        "en": "Ready",
    },
    "page_voice.custom_voice_hint": {
        "de": ("Du willst eine eigene Stimme, einen anderen Dialekt oder "
               "eigene Aufnahmen?"),
        "en": ("Want a custom voice, a different dialect, or your own "
               "recordings?"),
    },
    "page_voice.build_custom_voice_button": {
        "de": "Eigene Stimme bauen",
        "en": "Build a Custom Voice",
    },
    "page_voice.source_dialect": {
        "de": "Dialekt",
        "en": "Dialect",
    },
    "page_voice.source_custom": {
        "de": "Eigenes",
        "en": "Custom",
    },
    "page_voice.source_builtin": {
        "de": "in der App enthalten",
        "en": "built into the app",
    },
    "page_voice.source_downloaded": {
        "de": "heruntergeladene Fassung",
        "en": "downloaded version",
    },
    "page_voice.source_project_folder": {
        "de": "aus dem Projektordner",
        "en": "from the project folder",
    },
    "page_voice.dialect_meta": {
        "de": "{desc}  ({count} Ansagen, {voice}, {source})",
        "en": "{desc}  ({count} announcements, {voice}, {source})",
    },
    "page_voice.no_voice_available": {
        "de": "Es steht noch keine fertige Stimme bereit.",
        "en": "No ready-made voice is available yet.",
    },
    "page_voice.status_playing": {
        "de": "Spiele ab ...",
        "en": "Playing ...",
    },
    "page_voice.status_preparing_sample": {
        "de": "Bereite die Probe vor ...",
        "en": "Preparing the sample ...",
    },
    "page_voice.stop_button": {
        "de": "■ Stopp",
        "en": "■ Stop",
    },
    "page_voice.unpacking_ffmpeg": {
        "de": "ffmpeg wird einmalig ausgepackt ...",
        "en": "Unpacking ffmpeg (one time only) ...",
    },
    "page_voice.recordings_not_found_title": {
        "de": "Aufnahmen nicht gefunden",
        "en": "Recordings Not Found",
    },
    "page_voice.recordings_not_found_message": {
        "de": "Die Aufnahmen für {name} ließen sich nicht öffnen.",
        "en": "The recordings for {name} couldn't be opened.",
    },
    "page_voice.no_preview_title": {
        "de": "Keine Probe möglich",
        "en": "No Preview Possible",
    },
    "page_voice.no_preview_message": {
        "de": "Aus dieser Stimme ließ sich keine Ansage entnehmen.",
        "en": "No announcement could be extracted from this voice.",
    },
    "page_voice.no_preview_hint": {
        "de": ("Zum Anhören wird ffmpeg gebraucht. Es steckt in der EXE "
               "und wird beim ersten Bedarf ausgepackt."),
        "en": ("ffmpeg is needed to listen. It's built into the EXE "
               "and unpacked the first time it's needed."),
    },
    "page_voice.preview_cancelled": {
        "de": "Probe abgebrochen.",
        "en": "Preview cancelled.",
    },
    "page_voice.preview_done": {
        "de": "{count} Ansagen angehört. Klingt gut? Dann unten aufspielen.",
        "en": "{count} announcements previewed. Sound good? Install it below.",
    },
    "page_voice.preview_failed_title": {
        "de": "Probe fehlgeschlagen",
        "en": "Preview Failed",
    },
    "page_voice.cancel_requested_log": {
        "de": "Abbruch angefordert ...",
        "en": "Cancellation requested ...",
    },
    "page_voice.no_voice_chosen_title": {
        "de": "Keine Stimme gewählt",
        "en": "No Voice Chosen",
    },
    "page_voice.no_voice_chosen_message": {
        "de": "Wähle oben aus, wie dein Roboter klingen soll.",
        "en": "Choose above how your robot should sound.",
    },
    "page_voice.not_connected_title": {
        "de": "Nicht verbunden",
        "en": "Not Connected",
    },
    "page_voice.not_connected_message": {
        "de": "Melde dich auf der Startseite an und wähle deinen Roboter.",
        "en": "Sign in on the Start page and choose your robot.",
    },
    "page_voice.original_pack_missing_title": {
        "de": "Originalpaket fehlt",
        "en": "Original Pack Missing",
    },
    "page_voice.original_pack_missing_message": {
        "de": ("Das offizielle Sprachpaket deines Roboters wird auf "
               "der Startseite einmalig geholt."),
        "en": ("Your robot's official voice pack is fetched once, "
               "on the Start page."),
    },
    "page_voice.install_confirm_title": {
        "de": "Aufspielen?",
        "en": "Install?",
    },
    "page_voice.install_confirm_message": {
        "de": ("'{name}' auf {device} aufspielen?\n\nKennung: {id} - eine "
               "schon dort liegende eigene Stimme wird dabei überschrieben."
               "\n\nDer Rückweg zur Originalstimme bleibt jederzeit offen."),
        "en": ("Install '{name}' on {device}?\n\nIdentifier: {id} - a "
               "custom voice already there will be overwritten.\n\n"
               "The way back to the original voice stays open at any time."),
    },
    "page_voice.badge_preparing": {
        "de": "Bereite vor ...",
        "en": "Preparing ...",
    },
    "page_voice.log_using_pack": {
        "de": "Verwende das fertige Paket {name}.",
        "en": "Using the ready-made pack {name}.",
    },
    "page_voice.log_fetching_recordings": {
        "de": "Hole die Aufnahmen für {name} ...",
        "en": "Fetching the recordings for {name} ...",
    },
    "page_voice.error_recordings_not_found": {
        "de": "Die Aufnahmen für {name} sind nicht auffindbar.",
        "en": "The recordings for {name} can't be found.",
    },
    "page_voice.error_no_assignable_announcement": {
        "de": "In {file} war keine zuzuordnende Ansage.",
        "en": "No assignable announcement was found in {file}.",
    },
    "page_voice.error_cancelled_by_user": {
        "de": "Vom Benutzer abgebrochen.",
        "en": "Cancelled by the user.",
    },
    "page_voice.log_building_pack": {
        "de": "Baue das Paket für dein Modell ({count} Ansagen) ...",
        "en": "Building the pack for your model ({count} announcements) ...",
    },
    "page_voice.engine_builtin": {
        "de": "Mitgeliefert",
        "en": "Built-in",
    },
    "page_voice.log_transferring": {
        "de": "Übertrage auf den Roboter",
        "en": "Transferring to the robot",
    },
    "page_voice.badge_install_success": {
        "de": "Erfolgreich aufgespielt",
        "en": "Installed Successfully",
    },
    "page_voice.badge_transferred_unconfirmed": {
        "de": "Übertragen, nicht bestätigt",
        "en": "Transferred, Not Confirmed",
    },
    "page_voice.info_title_done": {
        "de": "Fertig",
        "en": "Done",
    },
    "page_voice.info_title_transferred": {
        "de": "Übertragen",
        "en": "Transferred",
    },
    "page_voice.info_message_running": {
        "de": "{name} läuft jetzt auf deinem Roboter.",
        "en": "{name} is now running on your robot.",
    },
    "page_voice.info_message_transferred": {
        "de": "{name} wurde auf den Roboter übertragen.",
        "en": "{name} was transferred to the robot.",
    },
    "page_voice.info_detail_try_it": {
        "de": ("Probier es aus: Lass ihn eine Reinigung starten - er "
               "sollte anders klingen.\n\nIn der Dreamehome-App taucht "
               "das Paket nicht auf; das ist normal und kein Fehler.\n\n"),
        "en": ("Try it out: have it start a cleaning run - it should "
               "sound different.\n\nThe pack won't show up in the "
               "Dreamehome app; that's normal, not a bug.\n\n"),
    },
    "page_voice.badge_not_installed": {
        "de": "Nicht aufgespielt",
        "en": "Not Installed",
    },
    "page_voice.badge_failed": {
        "de": "Fehlgeschlagen",
        "en": "Failed",
    },
    "page_voice.error_not_installed_title": {
        "de": "Nicht aufgespielt",
        "en": "Not Installed",
    },
})
