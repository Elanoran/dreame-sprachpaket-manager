"""English/German strings for dreamevoice/importer.py."""

from __future__ import annotations

from ..i18n import register

register({
    "importer.not_a_folder": {
        "de": "Das ist kein Ordner:\n{path}",
        "en": "That isn't a folder:\n{path}",
    },
    "importer.unknown_audio_format": {
        "de": "(kein bekanntes Audioformat)",
        "en": "(not a recognized audio format)",
    },
    "importer.no_number_in_name": {
        "de": "(keine Nummer im Namen)",
        "en": "(no number in the filename)",
    },
    # -- _TYPNAME: how each detected file type is named in messages -------
    "importer.type_rar": {"de": "RAR-Archiv", "en": "RAR archive"},
    "importer.type_7z": {"de": "7z-Archiv", "en": "7z archive"},
    "importer.type_bzip2": {"de": "bzip2-Archiv", "en": "bzip2 archive"},
    "importer.type_xz": {"de": "xz-Archiv", "en": "xz archive"},
    "importer.type_ogg": {"de": "Tondatei (OGG)", "en": "audio file (OGG)"},
    "importer.type_riff": {"de": "Tondatei (WAV)", "en": "audio file (WAV)"},
    "importer.type_mp3": {"de": "Tondatei (MP3)", "en": "audio file (MP3)"},
    "importer.type_flac": {"de": "Tondatei (FLAC)", "en": "audio file (FLAC)"},
    "importer.type_pdf": {"de": "PDF-Dokument", "en": "PDF document"},

    # -- ImportResult.summary() --------------------------------------------
    "importer.summary_count": {
        "de": "{count} Ansagen übernommen",
        "en": "{count} announcements taken over",
    },
    "importer.summary_unknown": {
        "de": "{count} Nummern kennt dein Modell nicht",
        "en": "{count} numbers your model doesn't recognize",
    },
    "importer.summary_skipped": {
        "de": "{count} Dateien übersprungen",
        "en": "{count} files skipped",
    },

    # -- _kein_archiv(): what the user picked instead of an archive -------
    "importer.err_empty_title": {
        "de": "Die Datei ist leer.",
        "en": "The file is empty.",
    },
    "importer.err_empty_hint": {
        "de": "'{name}' hat 0 Byte. Vermutlich ist der Download "
              "gescheitert oder wurde abgebrochen. Lade die Datei bitte "
              "noch einmal herunter.",
        "en": "'{name}' has 0 bytes. The download probably "
              "failed or was interrupted. Please download the file again.",
    },
    "importer.err_zip_incomplete_title": {
        "de": "Das Zip-Archiv ist unvollständig.",
        "en": "The ZIP archive is incomplete.",
    },
    "importer.err_zip_incomplete_hint": {
        "de": "Der Anfang der Datei ist ein Zip-Archiv, aber sein "
              "Inhaltsverzeichnis am Ende fehlt. Genau so sieht eine "
              "abgebrochene Übertragung aus.\n\n"
              "Lade die Datei bitte noch einmal herunter und warte, bis "
              "der Download wirklich fertig ist.\n\n"
              "Datei: {name} ({size})",
        "en": "The start of the file is a ZIP archive, but its directory "
              "at the end is missing. That's exactly what an interrupted "
              "transfer looks like.\n\n"
              "Please download the file again and wait until the download "
              "is really finished.\n\n"
              "File: {name} ({size})",
    },
    "importer.err_unsupported_archive_title": {
        "de": "Das ist ein {type_name} - damit kann die App nicht umgehen.",
        "en": "That's a {type_name} - the app can't handle those.",
    },
    "importer.err_unsupported_archive_hint": {
        "de": "Entpacke es bitte selbst und wähle danach entweder den "
              "entpackten Ordner oder packe die Ansagen als ZIP neu ein. "
              "ZIP und tar.gz versteht die App.",
        "en": "Please unpack it yourself and then choose either the "
              "unpacked folder or repack the announcements as a ZIP. "
              "The app understands ZIP and tar.gz.",
    },
    "importer.err_single_audio_title": {
        "de": "Das ist eine einzelne {type_name}, kein Archiv.",
        "en": "That's a single {type_name}, not an archive.",
    },
    "importer.err_single_audio_hint": {
        "de": "Hier wird ein ganzes Paket erwartet. Zwei Wege führen zum "
              "Ziel: Lege alle Ansagen in einen Ordner und wähle 'Ordner "
              "übernehmen' - oder packe den Ordner vorher als ZIP ein.",
        "en": "A whole pack is expected here. Two paths lead to the goal: "
              "put all announcements in a folder and choose 'Import "
              "Folder' - or ZIP the folder first.",
    },
    "importer.err_pdf_title": {
        "de": "Das ist ein PDF-Dokument, kein Sprachpaket.",
        "en": "That's a PDF document, not a voice pack.",
    },
    "importer.err_pdf_hint": {
        "de": "Erwartet wird ein ZIP- oder tar.gz-Archiv mit Ansagen, "
              "benannt wie 7.ogg oder 12.wav.",
        "en": "A ZIP or tar.gz archive with announcements named like "
              "7.ogg or 12.wav is expected.",
    },
    "importer.err_unknown_archive_title": {
        "de": "Die Datei ist kein Archiv, das die App lesen kann.",
        "en": "The file isn't an archive the app can read.",
    },
    "importer.err_unknown_archive_hint": {
        "de": "'{name}' beginnt weder wie ein ZIP noch wie ein "
              "tar.gz. Möglich ist auch, dass statt des Archivs eine "
              "Fehlerseite des Servers heruntergeladen wurde - dann hilft "
              "nur, sie noch einmal zu holen.",
        "en": "'{name}' starts like neither a ZIP nor a "
              "tar.gz. It's also possible that a server error page was "
              "downloaded instead of the archive - in that case, just "
              "fetch it again.",
    },

    # -- extract_archive(): discard reasons (shown via verworfen/hint) ----
    "importer.reason_more_than_expected": {
        "de": "mehr als erwartet",
        "en": "more than expected",
    },
    "importer.reason_too_large": {
        "de": "zu groß",
        "en": "too large",
    },
    "importer.reason_archive_too_large": {
        "de": "Archiv insgesamt zu groß",
        "en": "archive too large overall",
    },
    "importer.reason_larger_than_announced": {
        "de": "größer als angekündigt",
        "en": "larger than announced",
    },
    "importer.err_password_protected_title": {
        "de": "Das Archiv ist mit einem Kennwort geschützt.",
        "en": "The archive is password-protected.",
    },
    "importer.err_password_protected_hint": {
        "de": "Kennwortgeschützte Archive kann die App nicht "
              "öffnen. Entpacke es bitte selbst und wähle "
              "danach den entpackten Ordner - oder packe die "
              "Ansagen ohne Kennwort neu ein.\n\n"
              "Betroffen: {filename}",
        "en": "The app can't open password-protected archives. "
              "Please unpack it yourself and then choose the "
              "unpacked folder - or repack the announcements "
              "without a password.\n\n"
              "Affected: {filename}",
    },
    "importer.err_incomplete_read_title": {
        "de": "Das Archiv lässt sich nicht vollständig lesen.",
        "en": "The archive can't be read completely.",
    },
    "importer.err_incomplete_read_hint": {
        "de": "Das Inhaltsverzeichnis ist da, die Daten "
              "dahinter sind es nicht. So sieht ein "
              "unvollständig heruntergeladenes oder "
              "beschädigtes Archiv aus - lade es bitte noch "
              "einmal herunter.\n\n"
              "Betroffen: {filename}\n"
              "Technischer Grund: {reason}",
        "en": "The directory is there, but the data behind it "
              "isn't. That's what an incompletely downloaded "
              "or damaged archive looks like - please download "
              "it again.\n\n"
              "Affected: {filename}\n"
              "Technical reason: {reason}",
    },
    "importer.err_save_failed_title": {
        "de": "Eine Datei aus dem Archiv ließ sich nicht ablegen.",
        "en": "A file from the archive couldn't be saved.",
    },
    "importer.err_save_failed_hint": {
        "de": "Betroffen: {name}\n\nMögliche Gründe: der Name "
              "ist zu lang, die Platte ist voll, oder der "
              "Zielordner ist gesperrt.\n\nTechnische Details: "
              "{reason}",
        "en": "Affected: {name}\n\nPossible reasons: the name "
              "is too long, the disk is full, or the target "
              "folder is locked.\n\nTechnical details: "
              "{reason}",
    },
    "importer.err_tar_incomplete_title": {
        "de": "Das Archiv ist unvollständig oder beschädigt.",
        "en": "The archive is incomplete or damaged.",
    },
    "importer.err_tar_incomplete_hint": {
        "de": "Der Anfang der Datei ist ein gepacktes Archiv, "
              "aber es lässt sich nicht bis zum Ende entpacken. "
              "Am häufigsten liegt das an einem abgebrochenen "
              "Download - lade die Datei bitte noch einmal "
              "herunter.\n\n"
              "Technischer Grund: {reason}",
        "en": "The start of the file is a packed archive, but it "
              "can't be unpacked to the end. This is most often "
              "caused by an interrupted download - please download "
              "the file again.\n\n"
              "Technical reason: {reason}",
    },

    "importer.hint_expected_files": {
        "de": "Erwartet werden Dateien wie 7.ogg oder 12.wav.",
        "en": "Files like 7.ogg or 12.wav are expected.",
    },
    "importer.hint_discarded": {
        "de": "{count} Einträge wurden verworfen. Der erste: "
              "'{name}' ({reason}). Ein "
              "Sprachpaket besteht aus kurzen Ansagen von wenigen "
              "Sekunden.",
        "en": "{count} entries were discarded. The first: "
              "'{name}' ({reason}). A voice "
              "pack consists of short announcements a few "
              "seconds long.",
    },
    "importer.err_no_audio_title": {
        "de": "In dem Archiv waren keine brauchbaren Audiodateien.",
        "en": "The archive contained no usable audio files.",
    },
    "importer.log_unpacked": {
        "de": "{count} Dateien aus {archive} entpackt.",
        "en": "{count} files unpacked from {archive}.",
    },
    "importer.log_skipped_note": {
        "de": "Achtung: {count} Einträge wurden übersprungen "
              "({reason}, zuerst '{name}'). Das Paket "
              "ist dadurch unvollständig.",
        "en": "Note: {count} entries were skipped "
              "({reason}, first '{name}'). The pack "
              "is incomplete as a result.",
    },

    # -- create_template_folder() ------------------------------------------
    "importer.err_no_originals_title": {
        "de": "Es stehen keine Originalansagen bereit.",
        "en": "No original announcements are available.",
    },
    "importer.err_no_originals_hint": {
        "de": "Melde dich zuerst unter 'Start' an - das Originalpaket deines "
              "Roboters holt die App danach von selbst.",
        "en": "First sign in under 'Start' - the app then fetches your "
              "robot's original pack by itself.",
    },
    "importer.template_header": {
        "de": "So baust du dein eigenes Sprachpaket",
        "en": "How to build your own voice pack",
    },
    "importer.template_intro": {
        "de": "In diesem Ordner liegt jede Ansage deines Roboters - bereits richtig\n"
              "benannt. Die Zahl im Dateinamen ist die Ansage-Nummer.",
        "en": "This folder has every announcement from your robot - already\n"
              "correctly named. The number in the filename is the announcement number.",
    },
    "importer.template_step1": {
        "de": "1. Datei anhören, damit du weißt, was gesagt wird.",
        "en": "1. Listen to the file so you know what's said.",
    },
    "importer.template_step2": {
        "de": "2. Eigene Aufnahme unter GENAU DEMSELBEN NAMEN speichern.\n"
              "   (mp3, wav, m4a und flac gehen auch - die App wandelt um.)",
        "en": "2. Save your own recording under EXACTLY THE SAME NAME.\n"
              "   (mp3, wav, m4a, and flac work too - the app converts them.)",
    },
    "importer.template_step3": {
        "de": "3. Was du nicht ersetzt, einfach liegen lassen: diese Ansagen\n"
              "   bleiben auf der deutschen Originalstimme.",
        "en": "3. Whatever you don't replace, just leave alone: these announcements\n"
              "   stay on the German original voice.",
    },
    "importer.template_step4": {
        "de": "4. In der App auf 'Ganzen Ordner importieren' klicken und diesen\n"
              "   Ordner auswählen.",
        "en": "4. In the app, click 'Import Whole Folder' and choose this\n"
              "   folder.",
    },
    "importer.template_keep_short": {
        "de": "Halte die Aufnahmen kurz - die Originale sind zwei bis sechs Sekunden.",
        "en": "Keep the recordings short - the originals are two to six seconds.",
    },
    "importer.unknown_placeholder": {
        "de": "(unbekannt)",
        "en": "(unknown)",
    },
    "importer.instructions_filename": {
        "de": "_Anleitung.txt",
        "en": "_Instructions.txt",
    },
    "importer.log_copied": {
        "de": "{count} Originalansagen nach {target} kopiert.",
        "en": "{count} original announcements copied to {target}.",
    },
})
