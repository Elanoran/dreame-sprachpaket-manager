"""German/English strings for dreamevoice/vorhoeren.py."""

from ..i18n import register

register({
    "vorhoeren.announcement_plain": {
        "de": "Ansage {nummer}",
        "en": "Announcement {nummer}",
    },
    "vorhoeren.announcement_with_title": {
        "de": "Ansage {nummer} · {title}",
        "en": "Announcement {nummer} · {title}",
    },
    "vorhoeren.no_announcement_to_preview": {
        "de": "In diesem Paket ist keine Ansage zum Anhören.",
        "en": "There's no announcement in this pack to preview.",
    },
    "vorhoeren.ffmpeg_needed": {
        "de": "Zum Anhören wird ffmpeg gebraucht - es ließ sich nicht nutzen.",
        "en": "ffmpeg is needed to preview - it couldn't be used.",
    },
})
