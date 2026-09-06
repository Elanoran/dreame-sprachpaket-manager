"""German/English strings for dreamevoice/cloud.py."""

from ..i18n import register

register({
    "cloud.region_eu": {
        "de": "Europa (Deutschland, Österreich, Schweiz)",
        "en": "Europe (Germany, Austria, Switzerland)",
    },
    "cloud.region_us": {
        "de": "Nord-/Südamerika",
        "en": "North/South America",
    },
    "cloud.region_sg": {
        "de": "Asien-Pazifik",
        "en": "Asia-Pacific",
    },
    "cloud.region_ru": {
        "de": "Russland",
        "en": "Russia",
    },
    "cloud.region_cn": {
        "de": "China (Festland)",
        "en": "China (Mainland)",
    },
    "cloud.login_empty_credentials": {
        "de": "E-Mail und Passwort dürfen nicht leer sein.",
        "en": "Email and password must not be empty.",
    },
    "cloud.ssl_error_message": {
        "de": "Die gesicherte Verbindung zum Dreame-Server kam nicht zustande.",
        "en": "The secure connection to the Dreame server didn't come through.",
    },
    "cloud.ssl_error_hint": {
        "de": "Prüfe, ob eine Firewall, ein VPN oder ein Virenscanner mit "
              "HTTPS-Scan dazwischenfunkt.",
        "en": "Check whether a firewall, VPN, or antivirus with HTTPS "
              "scanning is interfering.",
    },
    "cloud.timeout_message": {
        "de": "Der Dreame-Server hat nicht rechtzeitig geantwortet.",
        "en": "The Dreame server didn't respond in time.",
    },
    "cloud.timeout_hint": {
        "de": "Prüfe deine Internetverbindung und versuche es erneut.",
        "en": "Check your internet connection and try again.",
    },
    "cloud.request_error_message": {
        "de": "Der Dreame-Server ist nicht erreichbar.",
        "en": "The Dreame server can't be reached.",
    },
    "cloud.technical_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "cloud.login_rejected": {
        "de": "E-Mail oder Passwort wurde nicht akzeptiert.",
        "en": "Email or password wasn't accepted.",
    },
    "cloud.login_rejected_hint": {
        "de": "Prüfe die Zugangsdaten in der Dreamehome-App. Achte auch auf "
              "die richtige Region: Konten aus Deutschland liegen fast immer "
              "auf 'Europa'.",
        "en": "Check your credentials in the Dreamehome app. Also check the "
              "right region: accounts from Germany are almost always on "
              "'Europe'.",
    },
    "cloud.signin_rejected_http": {
        "de": "Die Anmeldung wurde abgelehnt (HTTP {status}).",
        "en": "The sign-in was rejected (HTTP {status}).",
    },
    "cloud.no_further_explanation": {
        "de": "Keine nähere Begründung vom Server.",
        "en": "No further explanation from the server.",
    },
    "cloud.response_unreadable": {
        "de": "Die Antwort des Servers war unlesbar.",
        "en": "The server's response was unreadable.",
    },
    "cloud.no_access_token": {
        "de": "Der Server hat kein Zugriffstoken geliefert.",
        "en": "The server didn't provide an access token.",
    },
    "cloud.response_detail": {
        "de": "Antwort: {data}",
        "en": "Response: {data}",
    },
    "cloud.signin_failed_any_region": {
        "de": "Anmeldung in keiner Region erfolgreich.",
        "en": "Sign-in did not succeed in any region.",
    },
    "cloud.not_signed_in": {
        "de": "Nicht angemeldet.",
        "en": "Not signed in.",
    },
    "cloud.server_http_status": {
        "de": "Der Dreame-Server antwortete mit HTTP {status}.",
        "en": "The Dreame server responded with HTTP {status}.",
    },
    "cloud.request_failed": {
        "de": "Die Anfrage an den Dreame-Server ist fehlgeschlagen.",
        "en": "The request to the Dreame server failed.",
    },
    "cloud.device_list_failed": {
        "de": "Die Geräteliste konnte nicht geladen werden.",
        "en": "The device list couldn't be loaded.",
    },
    "cloud.server_response_detail": {
        "de": "Antwort des Servers: {data}",
        "en": "Server response: {data}",
    },
    "cloud.device_data_failed": {
        "de": "Die Gerätedaten konnten nicht geladen werden.",
        "en": "The device data couldn't be loaded.",
    },
    "cloud.robot_no_response": {
        "de": "Der Roboter hat auf den Befehl nicht geantwortet.",
        "en": "The robot didn't respond to the command.",
    },
    "cloud.robot_no_response_hint": {
        "de": "Er ist vermutlich offline oder im Standby. Wecke ihn in der "
              "Dreamehome-App auf und versuche es erneut.",
        "en": "It's probably offline or in standby. Wake it in the "
              "Dreamehome app and try again.",
    },
})
