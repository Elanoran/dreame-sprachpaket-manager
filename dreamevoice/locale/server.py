"""German/English strings for server.py (the local HTTP server the robot downloads from)."""

from __future__ import annotations

from ..i18n import register

register({
    "server.pack_file_missing": {
        "de": "Die Paketdatei fehlt:\n{path}",
        "en": "The pack file is missing:\n{path}",
    },
    "server.log_download_complete": {
        "de": "Roboter ({client}) hat das Paket vollständig geladen.",
        "en": "Robot ({client}) has fully downloaded the pack.",
    },
    "server.log_request": {
        "de": "Roboter ({client}) fragt das Paket an [{what}]",
        "en": "Robot ({client}) is requesting the pack [{what}]",
    },
    "server.start_failed_title": {
        "de": "Der Webserver konnte auf Port {port} nicht starten.",
        "en": "The web server couldn't start on port {port}.",
    },
    "server.start_failed_hint": {
        "de": "Vermutlich ist der Port belegt. Wähle in den Einstellungen "
              "einen anderen Port. Technische Details: {details}",
        "en": "The port is probably in use. Choose a different port in "
              "the settings. Technical details: {details}",
    },
    "server.log_running": {
        "de": "Webserver läuft auf {url}",
        "en": "Web server running at {url}",
    },
    "server.log_stopped": {
        "de": "Webserver beendet.",
        "en": "Web server stopped.",
    },
    "server.reachability_hint": {
        "de": "Der Roboter hat das Paket nicht abgeholt. Die häufigsten "
              "Gründe:\n\n"
              "1. Die Windows-Firewall blockiert eingehende Verbindungen "
              "auf Port {port}. Beim ersten Start fragt Windows nach - "
              "dort muss 'Privates Netzwerk' erlaubt sein.\n"
              "2. PC und Roboter hängen in verschiedenen Netzen (z. B. "
              "Gast-WLAN, getrenntes IoT-WLAN, oder der PC ist per VPN "
              "verbunden).\n"
              "3. Der Roboter ist im Standby. Wecke ihn in der "
              "Dreamehome-App auf.\n\n"
              "Alternative: lade das Paket auf einen eigenen Webspace und "
              "trage die öffentliche URL im Feld 'Eigene URL' ein.",
        "en": "The robot didn't pick up the pack. The most common "
              "reasons:\n\n"
              "1. The Windows Firewall is blocking incoming connections "
              "on port {port}. Windows asks the first time you run this - "
              "'Private network' must be allowed there.\n"
              "2. The PC and robot are on different networks (e.g. guest "
              "Wi-Fi, separate IoT Wi-Fi, or the PC is connected via "
              "VPN).\n"
              "3. The robot is in standby. Wake it in the Dreamehome "
              "app.\n\n"
              "Alternative: upload the pack to your own web space and "
              "enter the public URL in the 'Custom URL' field.",
    },
})
