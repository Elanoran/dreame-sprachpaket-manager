"""German/English strings for dreamevoice/dialects/berlinerisch.py.

Scope: only the dialect's display NAME and BESCHREIBUNG (shown in the
app's dialect picker). The TEXTE dict in that module is the actual
Berlin dialect script and is out of scope for this table.
"""

from __future__ import annotations

from ..i18n import register

register({
    "berlinerisch.name": {
        "de": "Berlinerisch",
        "en": "Berlin Dialect",
    },
    "berlinerisch.beschreibung": {
        "de": (
            "Berliner Schnauze: direkt, trocken, mit Herz. Beschwert sich gern, "
            "macht aber trotzdem sauber."
        ),
        "en": (
            "Berlin's famous 'Schnauze': blunt, dry, with heart. Loves to "
            "complain, but cleans anyway."
        ),
    },
})
