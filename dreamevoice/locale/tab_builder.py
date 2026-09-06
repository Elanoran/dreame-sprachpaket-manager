"""German/English strings for ui/tab_builder.py (the 'Individual Announcements' tab)."""

from __future__ import annotations

from ..i18n import register

register({
    "tab_builder.filetype_audio": {
        "de": "Audiodateien",
        "en": "Audio files",
    },
    "tab_builder.filetype_ogg": {
        "de": "OGG Vorbis (bereits passend)",
        "en": "OGG Vorbis (already correct)",
    },
    "tab_builder.filetype_all": {
        "de": "Alle Dateien",
        "en": "All files",
    },
    "tab_builder.no_description": {
        "de": "keine Beschreibung bekannt - bitte anhören",
        "en": "no description known - please listen",
    },
    "tab_builder.listen_original": {
        "de": "Original anhören",
        "en": "Listen to Original",
    },
    "tab_builder.browse_button": {
        "de": "Durchsuchen ...",
        "en": "Browse ...",
    },
    "tab_builder.no_preview_title": {
        "de": "Keine Hörprobe",
        "en": "No Preview Available",
    },
    "tab_builder.no_preview_body": {
        "de": "Lade zuerst oben das offizielle Sprachpaket deines Roboters "
              "herunter - daraus stammen die Hörproben.",
        "en": "First download your robot's official voice pack above - "
              "the previews come from that.",
    },
    "tab_builder.playback_error_title": {
        "de": "Wiedergabe nicht möglich",
        "en": "Playback Not Possible",
    },
    "tab_builder.playback_error_body": {
        "de": "Die Datei konnte nicht abgespielt werden.\n\n{path}\n\n{exc}",
        "en": "The file couldn't be played back.\n\n{path}\n\n{exc}",
    },
    "tab_builder.browse_dialog_title": {
        "de": "Audiodatei für Ansage {id} - {title}   (erwarteter Name: {filename})",
        "en": "Audio File for Announcement {id} - {title}   (expected name: {filename})",
    },
    "tab_builder.file_missing": {
        "de": "Diese Datei existiert nicht (mehr).",
        "en": "This file no longer exists.",
    },
    "tab_builder.file_ready": {
        "de": "Bereit: {name} ({size_kb} KB)",
        "en": "Ready: {name} ({size_kb} KB)",
    },
    "tab_builder.info_banner": {
        "de": "Dein Paket entsteht als Kopie des offiziellen Sprachpakets deines "
              "Roboters - ausgetauscht wird nur, was du selbst zuweist. Alles andere "
              "bleibt auf der originalen deutschen Stimme. Deshalb ist der erste "
              "Schritt immer das Laden des Originalpakets.",
        "en": "Your pack is built as a copy of your robot's official voice "
              "pack - only what you assign yourself gets replaced. Everything "
              "else stays on the original German voice. That's why the first "
              "step is always loading the original pack.",
    },
    "tab_builder.step1_title": {
        "de": "Schritt 1: Originalpaket laden",
        "en": "Step 1: Load Original Pack",
    },
    "tab_builder.step1_body": {
        "de": "Grundlage und zugleich Sicherheitsnetz - daraus kommen auch "
              "die Hörproben.",
        "en": "The foundation and safety net at the same time - the "
              "previews come from here too.",
    },
    "tab_builder.language_label": {
        "de": "Sprache",
        "en": "Language",
    },
    "tab_builder.default_language_value": {
        "de": "Deutsch (DE)",
        "en": "German (DE)",
    },
    "tab_builder.download_pack_button": {
        "de": "Originalpaket herunterladen",
        "en": "Download Original Pack",
    },
    "tab_builder.not_loaded_yet": {
        "de": "Noch nicht geladen",
        "en": "Not loaded yet",
    },
    "tab_builder.ffmpeg_setup_button": {
        "de": "ffmpeg automatisch einrichten",
        "en": "Set Up ffmpeg Automatically",
    },
    "tab_builder.step2_title": {
        "de": "Schritt 2: Ansagen austauschen",
        "en": "Step 2: Replace Announcements",
    },
    "tab_builder.step2_body": {
        "de": "Wähle je Ansage eine eigene Audiodatei. Formate wie mp3 "
              "oder wav werden beim Bauen automatisch umgewandelt.",
        "en": "Choose a custom audio file per announcement. Formats "
              "like mp3 or wav are converted automatically when building.",
    },
    "tab_builder.search_label": {
        "de": "Suche",
        "en": "Search",
    },
    "tab_builder.category_label": {
        "de": "Bereich",
        "en": "Category",
    },
    "tab_builder.all_categories": {
        "de": "Alle Bereiche",
        "en": "All Categories",
    },
    "tab_builder.only_common_checkbox": {
        "de": "nur die wichtigsten",
        "en": "only the most important",
    },
    "tab_builder.only_assigned_checkbox": {
        "de": "nur bereits zugewiesene",
        "en": "only already assigned",
    },
    "tab_builder.clear_all_button": {
        "de": "Alle Zuweisungen löschen",
        "en": "Clear All Assignments",
    },
    "tab_builder.import_folder_button": {
        "de": "Ganzen Ordner importieren ...",
        "en": "Import Whole Folder ...",
    },
    "tab_builder.import_archive_button": {
        "de": "Aus Archiv importieren ...",
        "en": "Import from Archive ...",
    },
    "tab_builder.create_template_button": {
        "de": "Vorlagenordner anlegen ...",
        "en": "Create Template Folder ...",
    },
    "tab_builder.bulk_hint": {
        "de": "Die Zahl im Dateinamen ist die Ansage-Nummer: 7.ogg, 007.wav "
              "oder '7 - Reinigung.mp3' landen alle bei Ansage 7.",
        "en": "The number in the filename is the announcement number: "
              "7.ogg, 007.wav, or '7 - Cleaning.mp3' all land on "
              "announcement 7.",
    },
    "tab_builder.show_more_button": {
        "de": "Weitere anzeigen",
        "en": "Show More",
    },
    "tab_builder.show_more_count": {
        "de": "Weitere {count} anzeigen",
        "en": "Show {count} More",
    },
    "tab_builder.ffmpeg_ready": {
        "de": "Audio-Umwandlung bereit ({info}).",
        "en": "Audio conversion ready ({info}).",
    },
    "tab_builder.ffmpeg_unpacking": {
        "de": "ffmpeg ist in der App enthalten und wird einmalig "
              "ausgepackt ...",
        "en": "ffmpeg is built into the app and is being "
              "unpacked once ...",
    },
    "tab_builder.ffmpeg_not_found": {
        "de": "ffmpeg wurde nicht gefunden. Ohne ffmpeg lassen sich nur "
              "fertige .ogg-Dateien (Vorbis, mono, 16000 Hz) verwenden - "
              "mp3 und wav können dann nicht umgewandelt werden. "
              "Abhilfe: entweder ffmpeg.exe in denselben Ordner wie diese "
              "App legen, oder die Schaltfläche unten benutzen.",
        "en": "ffmpeg wasn't found. Without ffmpeg, only ready-made "
              ".ogg files (Vorbis, mono, 16000 Hz) can be used - mp3 "
              "and wav can't be converted. Fix: either place ffmpeg.exe "
              "in the same folder as this app, or use the button below.",
    },
    "tab_builder.ffmpeg_unpack_failed": {
        "de": "Das mitgelieferte ffmpeg ließ sich nicht auspacken. "
              "Lege ersatzweise eine ffmpeg.exe neben die App.",
        "en": "The bundled ffmpeg couldn't be unpacked. Place "
              "an ffmpeg.exe next to the app instead.",
    },
    "tab_builder.ffmpeg_setup_confirm_title": {
        "de": "ffmpeg einrichten",
        "en": "Set Up ffmpeg",
    },
    "tab_builder.ffmpeg_setup_confirm_question": {
        "de": "\n\nJetzt herunterladen?",
        "en": "\n\nDownload now?",
    },
    "tab_builder.ffmpeg_downloading": {
        "de": "Lade ffmpeg herunter (etwa 170 MB) ...",
        "en": "Downloading ffmpeg (about 170 MB) ...",
    },
    "tab_builder.ffmpeg_downloading_progress": {
        "de": "Lade ffmpeg herunter ... {done_mb} von {total_mb} MB",
        "en": "Downloading ffmpeg ... {done_mb} of {total_mb} MB",
    },
    "tab_builder.ffmpeg_setup_done_title": {
        "de": "ffmpeg eingerichtet",
        "en": "ffmpeg Set Up",
    },
    "tab_builder.ffmpeg_setup_done_body": {
        "de": "ffmpeg ist jetzt einsatzbereit. mp3-, wav- und "
              "m4a-Dateien werden ab sofort automatisch "
              "umgewandelt.",
        "en": "ffmpeg is now ready to use. mp3, wav, and "
              "m4a files will be converted automatically "
              "from now on.",
    },
    "tab_builder.ffmpeg_setup_failed_title": {
        "de": "ffmpeg-Einrichtung fehlgeschlagen",
        "en": "ffmpeg Setup Failed",
    },
    "tab_builder.languages_available": {
        "de": "{count} offizielle Sprachen verfügbar",
        "en": "{count} official languages available",
    },
    "tab_builder.language_list_error": {
        "de": "Sprachliste nicht abrufbar",
        "en": "Language List Not Available",
    },
    "tab_builder.no_robot_title": {
        "de": "Kein Roboter ausgewählt",
        "en": "No Robot Selected",
    },
    "tab_builder.no_robot_body": {
        "de": "Melde dich zuerst unter 'Verbindung' an und wähle deinen Roboter.",
        "en": "Sign in under 'Connection' first and choose your robot.",
    },
    "tab_builder.loading_languages_title": {
        "de": "Sprachliste wird geladen",
        "en": "Loading Language List",
    },
    "tab_builder.loading_languages_body": {
        "de": "Die Liste der offiziellen Sprachpakete wird gerade abgerufen. "
              "Bitte gleich noch einmal klicken.",
        "en": "The list of official voice packs is being fetched. "
              "Please click again in a moment.",
    },
    "tab_builder.no_language_title": {
        "de": "Keine Sprache gewählt",
        "en": "No Language Chosen",
    },
    "tab_builder.no_language_body": {
        "de": "Bitte wähle ein offizielles Sprachpaket aus.",
        "en": "Please choose an official voice pack.",
    },
    "tab_builder.loading_pack": {
        "de": "Lade Originalpaket ...",
        "en": "Loading original pack ...",
    },
    "tab_builder.extracting_samples": {
        "de": "Entpacke Hörproben ...",
        "en": "Extracting samples ...",
    },
    "tab_builder.pack_ready": {
        "de": "Bereit - {summary}",
        "en": "Ready - {summary}",
    },
    "tab_builder.download_failed_title": {
        "de": "Download fehlgeschlagen",
        "en": "Download Failed",
    },
    "tab_builder.original_pack_not_loaded_title": {
        "de": "Originalpaket nicht geladen",
        "en": "Original Pack Not Loaded",
    },
    "tab_builder.no_matches": {
        "de": "Zu diesen Filtern gibt es keine Ansagen.",
        "en": "No announcements match these filters.",
    },
    "tab_builder.counter_replaced": {
        "de": "{assigned} von {total} Ansagen ausgetauscht",
        "en": "{assigned} of {total} announcements replaced",
    },
    "tab_builder.counter_shown": {
        "de": "  ·  {shown} angezeigt",
        "en": "  ·  {shown} shown",
    },
    "tab_builder.counter_missing": {
        "de": "  ·  {missing} Zuweisung(en) zeigen auf fehlende Dateien",
        "en": "  ·  {missing} assignment(s) point to missing files",
    },
    "tab_builder.choose_audio_folder_title": {
        "de": "Ordner mit deinen Audiodateien wählen",
        "en": "Choose the Folder with Your Audio Files",
    },
    "tab_builder.choose_archive_title": {
        "de": "Sprachpaket oder Archiv wählen",
        "en": "Choose a Voice Pack or Archive",
    },
    "tab_builder.filetype_archives": {
        "de": "Archive",
        "en": "Archives",
    },
    "tab_builder.filetype_all_archive": {
        "de": "Alle Dateien",
        "en": "All files",
    },
    "tab_builder.imported_folder_name": {
        "de": "Importiert",
        "en": "Imported",
    },
    "tab_builder.import_nothing_found_title": {
        "de": "Nichts gefunden",
        "en": "Nothing Found",
    },
    "tab_builder.import_nothing_found_line1": {
        "de": "In der Auswahl war keine verwertbare Audiodatei.",
        "en": "No usable audio file was in the selection.",
    },
    "tab_builder.import_nothing_found_line2": {
        "de": "Die Dateien müssen die Ansage-Nummer im Namen tragen, "
              "zum Beispiel 7.ogg oder 12.wav.\n\n",
        "en": "Files need the announcement number in their name, "
              "e.g. 7.ogg or 12.wav.\n\n",
    },
    "tab_builder.import_summary_header": {
        "de": "{count} Ansagen gefunden:\n\n",
        "en": "{count} announcements found:\n\n",
    },
    "tab_builder.import_summary_new": {
        "de": "· {count} neu zugewiesen\n",
        "en": "· {count} newly assigned\n",
    },
    "tab_builder.import_summary_overwritten": {
        "de": "· {count} bereits zugewiesene werden überschrieben\n",
        "en": "· {count} already-assigned ones will be overwritten\n",
    },
    "tab_builder.import_summary_unknown": {
        "de": "· {count} Nummern kennt dein Modell nicht und werden ausgelassen\n",
        "en": "· {count} numbers your model doesn't recognize will be skipped\n",
    },
    "tab_builder.import_summary_skipped": {
        "de": "· {count} Dateien übersprungen\n",
        "en": "· {count} files skipped\n",
    },
    "tab_builder.import_summary_apply": {
        "de": "\nÜbernehmen?",
        "en": "\nApply?",
    },
    "tab_builder.review_import_title": {
        "de": "Import prüfen",
        "en": "Review Import",
    },
    "tab_builder.import_complete_title": {
        "de": "Import fertig",
        "en": "Import Complete",
    },
    "tab_builder.import_failed_title": {
        "de": "Import fehlgeschlagen",
        "en": "Import Failed",
    },
    "tab_builder.unknown_numbers_prefix": {
        "de": "Unbekannte Ansage-Nummern: ",
        "en": "Unknown announcement numbers: ",
    },
    "tab_builder.skipped_label": {
        "de": "Übersprungen:",
        "en": "Skipped:",
    },
    "tab_builder.skipped_more": {
        "de": "   ... und {count} weitere",
        "en": "   ... and {count} more",
    },
    "tab_builder.original_pack_missing_title": {
        "de": "Originalpaket fehlt",
        "en": "Original Pack Missing",
    },
    "tab_builder.original_pack_missing_line1": {
        "de": "Für den Vorlagenordner werden die Originalansagen gebraucht.",
        "en": "The template folder needs the original announcements.",
    },
    "tab_builder.original_pack_missing_line2": {
        "de": "Lade oben in Schritt 1 zuerst das offizielle Sprachpaket "
              "deines Roboters herunter.",
        "en": "First download your robot's official voice pack above, in "
              "step 1.",
    },
    "tab_builder.choose_scope_title": {
        "de": "Umfang wählen",
        "en": "Choose Scope",
    },
    "tab_builder.choose_scope_question": {
        "de": "Sollen nur die wichtigsten Ansagen in den Vorlagenordner?\n\n",
        "en": "Should only the most important announcements go into the "
              "template folder?\n\n",
    },
    "tab_builder.choose_scope_yes": {
        "de": "Ja  = {count} Ansagen (empfohlen für den Anfang)\n",
        "en": "Yes = {count} announcements (recommended to start with)\n",
    },
    "tab_builder.choose_scope_no": {
        "de": "Nein = alle {count} Ansagen",
        "en": "No = all {count} announcements",
    },
    "tab_builder.template_folder_dialog_title": {
        "de": "Wo soll der Vorlagenordner entstehen?",
        "en": "Where Should the Template Folder Go?",
    },
    "tab_builder.my_announcements_folder": {
        "de": "Meine Ansagen",
        "en": "My Announcements",
    },
    "tab_builder.template_created_title": {
        "de": "Vorlagenordner angelegt",
        "en": "Template Folder Created",
    },
    "tab_builder.template_created_line1": {
        "de": "{count} Originalansagen liegen jetzt in:\n{path}",
        "en": "{count} original announcements are now in:\n{path}",
    },
    "tab_builder.template_created_line2": {
        "de": "So geht es weiter:\n"
              "1. Datei anhören, damit du weißt, was gesagt wird.\n"
              "2. Eigene Aufnahme unter genau demselben Namen speichern.\n"
              "3. Hier auf 'Ganzen Ordner importieren' klicken.\n\n"
              "Eine Anleitung liegt als _Anleitung.txt im Ordner. "
              "Der Ordner wird jetzt geöffnet.",
        "en": "How to proceed:\n"
              "1. Listen to a file so you know what's said.\n"
              "2. Save your own recording under exactly the same name.\n"
              "3. Click 'Import Whole Folder' here.\n\n"
              "Instructions are in _Instructions.txt in the folder. "
              "The folder is now opening.",
    },
    "tab_builder.template_failed_title": {
        "de": "Vorlagenordner fehlgeschlagen",
        "en": "Template Folder Failed",
    },
    "tab_builder.clear_confirm_title": {
        "de": "Wirklich löschen?",
        "en": "Really Delete?",
    },
    "tab_builder.clear_confirm_body": {
        "de": "Alle Zuweisungen werden entfernt. Deine Audiodateien selbst "
              "bleiben natürlich erhalten.",
        "en": "All assignments will be removed. Your audio files "
              "themselves are of course kept.",
    },
})
