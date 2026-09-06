"""German/English strings for dreamevoice/dialects/hessisch.py.

Scope: only the dialect's display NAME and BESCHREIBUNG (shown in the
app's dialect picker). The TEXTE dict in that module is the actual
Hessian dialect script and is out of scope for this table.
"""

from __future__ import annotations

from ..i18n import register

register({
    "hessisch.name": {
        "de": "Hessisch",
        "en": "Hessian",
    },
    "hessisch.beschreibung": {
        "de": (
            "Frankfurterisch aus dem Rhein-Main-Gebiet: lautgetreu geschrieben, "
            "gutgelaunt und geschwätzig. Ei gude, wie?"
        ),
        "en": (
            "Frankfurt-style Hessian from the Rhine-Main area: written "
            "phonetically, good-humored and chatty. Ei gude, wie?"
        ),
    },
})
