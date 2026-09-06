"""German/English strings for dreamevoice/dialects/koelsch.py.

Scope: only the dialect's display NAME and BESCHREIBUNG (shown in the
app's dialect picker). The TEXTE dict in that module is the actual
Cologne dialect script and is out of scope for this table.
"""

from __future__ import annotations

from ..i18n import register

register({
    "koelsch.name": {
        "de": "Kölsch",
        "en": "Kölsch",
    },
    "koelsch.beschreibung": {
        "de": (
            "Rheinisch-kölsch: gut gelaunt, nimmt nichts zu schwer. "
            "Et hätt noch immer joot jejange."
        ),
        "en": (
            "Cologne's Kölsch dialect: good-humored, doesn't take anything "
            "too seriously. Et hätt noch immer joot jejange."
        ),
    },
})
