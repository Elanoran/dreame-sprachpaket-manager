"""German/English strings for dreamevoice/dialects/bayerisch.py.

Scope: only the dialect's display NAME and BESCHREIBUNG (shown in the
app's dialect picker). The TEXTE dict in that module is the actual
Bavarian dialect script and is out of scope for this table.
"""

from __future__ import annotations

from ..i18n import register

register({
    "bayerisch.name": {
        "de": "Bayerisch",
        "en": "Bavarian",
    },
    "bayerisch.beschreibung": {
        "de": (
            "Modernes Altbayerisch, wie es in und um München geredet wird: "
            "lautgetreu geschrieben, mit Grant und Witz an den richtigen Stellen."
        ),
        "en": (
            "Modern Old Bavarian, as spoken in and around Munich: written "
            "phonetically, with grumpiness and wit in the right places."
        ),
    },
})
