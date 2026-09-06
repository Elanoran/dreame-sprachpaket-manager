"""German/English strings for dreamevoice/dialects/wienerisch.py.

Scope: only the dialect's display NAME and BESCHREIBUNG (shown in the
app's dialect picker). The TEXTE dict in that module is the actual
Viennese dialect script and is out of scope for this table.
"""

from __future__ import annotations

from ..i18n import register

register({
    "wienerisch.name": {
        "de": "Wienerisch",
        "en": "Viennese",
    },
    "wienerisch.beschreibung": {
        "de": (
            "Wienerisch, wie es in der Stadt geredet wird: lautgetreu geschrieben "
            "und leicht grantig. Kein Bairisch mit Wiener Anstrich."
        ),
        "en": (
            "Viennese, as spoken in the city: written phonetically and "
            "slightly grumpy. Not Bavarian with a Viennese coat of paint."
        ),
    },
})
