"""German/English strings for dreamevoice/dialects/saechsisch.py.

Scope: only the dialect's display NAME and BESCHREIBUNG (shown in the
app's dialect picker). The TEXTE dict in that module is the actual
Saxon dialect script and is out of scope for this table.
"""

from __future__ import annotations

from ..i18n import register

register({
    "saechsisch.name": {
        "de": "Sächsisch",
        "en": "Saxon",
    },
    "saechsisch.beschreibung": {
        "de": (
            "Sächsisch mit weichen Konsonanten und einem herzlichen 'Nu'. "
            "Klingt immer ein bisschen freundlicher, als es gemeint ist."
        ),
        "en": (
            "Saxon dialect with soft consonants and a hearty 'Nu'. Always "
            "sounds a bit friendlier than it's meant."
        ),
    },
})
