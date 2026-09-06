"""German/English strings for dreamevoice/community.py."""

from ..i18n import register

register({
    "community.packs_folder_name": {
        "de": "Community-Pakete",
        "en": "Community Packs",
    },
    "community.tag_funny": {"de": "lustig", "en": "funny"},
    "community.tag_ai": {"de": "KI", "en": "AI"},
    "community.tag_game": {"de": "Spiel", "en": "game"},
    "community.tag_movie": {"de": "Film", "en": "movie"},
    "community.tag_no_speech": {"de": "ohne Sprache", "en": "no speech"},
    "community.tag_extensive": {"de": "umfangreich", "en": "extensive"},
    "community.tag_language": {"de": "Sprache", "en": "language"},
    "community.tag_reference": {"de": "Referenz", "en": "reference"},

    "community.language_english": {"de": "Englisch", "en": "English"},
    "community.language_no_speech": {"de": "ohne Sprache", "en": "no speech"},
    "community.language_english_no_speech": {
        "de": "Englisch / ohne Sprache",
        "en": "English / no speech",
    },
    "community.language_ukrainian": {"de": "Ukrainisch", "en": "Ukrainian"},

    "community.license_none": {
        "de": "keine Lizenz angegeben",
        "en": "no license given",
    },
    "community.license_see_project": {
        "de": "siehe LICENSE im Projekt",
        "en": "see LICENSE in the project",
    },

    "community.name_glados_findus23": {
        "de": "GLaDOS (Variante 15.ai)",
        "en": "GLaDOS (15.ai variant)",
    },
    "community.name_glados_x40": {
        "de": "GLaDOS für X40 (514 Ansagen)",
        "en": "GLaDOS for X40 (514 announcements)",
    },
    "community.name_uk_female_pensive": {
        "de": "Ukrainisch (weiblich, ruhig)",
        "en": "Ukrainian (female, calm)",
    },
    "community.name_original_en": {
        "de": "Original Englisch (Sicherung)",
        "en": "Original English (backup)",
    },

    "community.desc_glados_zigerschlitz": {
        "de": "Die sarkastische KI aus dem Spiel Portal. Der am besten "
              "gepflegte GLaDOS-Satz, als fertiges Archiv mit "
              "veröffentlichter Prüfsumme.",
        "en": "The sarcastic AI from the game Portal. The best-maintained "
              "GLaDOS set, as a ready-made archive with a published "
              "checksum.",
    },
    "community.desc_r2d2": {
        "de": "Statt Sätzen nur Piepen und Zwitschern des Star-Wars-Droiden. "
              "Sehr unterhaltsam, aber man erfährt nicht mehr, was der "
              "Roboter eigentlich meldet.",
        "en": "Just beeps and chirps from the Star Wars droid instead of "
              "sentences. Very entertaining, but you no longer know what "
              "the robot is actually reporting.",
    },
    "community.desc_memes": {
        "de": "Internet-Meme-Sounds statt der üblichen Ansagen.",
        "en": "Internet meme sounds instead of the usual announcements.",
    },
    "community.desc_glados_findus23": {
        "de": "Ältere GLaDOS-Fassung, mit der Sprachsynthese 15.ai erzeugt. "
              "Andere Betonung als die Variante oben.",
        "en": "Older GLaDOS version, generated with the 15.ai speech "
              "synthesizer. Different intonation than the variant above.",
    },
    "community.desc_glados_x40": {
        "de": "Mit Abstand der umfangreichste Satz: alle 514 Ansagen des "
              "X40 Ultra neu getextet und mit Kokoro-TTS gesprochen. Da "
              "X40 und X50 sich 513 Nummern teilen, deckt dieses Paket "
              "fast den kompletten X50 ab.",
        "en": "By far the most extensive set: all 514 announcements of "
              "the X40 Ultra rewritten and spoken with Kokoro TTS. Since "
              "the X40 and X50 share 513 numbers, this pack covers almost "
              "the entire X50.",
    },
    "community.desc_uk_female_pensive": {
        "de": "Ukrainische Ansagen, ruhig und sachlich gesprochen.",
        "en": "Ukrainian announcements, spoken calmly and matter-of-factly.",
    },
    "community.desc_original_en": {
        "de": "Die englischen Originalansagen eines älteren Modells. Vor "
              "allem als Vergleichsmaterial nützlich.",
        "en": "The original English announcements of an older model. "
              "Mainly useful as reference material.",
    },

    "community.notes_r2d2": {
        "de": "Achtung: Fehlermeldungen sind danach nicht mehr verständlich.",
        "en": "Note: error messages are no longer intelligible after this.",
    },
    "community.notes_x40": {
        "de": "Wird als Projektarchiv geladen; die App holt sich die "
              "Ogg-Dateien daraus. Größe und Prüfsumme ändern sich mit "
              "jeder Aktualisierung des Projekts und werden daher nicht "
              "fest geprüft.",
        "en": "Downloaded as a project archive; the app extracts the Ogg "
              "files from it. Size and checksum change with every update "
              "to the project, so they aren't checked against a fixed "
              "value.",
    },

    "community.source_not_allowed_message": {
        "de": "Die Bezugsadresse von '{name}' ist nicht zulässig.",
        "en": "'{name}''s source address isn't allowed.",
    },
    "community.source_not_allowed_hint": {
        "de": "Fremdpakete werden nur von GitHub geladen.\n\nAdresse: {url}",
        "en": "Third-party packs are only downloaded from GitHub.\n\n"
              "Address: {url}",
    },
    "community.download_failed_http": {
        "de": "Download fehlgeschlagen (HTTP {status}).",
        "en": "Download failed (HTTP {status}).",
    },
    "community.download_failed_http_hint": {
        "de": "Quelle: {url}",
        "en": "Source: {url}",
    },
    "community.pack_too_large_message": {
        "de": "'{name}' ist unerwartet groß.",
        "en": "'{name}' is unexpectedly large.",
    },
    "community.pack_too_large_hint": {
        "de": "Der Download wurde abgebrochen. Ein Sprachpaket wiegt rund "
              "zehn Megabyte.",
        "en": "The download was aborted. A voice pack weighs about ten "
              "megabytes.",
    },
    "community.download_request_failed": {
        "de": "Das Paket '{name}' konnte nicht geladen werden.",
        "en": "The pack '{name}' couldn't be downloaded.",
    },
    "community.download_technical_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "community.checksum_mismatch_message": {
        "de": "Die Prüfsumme von '{name}' stimmt nicht.",
        "en": "'{name}''s checksum doesn't match.",
    },
    "community.checksum_mismatch_hint": {
        "de": "Erwartet {expected}, erhalten {actual}. Der Download wurde "
              "verworfen - die Datei wird nicht verwendet.",
        "en": "Expected {expected}, got {actual}. The download was "
              "discarded - the file won't be used.",
    },
})
