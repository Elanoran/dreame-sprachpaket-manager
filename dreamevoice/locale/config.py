"""German/English strings for dreamevoice/config.py.

Scope: only Config.password_location and Config.elevenlabs_key_location -
the rest of config.py (DEFAULTS, DPAPI code, comments) is internal and
not user-facing.
"""

from ..i18n import register

register({
    "config.location_credential_manager": {
        "de": "Windows-Anmeldeinformationsspeicher",
        "en": "Windows Credential Manager",
    },
    "config.location_config_encrypted": {
        "de": "config.json (verschlüsselt mit deinem Windows-Konto)",
        "en": "config.json (encrypted with your Windows account)",
    },
    "config.location_not_saved": {
        "de": "nicht gespeichert",
        "en": "not saved",
    },
})
