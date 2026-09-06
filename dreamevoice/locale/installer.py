"""English/German strings for dreamevoice/installer.py."""

from __future__ import annotations

from ..i18n import register

register({
    # -- validate_lang_id() --------------------------------------------------
    "installer.err_invalid_lang_id_title": {
        "de": "Die Paketkennung '{lang_id}' ist ungültig.",
        "en": "The pack identifier '{lang_id}' is invalid.",
    },
    "installer.err_invalid_lang_id_hint": {
        "de": "Erlaubt sind bis zu 8 Buchstaben oder Ziffern, z. B. CUSTOM oder BAYERN.",
        "en": "Up to 8 letters or digits are allowed, e.g. CUSTOM or BAYERN.",
    },
    "installer.warn_official_lang_id": {
        "de": "'{cleaned}' ist eine offizielle Dreame-Kennung. Dein Paket "
              "überschreibt damit die mitgelieferte Sprache. Zum Zurückwechseln "
              "musst du das Originalpaket erneut installieren - das kann diese "
              "App, aber eine eigene Kennung wie CUSTOM ist bequemer.",
        "en": "'{cleaned}' is an official Dreame identifier. Your pack "
              "overwrites the built-in language with it. To switch back, "
              "you'll need to reinstall the original pack - this app can "
              "do that, but a custom identifier like CUSTOM is more "
              "convenient.",
    },

    # -- refresh_volume() -----------------------------------------------------
    "installer.log_volume_confirmed": {
        "de": "Lautstärke bestätigt: {value}.",
        "en": "Volume confirmed: {value}.",
    },
    "installer.log_volume_not_confirmed": {
        "de": "Hinweis: Die Lautstärke ließ sich nicht bestätigen.",
        "en": "Note: the volume couldn't be confirmed.",
    },

    # -- NEUSTART_HINWEIS: shown in the log and the finished dialog -------
    "installer.restart_hint": {
        "de": "Falls der Roboter danach leiser klingt als gewohnt: Das liegt an "
              "seiner Firmware, nicht an den Aufnahmen - sie haben denselben Pegel "
              "wie die Originalansagen. Nach einem Sprachwechsel wendet er seine "
              "Lautstärke mitunter erst nach einem Neustart wieder an. Schalte ihn "
              "dazu am Gerät einmal aus und wieder ein; danach ist es behoben.",
        "en": "If the robot sounds quieter than usual afterward: that's due to its "
              "firmware, not the recordings - they're at the same level as the "
              "original announcements. After switching languages it sometimes only "
              "applies its volume again after a restart. Turn it off and on again "
              "at the device; that fixes it.",
    },

    # -- install_pack(): header log lines -----------------------------------
    "installer.log_pack_name": {
        "de": "Paket:  {name}",
        "en": "Pack:  {name}",
    },
    "installer.log_pack_size": {
        "de": "Größe: {size} Bytes ({size_mb:.1f} MB)",
        "en": "Size: {size} bytes ({size_mb:.1f} MB)",
    },
    "installer.log_pack_identifier": {
        "de": "Kennung: {lang_id}",
        "en": "Identifier: {lang_id}",
    },

    # -- install_pack(): step 1, delivery -------------------------------------
    "installer.log_using_custom_url": {
        "de": "Verwende eigene URL: {url}",
        "en": "Using custom URL: {url}",
    },
    "installer.step_using_custom_url": {
        "de": "Eigene URL wird verwendet",
        "en": "Using custom URL",
    },
    "installer.step_starting_server": {
        "de": "Webserver wird gestartet",
        "en": "Starting web server",
    },
    "installer.step_server_running": {
        "de": "Webserver läuft",
        "en": "Web server running",
    },

    # -- install_pack(): step 2, sending the order ---------------------------
    "installer.step_checking_robot": {
        "de": "Roboter wird geprüft",
        "en": "Checking the robot",
    },
    "installer.log_asking_robot": {
        "de": "Frage beim Roboter nach, ob er Sprachpakete auf dem üblichen "
              "Weg entgegennimmt ...",
        "en": "Asking the robot whether it accepts voice packs the usual "
              "way ...",
    },
    "installer.err_no_response_title": {
        "de": "Der Roboter hat auf die Nachfrage nicht geantwortet.",
        "en": "The robot didn't respond to the query.",
    },
    "installer.err_no_response_hint": {
        "de": "Es wurde nichts gesendet. Am häufigsten liegt es "
              "daran, dass er gerade schläft: Wecke ihn in der "
              "Dreamehome-App auf - ein Tipp auf 'Roboter finden' "
              "genügt - und versuche es erneut.\n\n"
              "Technische Details: {reason}",
        "en": "Nothing was sent. Most often it's because it's "
              "asleep: wake it in the Dreamehome app - tapping "
              "'Find Robot' is enough - and try again.\n\n"
              "Technical details: {reason}",
    },
    "installer.err_no_voice_service_title": {
        "de": "Dieser Roboter meldet keinen Sprachpaket-Dienst.",
        "en": "This robot doesn't report a voice-pack service.",
    },
    "installer.err_no_voice_service_hint": {
        "de": "Die App hat vorsichtshalber nichts gesendet. Der "
              "Installationsauftrag geht bei Dreame- und "
              "MOVA-Saugrobotern immer an dieselbe Stelle "
              "(MIoT siid 7, piid 4); dein Gerät antwortet dort "
              "aber nicht. Das spricht dafür, dass es Sprachpakete "
              "gar nicht kennt - etwa bei Mährobotern oder sehr "
              "alten Modellen aus der Mi-Home-App.\n\n"
              "Prüfe, ob du in der Dreamehome-App unter "
              "'Sprachton' überhaupt Sprachen auswählen kannst. "
              "Geht das dort nicht, kann es diese App auch nicht.",
        "en": "The app cautiously sent nothing. The install order "
              "always goes to the same spot on Dreame and MOVA "
              "vacuum robots (MIoT siid 7, piid 4); your device "
              "isn't responding there. That suggests it doesn't "
              "know voice packs at all - for example on mowing "
              "robots or very old Mi-Home models.\n\n"
              "Check whether you can even choose a language under "
              "'Voice' in the Dreamehome app. If that doesn't work "
              "there, this app can't do it either.",
    },
    "installer.log_knows_service": {
        "de": "Der Roboter kennt den Sprachpaket-Dienst.",
        "en": "The robot knows the voice-pack service.",
    },
    "installer.log_configured_volume": {
        "de": "Eingestellte Lautstärke: {value}",
        "en": "Configured volume: {value}",
    },
    "installer.log_pack_exists": {
        "de": "Unter '{lang_id}' liegt bereits ein Paket - es wird "
              "überschrieben.",
        "en": "There's already a pack under '{lang_id}' - it will be "
              "overwritten.",
    },
    "installer.step_sending_order": {
        "de": "Auftrag wird an den Roboter geschickt",
        "en": "Sending the order to the robot",
    },
    "installer.log_sending_order": {
        "de": "Sende Installationsauftrag über die Dreame-Cloud ...",
        "en": "Sending install order via the Dreame cloud ...",
    },
    "installer.err_order_rejected_title": {
        "de": "Der Roboter hat den Auftrag nicht angenommen.",
        "en": "The robot didn't accept the order.",
    },
    "installer.log_order_accepted": {
        "de": "Auftrag angenommen.",
        "en": "Order accepted.",
    },

    # -- install_pack(): step 3, waiting for the download ---------------------
    "installer.step_downloading": {
        "de": "Roboter lädt das Paket herunter",
        "en": "Robot downloading the pack",
    },
    "installer.log_waiting_download": {
        "de": "Warte bis zu {seconds} Sekunden auf den Download ...",
        "en": "Waiting up to {seconds} seconds for the download ...",
    },
    "installer.msg_cancelled": {
        "de": "Vom Benutzer abgebrochen.",
        "en": "Cancelled by the user.",
    },
    "installer.err_download_stopped_title": {
        "de": "Der Roboter hat begonnen zu laden und dann "
              "abgebrochen.",
        "en": "The robot started downloading and then stopped.",
    },
    "installer.err_download_stopped_hint": {
        "de": "Er hat diesen PC erreicht - an Firewall oder "
              "getrennten Netzen liegt es also nicht. Die "
              "Verbindung ist mittendrin abgerissen. Häufigste "
              "Gründe: schwaches WLAN an der Stelle, an der "
              "der Roboter gerade steht, oder er ist in den "
              "Standby gegangen. Stell ihn näher an den "
              "Router, weck ihn in der Dreamehome-App auf "
              "und versuche es erneut.",
        "en": "It reached this PC - so it's not a firewall "
              "or separate networks. The connection dropped "
              "midway. Most common reasons: weak Wi-Fi "
              "where the robot currently is, or it went "
              "into standby. Move it closer to the router, "
              "wake it in the Dreamehome app, and try "
              "again.",
    },
    "installer.err_not_picked_up_title": {
        "de": "Der Roboter hat das Sprachpaket nicht abgeholt.",
        "en": "The robot didn't pick up the voice pack.",
    },
    "installer.log_download_confirmed": {
        "de": "Download durch den Roboter bestätigt.",
        "en": "Download confirmed by the robot.",
    },
    "installer.step_pack_transferred": {
        "de": "Paket übertragen",
        "en": "Pack transferred",
    },
    "installer.step_waiting_robot": {
        "de": "Warte auf den Roboter",
        "en": "Waiting for the robot",
    },

    # -- install_pack(): step 4, watching the installation ---------------------
    "installer.step_installing": {
        "de": "Roboter installiert das Paket",
        "en": "Robot installing the pack",
    },
    "installer.log_waiting_response": {
        "de": "Warte auf die Rückmeldung des Roboters ...",
        "en": "Waiting for the robot's response ...",
    },
    "installer.err_install_failed_title": {
        "de": "Der Roboter meldet, dass die Installation fehlgeschlagen ist.",
        "en": "The robot reports that the installation failed.",
    },
    "installer.err_install_failed_hint": {
        "de": "Meist stimmt die Datei nicht mit MD5 oder Größe "
              "überein, oder der Roboter kam nicht bis zum Ende "
              "an sie heran. Die bisherige Stimme bleibt dabei "
              "unangetastet - du kannst es einfach erneut "
              "versuchen.",
        "en": "Usually the file doesn't match on MD5 or size, "
              "or the robot didn't get all the way through it. "
              "The current voice stays untouched - you can "
              "just try again.",
    },
    "installer.err_lang_mismatch_title": {
        "de": "Der Roboter meldet '{active}' als "
              "aktive Sprache, nicht '{target}'.",
        "en": "The robot reports '{active}' as the "
              "active language, not '{target}'.",
    },
    "installer.err_lang_mismatch_hint_install": {
        "de": "Der Zustand am Gerät meldet zwar Erfolg, die "
              "aktive Sprache passt aber nicht dazu. Am "
              "wahrscheinlichsten ist, dass in der "
              "Dreamehome-App zwischenzeitlich eine Sprache "
              "unter 'Sprachton' ausgewählt wurde - damit "
              "lädt der Roboter das offizielle Paket nach "
              "und überschreibt das eigene. Versuche es "
              "erneut und lass die Sprachauswahl in der "
              "Handy-App dabei unberührt.",
        "en": "The device's state reports success, but the "
              "active language doesn't match it. Most likely a "
              "language was selected under 'Voice' in the "
              "Dreamehome app in the meantime - this makes the "
              "robot re-download the official pack and "
              "overwrite the custom one. Try again and leave "
              "the language selection in the phone app alone.",
    },
    "installer.log_active_pack": {
        "de": "Der Roboter meldet '{active}' als aktives "
              "Sprachpaket.",
        "en": "The robot reports '{active}' as the "
              "active voice pack.",
    },
    "installer.msg_installed_active": {
        "de": "Das Sprachpaket '{lang_id}' ist "
              "installiert und aktiv.",
        "en": "The voice pack '{lang_id}' is "
              "installed and active.",
    },
    "installer.msg_pack_transferred": {
        "de": "Das Sprachpaket '{lang_id}' wurde "
              "übertragen.",
        "en": "The voice pack '{lang_id}' was "
              "transferred.",
    },
    "installer.hint_probably_installed": {
        "de": "Der Roboter hat das Paket nachweislich abgeholt "
              "und meldet 'erfolgreich' - eine Zustandsänderung "
              "war dabei aber nicht zu beobachten, weil dort schon "
              "vorher dieselbe Meldung stand. Hör einmal hin: Wenn "
              "der Roboter in der neuen Stimme spricht, hat alles "
              "geklappt.\n\n",
        "en": "The robot has provably picked up the pack and "
              "reports 'successful' - but no state change was "
              "observed, because the same message was already "
              "there before. Listen: if the robot speaks in the "
              "new voice, everything worked.\n\n",
    },
    "installer.step_done": {
        "de": "Fertig",
        "en": "Done",
    },
    "installer.err_timeout_title": {
        "de": "Der Roboter hat die Installation nicht innerhalb der Wartezeit bestätigt.",
        "en": "The robot didn't confirm the installation within the wait time.",
    },
    "installer.hint_timeout_prefix_downloaded": {
        "de": "Das Paket wurde nachweislich vollständig abgeholt. ",
        "en": "The pack was provably fetched completely. ",
    },
    "installer.hint_timeout_prefix_custom_url": {
        "de": "Ob der Roboter das Paket abgeholt hat, lässt sich bei "
              "einer eigenen URL von hier aus nicht sehen. ",
        "en": "Whether the robot picked up the pack can't be seen "
              "from here with a custom URL. ",
    },
    "installer.hint_timeout_suffix": {
        "de": "Sehr wahrscheinlich läuft die Installation noch oder ist "
              "bereits fertig. Der Roboter sagt bei Erfolg 'Sprache "
              "erfolgreich gewechselt'. Prüfe die Stimme am Gerät; falls "
              "sie unverändert ist, starte den Vorgang einfach erneut.",
        "en": "It's very likely that the installation is still "
              "running or is already done. On success the robot "
              "says 'language switched successfully'. Check the "
              "voice on the device; if it's unchanged, just start "
              "the process again.",
    },
    "installer.err_unexpected": {
        "de": "Unerwarteter Fehler bei der Installation.",
        "en": "Unexpected error during installation.",
    },

    # -- restore_official() ---------------------------------------------------
    "installer.log_restoring_pack": {
        "de": "Stelle das offizielle Paket '{label}' wieder her.",
        "en": "Restoring the official pack '{label}'.",
    },
    "installer.log_source": {
        "de": "Quelle: {url}",
        "en": "Source: {url}",
    },
    "installer.log_size_md5": {
        "de": "Größe: {size} Bytes, MD5: {md5}",
        "en": "Size: {size} bytes, MD5: {md5}",
    },
    "installer.log_already_active": {
        "de": "'{id}' ist bereits die aktive Kennung - das Paket wird "
              "neu geladen.",
        "en": "'{id}' is already the active identifier - the pack "
              "will be reloaded.",
    },
    "installer.step_sending_order_short": {
        "de": "Auftrag wird geschickt",
        "en": "Sending the order",
    },
    "installer.log_order_accepted_direct": {
        "de": "Auftrag angenommen. Der Roboter lädt jetzt direkt bei Dreame.",
        "en": "Order accepted. The robot is now downloading directly from Dreame.",
    },
    "installer.step_downloading_from_dreame": {
        "de": "Roboter lädt bei Dreame",
        "en": "Robot downloading from Dreame",
    },
    "installer.err_restore_failed_title": {
        "de": "Der Roboter meldet, dass das Zurückholen fehlgeschlagen ist.",
        "en": "The robot reports that restoring it failed.",
    },
    "installer.err_restore_failed_hint": {
        "de": "Die bisherige Stimme bleibt dabei unangetastet. "
              "Versuche es erneut, oder stelle die Sprache in der "
              "Dreamehome-App unter Einstellungen > Sprachpaket um.",
        "en": "The current voice stays untouched. Try again, or "
              "switch the language in the Dreamehome app under "
              "Settings > Voice Pack.",
    },
    "installer.err_lang_mismatch_hint_restore": {
        "de": "Die Zustandsmeldung am Gerät passt nicht zur aktiven "
              "Sprache. Stelle die Sprache in der Dreamehome-App "
              "unter 'Sprachton' um - das ist derselbe Vorgang, und "
              "dort siehst du unmittelbar, was der Roboter tut.",
        "en": "The device's state message doesn't match the "
              "active language. Switch the language in the "
              "Dreamehome app under 'Voice' - that's the same "
              "process, and you'll see immediately what the robot "
              "does.",
    },
    "installer.hint_no_movement": {
        "de": "Hinweis: '{id}' war schon vorher die aktive "
              "Sprache, und der Roboter hat keine Neuinstallation "
              "gemeldet. Falls du das Paket erneuern wolltest, weil "
              "etwas nicht stimmt: Stelle in der Dreamehome-App unter "
              "'Sprachton' auf eine andere Sprache und wieder zurück - "
              "dann lädt der Roboter es garantiert neu.\n\n",
        "en": "Note: '{id}' was already the active language "
              "before, and the robot didn't report a fresh install. "
              "If you wanted to renew the pack because something's "
              "wrong: switch to a different language in the "
              "Dreamehome app under 'Voice' and back again - that "
              "guarantees the robot reloads it.\n\n",
    },
    "installer.msg_original_active": {
        "de": "Das Originalpaket '{id}' ist wieder aktiv.",
        "en": "The original pack '{id}' is active again.",
    },
    "installer.err_no_confirmation_title": {
        "de": "Keine Bestätigung innerhalb der Wartezeit.",
        "en": "No confirmation within the wait time.",
    },
    "installer.err_no_confirmation_hint": {
        "de": "Der Auftrag wurde angenommen. Prüfe die Stimme am Roboter - "
              "oft ist die Installation trotzdem durchgelaufen. Alternativ "
              "lässt sich die Sprache jederzeit in der Dreamehome-App unter "
              "Einstellungen > Sprachpaket umstellen.",
        "en": "The order was accepted. Check the voice on the robot - "
              "the installation often went through anyway. Alternatively, "
              "the language can be changed any time in the Dreamehome "
              "app under Settings > Voice Pack.",
    },
})
