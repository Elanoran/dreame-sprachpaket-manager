"""German/English strings for dreamevoice/dialects/schwaebisch.py.

Scope: only the dialect's display NAME and BESCHREIBUNG (shown in the
app's dialect picker). The TEXTE dict in that module is the actual
Swabian dialect script and is out of scope for this table.
"""

from __future__ import annotations

from ..i18n import register

register({
    "schwaebisch.name": {
        "de": "Schwäbisch",
        "en": "Swabian",
    },
    "schwaebisch.beschreibung": {
        "de": (
            "Stuggerter Schwäbisch. Fleissig, gründlich und mit dem nötigen "
            "Respekt vor der Kehrwoche."
        ),
        "en": (
            "Stuttgart-style Swabian. Diligent, thorough, and with due "
            "respect for the cleaning rota."
        ),
    },
})
