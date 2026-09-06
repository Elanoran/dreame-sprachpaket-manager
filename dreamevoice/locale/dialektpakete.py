"""German/English strings for dreamevoice/dialektpakete.py.

Scope: only the KATALOG list's `name`/`beschreibung`/`geschlecht` fields
(the ready-made dialect entries shown in the download picker). Every
other user-facing string in that module (log messages, error messages)
belongs to a different batch of this rollout.
"""

from __future__ import annotations

from ..i18n import register

register({
    "dialektpakete.katalog_bayerisch_name": {
        "de": "Bayerisch",
        "en": "Bavarian",
    },
    "dialektpakete.katalog_bayerisch_beschreibung": {
        "de": "Oberbayerisch, wie man es um München herum spricht.",
        "en": "Upper Bavarian, as spoken around Munich.",
    },
    "dialektpakete.katalog_bayerisch_weiblich_name": {
        "de": "Bayerisch",
        "en": "Bavarian",
    },
    "dialektpakete.katalog_bayerisch_weiblich_beschreibung": {
        "de": "Oberbayerisch, wie man es um München herum spricht.",
        "en": "Upper Bavarian, as spoken around Munich.",
    },
    "dialektpakete.katalog_bayerisch_weiblich_geschlecht": {
        "de": "weiblich",
        "en": "female",
    },
    "dialektpakete.katalog_hessisch_name": {
        "de": "Hessisch",
        "en": "Hessian",
    },
    "dialektpakete.katalog_hessisch_beschreibung": {
        "de": "Frankfurterisch aus dem Rhein-Main-Gebiet.",
        "en": "Frankfurt-style Hessian from the Rhine-Main area.",
    },
    "dialektpakete.katalog_wienerisch_name": {
        "de": "Wienerisch",
        "en": "Viennese",
    },
    "dialektpakete.katalog_wienerisch_beschreibung": {
        "de": "Wiener Umgangssprache, kein Bühnendialekt.",
        "en": "Viennese vernacular, not stage dialect.",
    },
    "dialektpakete.katalog_berlinerisch_name": {
        "de": "Berlinerisch",
        "en": "Berlin Dialect",
    },
    "dialektpakete.katalog_berlinerisch_beschreibung": {
        "de": "Berliner Schnauze, mit dem harten j statt g.",
        "en": "Berlin's Schnauze, with the hard j instead of g.",
    },
})
