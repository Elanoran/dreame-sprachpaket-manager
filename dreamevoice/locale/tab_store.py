"""German/English strings for dreamevoice/ui/tab_store.py."""

from __future__ import annotations

from ..i18n import register

register({
    # --- module-level choice constants (used inside _on_import_ready) --
    "tab_store.choice_archive": {
        "de": "ZIP-Datei oder fertiges Paket (.tar.gz)",
        "en": "ZIP file or ready-made pack (.tar.gz)",
    },
    "tab_store.choice_folder": {
        "de": "Ordner mit mp3-, wav- oder ogg-Dateien",
        "en": "Folder with mp3, wav, or ogg files",
    },
    "tab_store.choice_save_alongside": {
        "de": "Daneben speichern - das vorhandene bleibt",
        "en": "Save alongside - the existing one stays",
    },
    "tab_store.choice_replace_existing": {
        "de": "Das vorhandene ersetzen",
        "en": "Replace the existing one",
    },

    # --- PackCard ---------------------------------------------------
    "tab_store.pack_card_meta": {
        "de": "{language}  ·  ca. {count} Ansagen",
        "en": "{language}  ·  approx. {count} announcements",
    },
    "tab_store.pack_card_source": {
        "de": "Quelle: {author}  ·  Lizenz: {license}",
        "en": "Source: {author}  ·  License: {license}",
    },
    "tab_store.download_and_adapt_button": {
        "de": "Herunterladen und anpassen",
        "en": "Download and Adapt",
    },
    "tab_store.view_project_page_button": {
        "de": "Projektseite ansehen",
        "en": "View Project Page",
    },

    # --- _build -------------------------------------------------------
    "tab_store.store_disclaimer": {
        "de": ("Ehrlich gesagt: einen richtigen Store gibt es nicht. Was hier steht, "
               "sind die wenigen frei verfügbaren Bastelprojekte, die tatsächlich "
               "existieren und deren Dateien geprüft wurden. Jedes Paket wird beim "
               "Herunterladen gegen seine Prüfsumme geprüft und anschließend auf "
               "das offizielle Paket deines Modells gelegt - alles, was das "
               "Fremdpaket nicht abdeckt, bleibt auf der deutschen Originalstimme."),
        "en": ("Honestly: there's no real store. What's here are the few "
               "freely available fan projects that actually exist and whose "
               "files have been checked. Every pack is verified against its "
               "checksum on download and then laid over your model's "
               "official pack - anything the third-party pack doesn't cover "
               "stays on the German original voice."),
    },
    "tab_store.available_packs_heading": {
        "de": "Verfügbare Pakete",
        "en": "Available Packs",
    },
    "tab_store.status_ready": {
        "de": "Bereit",
        "en": "Ready",
    },

    # --- _build_dialect_card -------------------------------------------
    "tab_store.dialect_card_title": {
        "de": "Selbst erzeugen: Dialektpakete",
        "en": "Generate Your Own: Dialect Packs",
    },
    "tab_store.dialect_card_subtitle": {
        "de": "{count} Dialekte, {span} Ansagen - fertig herunterladen kann man die nirgends.",
        "en": "{count} dialects, {span} announcements - nowhere can you download these ready-made.",
    },
    "tab_store.dialect_intro": {
        "de": ("Dialektpakete gibt es für keinen Saugroboter zum Herunterladen - "
               "weder für Dreame noch für Roborock, Xiaomi oder Valetudo. In den "
               "Foren wurden sie oft gewünscht, gebaut hat sie niemand; vorhanden "
               "ist einzig ein Schweizerdeutsch-Paket für den Roborock S5. Es gibt "
               "also kein Fremdpaket zum Umbauen.\n\n"
               "Diese App schreibt die Ansagen deshalb selbst im jeweiligen "
               "Dialekt und lässt sie sprechen. Mit der Windows-Stimme läuft das "
               "offline und kostenlos; für echten Dialekt in der Aussprache lässt "
               "sich auf ElevenLabs umschalten."),
        "en": ("Dialect packs don't exist for any vacuum robot to "
               "download - not for Dreame, Roborock, Xiaomi, or "
               "Valetudo. They've often been requested in forums, but "
               "nobody's built them; the only one out there is a Swiss "
               "German pack for the Roborock S5. So there's no "
               "third-party pack to adapt.\n\n"
               "This app therefore writes the announcements itself in "
               "each dialect and has them spoken. With the Windows "
               "voice this runs offline and free; for genuine dialect "
               "in the pronunciation, you can switch to ElevenLabs."),
    },
    "tab_store.dialect_label": {
        "de": "Dialekt",
        "en": "Dialect",
    },
    "tab_store.create_pack_button": {
        "de": "Eigenes Paket anlegen ...",
        "en": "Create Custom Pack ...",
    },
    "tab_store.rename_button": {
        "de": "Umbenennen",
        "en": "Rename",
    },
    "tab_store.delete_button": {
        "de": "Löschen",
        "en": "Delete",
    },
    "tab_store.import_recordings_button": {
        "de": "Aufnahmen einlesen ...",
        "en": "Import Recordings ...",
    },
    "tab_store.custom_pack_intro": {
        "de": ("Unter 'Eigenes Paket anlegen' entsteht eine eigene "
               "Textsammlung - etwa im Stil einer Filmfigur. Sie "
               "verhält sich wie ein Dialekt: anhören, Texte ändern, "
               "mit jeder Stimme erzeugen, nach aufgebrauchtem "
               "Kontingent fortsetzen. 'Aufnahmen einlesen' nimmt "
               "fertig gesprochene Ansagen entgegen: eine "
               "ZIP-Datei von der Projektseite, ein fertiges "
               ".tar.gz oder einen Ordner voller mp3- und "
               "wav-Dateien."),
        "en": ("'Create Custom Pack' creates your own text "
               "collection - say, in the style of a movie "
               "character. It behaves like a dialect: preview, "
               "edit texts, generate with any voice, resume after "
               "the quota runs out. 'Import Recordings' takes "
               "already-spoken announcements: a ZIP file from the "
               "project page, a ready-made .tar.gz, or a folder "
               "full of mp3 and wav files."),
    },
    "tab_store.discard_progress_button": {
        "de": "Zwischenstand verwerfen",
        "en": "Discard Progress",
    },
    "tab_store.listen_sample_button": {
        "de": "Kostprobe anhören",
        "en": "Listen to Sample",
    },
    "tab_store.view_edit_texts_button": {
        "de": "Texte ansehen und ändern",
        "en": "View and Edit Texts",
    },
    "tab_store.generate_pack_button": {
        "de": "Paket erzeugen",
        "en": "Generate Pack",
    },
    "tab_store.cancel_button": {
        "de": "Abbrechen",
        "en": "Cancel",
    },
    "tab_store.export_texts_button": {
        "de": "Texte als Dateien ausgeben",
        "en": "Export Texts as Files",
    },
    "tab_store.import_texts_button": {
        "de": "Texte aus Datei einlesen",
        "en": "Import Texts from File",
    },
    "tab_store.open_folder_button": {
        "de": "Ordner öffnen",
        "en": "Open Folder",
    },
    "tab_store.sample_texts_info": {
        "de": ("Die Kostprobe spricht drei Sätze mit der gerade gewählten "
               "Stimme und spielt sie ab - so hörst du vorher, ob dir das "
               "Ergebnis gefällt. Bei ElevenLabs kostet sie rund 60 Zeichen "
               "aus dem Monatskontingent.\n"
               "Unter 'Texte ansehen und ändern' kannst du jede Ansage "
               "umformulieren. Deine Fassung bleibt gespeichert; bereits "
               "gesprochene Aufnahmen geänderter Ansagen werden verworfen "
               "und beim nächsten Erzeugen neu aufgenommen.\n"
               "Für größere Überarbeitungen liegt jeder Dialekt auch als "
               "Textdatei im Datenordner: kopieren, von einer Sprach-KI "
               "verbessern lassen, zurück in die Datei einfügen und wieder "
               "einlesen."),
        "en": ("The sample speaks three sentences with the "
               "currently chosen voice and plays them - so you "
               "can hear beforehand whether you like the result. "
               "With ElevenLabs it costs about 60 characters from "
               "the monthly quota.\n"
               "Under 'View and Edit Texts' you can reword any "
               "announcement. Your version stays saved; already-"
               "spoken recordings of changed announcements are "
               "discarded and re-recorded the next time you "
               "generate.\n"
               "For bigger rewrites, every dialect is also "
               "available as a text file in the data folder: "
               "copy it, have a language AI improve it, paste "
               "the result back in, and read it in again."),
    },
    "tab_store.voice_cloning_legal_notice": {
        "de": ("Die Stimme einer real existierenden Person nachzubilden - etwa "
               "aus YouTube-Aufnahmen oder fremden Sprachpaketen - ist rechtlich "
               "heikel (Persönlichkeitsrecht, bei Schauspielern kommen "
               "Verwertungsrechte dazu). Dafür bietet diese App bewusst keine "
               "Funktion an."),
        "en": ("Recreating the voice of a real living person - say, "
               "from YouTube recordings or other voice packs - is "
               "legally sensitive (personality rights, and for actors "
               "there's also exploitation rights). This app "
               "deliberately offers no feature for that."),
    },

    # --- selection list prefixes ---------------------------------------
    "tab_store.prefix_dialect": {
        "de": "Dialekt · ",
        "en": "Dialect · ",
    },
    "tab_store.prefix_custom": {
        "de": "Eigenes · ",
        "en": "Custom · ",
    },

    # --- _on_dialect_changed --------------------------------------------
    "tab_store.dialect_meta": {
        "de": "{count} Ansagen  ·  Kennung {lang_id}",
        "en": "{count} announcements  ·  identifier {lang_id}",
    },
    "tab_store.dialect_meta_custom_edited": {
        "de": "  ·  {count} selbst geändert",
        "en": "  ·  {count} custom edited",
    },
    "tab_store.sample_prefix": {
        "de": "Kostprobe:\n",
        "en": "Sample:\n",
    },

    # --- refresh_progress -------------------------------------------
    "tab_store.progress_nothing_yet": {
        "de": "Zwischenstand: noch nichts gesprochen.",
        "en": "Progress: nothing spoken yet.",
    },
    "tab_store.progress_summary": {
        "de": "Zwischenstand: {done} von {total} Ansagen gesprochen",
        "en": "Progress: {done} of {total} announcements spoken",
    },
    "tab_store.progress_taken_over": {
        "de": "davon {count} aus vorhandenen Dateien übernommen",
        "en": "of which {count} taken over from existing files",
    },
    "tab_store.progress_outdated": {
        "de": "{count} gehören zu geändertem Text und werden erneuert",
        "en": "{count} belong to changed text and will be redone",
    },
    "tab_store.progress_remaining": {
        "de": "{count} offen - 'Paket erzeugen' macht dort weiter",
        "en": "{count} remaining - 'Generate Pack' continues from there",
    },
    "tab_store.progress_complete": {
        "de": "alles vorhanden, das Erzeugen kostet nichts mehr",
        "en": "everything's there, generating costs nothing more",
    },

    # --- _on_discard_progress --------------------------------------------
    "tab_store.discard_progress_confirm_title": {
        "de": "Zwischenstand verwerfen",
        "en": "Discard Progress",
    },
    "tab_store.discard_progress_confirm_message": {
        "de": ("{count} bereits gesprochene Ansagen werden gelöscht.\n\n"
               "Beim nächsten Erzeugen wird alles neu gesprochen - bei "
               "ElevenLabs kostet das erneut Kontingent.\n\nWirklich löschen?"),
        "en": ("{count} already-spoken announcements will be deleted.\n\n"
               "Everything will be re-spoken next time you generate - "
               "with ElevenLabs that costs quota again.\n\nReally delete?"),
    },
    "tab_store.progress_discarded_log": {
        "de": "Zwischenstand verworfen ({count} Aufnahmen).",
        "en": "Progress discarded ({count} recordings).",
    },

    # --- _on_new_custom -------------------------------------------------
    "tab_store.new_custom_title": {
        "de": "Eigenes Sprachpaket",
        "en": "Custom Voice Pack",
    },
    "tab_store.new_custom_prompt": {
        "de": ("Wie soll das Paket heißen?\n\n"
               "Zum Beispiel 'Bruce Willis', 'Pirat' oder 'Butler'. Der Name "
               "steht nur in dieser App - der Roboter bekommt daraus eine kurze "
               "Kennung."),
        "en": ("What should the pack be called?\n\n"
               "For example 'Bruce Willis', 'Pirate', or 'Butler'. The name "
               "only appears in this app - the robot gets a short identifier "
               "derived from it."),
    },
    "tab_store.copy_of_template": {
        "de": "Kopie von {name}",
        "en": "Copy of {name}",
    },
    "tab_store.start_empty_option": {
        "de": "Leer anfangen",
        "en": "Start Empty",
    },
    "tab_store.start_with_what_title": {
        "de": "Womit anfangen?",
        "en": "Start with What?",
    },
    "tab_store.start_with_what_prompt": {
        "de": ("Ein Paket braucht für jede Ansage einen Text.\n\n"
               "Am einfachsten kopierst du einen vorhandenen Dialekt: dann "
               "stehen alle Ansagen schon da und du schreibst sie um. Neben "
               "jeder Zeile steht, was sie bedeuten muss.\n\n"
               "Leer anfangen lohnt nur, wenn du bloß einzelne Ansagen "
               "austauschen willst - der Rest bleibt dann auf der deutschen "
               "Originalstimme."),
        "en": ("A pack needs a text for every announcement.\n\n"
               "The easiest way is to copy an existing dialect: then every "
               "announcement is already there and you just reword it. Next "
               "to each line is what it needs to mean.\n\n"
               "Starting empty is only worth it if you just want to replace "
               "a few individual announcements - the rest then stays on the "
               "German original voice."),
    },
    "tab_store.custom_not_saved_title": {
        "de": "Nicht gespeichert",
        "en": "Not Saved",
    },
    "tab_store.custom_pack_not_created_message": {
        "de": "Das eigene Paket konnte nicht angelegt werden.",
        "en": "The custom pack couldn't be created.",
    },
    "tab_store.technical_details_new_custom": {
        "de": "Technische Details: {error}",
        "en": "Technical details: {error}",
    },
    "tab_store.custom_pack_created_log": {
        "de": "Eigenes Paket '{name}' angelegt ({count} Ansagen, Kennung {lang_id}).",
        "en": "Custom pack '{name}' created ({count} announcements, identifier {lang_id}).",
    },
    "tab_store.pack_created_title": {
        "de": "Paket angelegt",
        "en": "Pack Created",
    },
    "tab_store.pack_created_message": {
        "de": "'{name}' steht jetzt in der Auswahl.",
        "en": "'{name}' is now in the selection.",
    },
    "tab_store.pack_created_hint": {
        "de": ("{count} Ansagen als Vorlage, Kennung {lang_id}.\n\n"
               "Mit 'Texte ansehen und ändern' schreibst du sie um - oder du "
               "gibst die Datei\n{filename}\naus dem Ordner "
               "'{folder}' einer Sprach-KI. Danach wie gewohnt auf "
               "'Paket erzeugen'."),
        "en": ("{count} announcements as a template, identifier {lang_id}.\n\n"
               "Use 'View and Edit Texts' to rewrite them - or hand the file\n"
               "{filename}\nfrom the '{folder}' "
               "folder to a language AI. Then click 'Generate Pack' as usual."),
    },

    # --- _on_rename_custom / _on_delete_custom ---------------------------
    "tab_store.no_custom_pack_title": {
        "de": "Kein eigenes Paket",
        "en": "No Custom Pack",
    },
    "tab_store.no_custom_pack_rename_message": {
        "de": "Mitgelieferte Dialekte lassen sich nicht umbenennen.",
        "en": "Built-in dialects can't be renamed.",
    },
    "tab_store.no_custom_pack_hint": {
        "de": "Wähle oben ein Paket aus, das mit 'Eigenes' beginnt.",
        "en": "Choose a pack above that starts with 'Custom'.",
    },
    "tab_store.rename_dialog_title": {
        "de": "Umbenennen",
        "en": "Rename",
    },
    "tab_store.rename_dialog_prompt": {
        "de": "Neuer Name:",
        "en": "New name:",
    },
    "tab_store.rename_not_saved_title": {
        "de": "Nicht gespeichert",
        "en": "Not Saved",
    },
    "tab_store.renamed_log": {
        "de": "Umbenannt in '{name}'.",
        "en": "Renamed to '{name}'.",
    },
    "tab_store.no_custom_pack_delete_message": {
        "de": "Mitgelieferte Dialekte lassen sich nicht löschen.",
        "en": "Built-in dialects can't be deleted.",
    },
    "tab_store.really_delete_title": {
        "de": "Wirklich löschen?",
        "en": "Really Delete?",
    },
    "tab_store.really_delete_message": {
        "de": ("'{name}' mit {count} Ansagen löschen?\n\n"
               "Bereits gesprochene Aufnahmen und fertig gebaute Pakete "
               "bleiben erhalten - nur die Textsammlung verschwindet."),
        "en": ("Delete '{name}' with {count} announcements?\n\n"
               "Already-spoken recordings and built packs are kept - "
               "only the text collection disappears."),
    },
    "tab_store.pack_deleted_log": {
        "de": "'{name}' gelöscht.",
        "en": "'{name}' deleted.",
    },

    # --- _on_import_ready -------------------------------------------------
    "tab_store.original_pack_missing_title": {
        "de": "Originalpaket fehlt",
        "en": "Original Pack Missing",
    },
    "tab_store.original_pack_missing_import_message": {
        "de": "Lade zuerst unter 'Einzelne Ansagen' das offizielle Sprachpaket deines Roboters herunter.",
        "en": "First download your robot's official voice pack under 'Individual Announcements'.",
    },
    "tab_store.original_pack_missing_import_hint": {
        "de": ("Jedes eigene Paket entsteht als Kopie davon - sonst fehlen "
               "dem Roboter alle Ansagen, die du nicht selbst lieferst."),
        "en": ("Every custom pack is built as a copy of it - otherwise "
               "the robot would be missing every announcement you didn't "
               "supply yourself."),
    },
    "tab_store.what_import_title": {
        "de": "Was soll eingelesen werden?",
        "en": "What Should Be Imported?",
    },
    "tab_store.what_import_prompt": {
        "de": ("Die Aufnahmen von der Projektseite sind ZIP-Dateien wie "
               "'Bayerisch-Aufnahmen.zip'. Nimm dafür die erste Zeile und wähle "
               "das ZIP direkt aus - entpacken musst du nichts.\n\n"
               "Beides landet als fertiges Paket in deiner Sammlung und steht "
               "danach unter 'Fertige Stimmen' zur Auswahl."),
        "en": ("The recordings from the project page are ZIP files like "
               "'Bayerisch-Aufnahmen.zip'. Use the first option for those and "
               "choose the ZIP directly - you don't need to unpack anything.\n\n"
               "Either way ends up as a finished pack in your collection and "
               "then shows up under 'Ready-Made Voices' for selection."),
    },
    "tab_store.choose_zip_title": {
        "de": "ZIP oder Paketdatei wählen",
        "en": "Choose a ZIP or Pack File",
    },
    "tab_store.filetype_recordings_packs": {
        "de": "Aufnahmen und Pakete",
        "en": "Recordings and packs",
    },
    "tab_store.filetype_all_files": {
        "de": "Alle Dateien",
        "en": "All files",
    },
    "tab_store.choose_folder_recordings_title": {
        "de": "Ordner mit den Aufnahmen wählen",
        "en": "Choose the Folder with the Recordings",
    },
    "tab_store.nothing_found_title": {
        "de": "Nichts gefunden",
        "en": "Nothing Found",
    },
    "tab_store.nothing_found_import_message": {
        "de": "In {name} steckt keine zuzuordnende Aufnahme.",
        "en": "{name} contains no assignable recording.",
    },
    "tab_store.nothing_found_import_hint": {
        "de": ("Die Dateien müssen die Ansage-Nummer im Namen tragen, also "
               "7.ogg, 7.wav oder 7.mp3. Ein passend benannter Vorlagenordner "
               "lässt sich unter 'Einzelne Ansagen' anlegen."),
        "en": ("Files need the announcement number in their name, so "
               "7.ogg, 7.wav, or 7.mp3. A correctly-named template folder "
               "can be created under 'Individual Announcements'."),
    },
    "tab_store.name_for_pack_title": {
        "de": "Name für dieses Paket",
        "en": "Name for This Pack",
    },
    "tab_store.name_for_pack_import_prompt": {
        "de": "{count} Ansagen gefunden.\n\nUnter welchem Namen soll das fertige Paket gespeichert werden?",
        "en": "{count} announcements found.\n\nWhat name should the finished pack be saved under?",
    },
    "tab_store.pack_exists_title": {
        "de": "Dieses Paket gibt es schon",
        "en": "This Pack Already Exists",
    },
    "tab_store.pack_exists_message": {
        "de": ("Vorhanden ist:\n{label}\n\n"
               "Ersetzen überschreibt es endgültig. Das neue Paket wird "
               "zuerst vollständig gebaut - schlägt das fehl, bleibt das "
               "vorhandene unangetastet."),
        "en": ("Existing:\n{label}\n\n"
               "Replacing overwrites it permanently. The new pack is "
               "built completely first - if that fails, the existing "
               "one stays untouched."),
    },
    "tab_store.replacing_log": {
        "de": "Ersetze {name}.",
        "en": "Replacing {name}.",
    },
    "tab_store.building_pack_log": {
        "de": "Baue Paket aus {count} Aufnahmen ...",
        "en": "Building pack from {count} recordings ...",
    },
    "tab_store.converting_building_badge": {
        "de": "Wandle um und baue ...",
        "en": "Converting and building ...",
    },
    "tab_store.engine_custom_recordings": {
        "de": "Eigene Aufnahmen",
        "en": "Custom Recordings",
    },
    "tab_store.import_done_badge": {
        "de": "Fertig - {count} Ansagen",
        "en": "Done - {count} announcements",
    },
    "tab_store.pack_ready_title": {
        "de": "Paket ist fertig",
        "en": "Pack Is Ready",
    },
    "tab_store.pack_ready_message": {
        "de": "{count} Ansagen übernommen.",
        "en": "{count} announcements taken over.",
    },
    "tab_store.pack_ready_hint": {
        "de": "Gespeichert als:\n{filename}\n\nUnter 'Fertige Stimmen' wählst du es zum Installieren aus.",
        "en": "Saved as:\n{filename}\n\nChoose it for install under 'Ready-Made Voices'.",
    },
    "tab_store.import_failed_badge": {
        "de": "Fehlgeschlagen",
        "en": "Failed",
    },
    "tab_store.pack_not_built_title": {
        "de": "Paket nicht gebaut",
        "en": "Pack Not Built",
    },
    "tab_store.import_failed_title": {
        "de": "Einlesen fehlgeschlagen",
        "en": "Import Failed",
    },

    # --- _ask_choice ------------------------------------------------
    "tab_store.ask_choice_apply_button": {
        "de": "Übernehmen",
        "en": "Apply",
    },
    "tab_store.ask_choice_cancel_button": {
        "de": "Abbrechen",
        "en": "Cancel",
    },

    # --- _on_export_texts / _on_open_text_folder ------------------------
    "tab_store.files_not_written_title": {
        "de": "Dateien nicht geschrieben",
        "en": "Files Not Written",
    },
    "tab_store.text_files_not_created_message": {
        "de": "Die Textdateien konnten nicht angelegt werden.",
        "en": "The text files couldn't be created.",
    },
    "tab_store.technical_details_export": {
        "de": "Technische Details: {error}",
        "en": "Technical details: {error}",
    },
    "tab_store.dialect_files_written_log": {
        "de": "{count} Dialekt-Textdateien geschrieben.",
        "en": "{count} dialect text files written.",
    },
    "tab_store.text_files_created_title": {
        "de": "Textdateien angelegt",
        "en": "Text Files Created",
    },
    "tab_store.text_files_created_message": {
        "de": "{count} Dateien liegen jetzt in:\n{folder}",
        "en": "{count} files are now in:\n{folder}",
    },
    "tab_store.text_files_created_hint": {
        "de": ("Eine Datei komplett kopieren, von einer Sprach-KI überarbeiten "
               "lassen, das Ergebnis wieder einfügen und speichern. Danach hier "
               "auf 'Texte aus Datei einlesen' klicken.\n\n"
               "Achtung: vorhandene Dateien wurden mit dem aktuellen Stand "
               "überschrieben."),
        "en": ("Copy a whole file, have a language AI rework it, paste the "
               "result back in and save. Then click 'Import Texts from File' "
               "here.\n\n"
               "Note: existing files were overwritten with the current state."),
    },
    "tab_store.folder_not_opened_title": {
        "de": "Ordner nicht geöffnet",
        "en": "Folder Not Opened",
    },
    "tab_store.folder_here_hint": {
        "de": "Der Ordner liegt hier:\n{folder}",
        "en": "The folder is here:\n{folder}",
    },

    # --- _on_import_texts -------------------------------------------------
    "tab_store.import_revised_texts_title": {
        "de": "Überarbeitete Dialekttexte einlesen",
        "en": "Import Revised Dialect Texts",
    },
    "tab_store.filetype_text_files": {
        "de": "Textdateien",
        "en": "Text files",
    },
    "tab_store.pack_not_recognized_title": {
        "de": "Paket nicht erkannt",
        "en": "Pack Not Recognized",
    },
    "tab_store.pack_not_recognized_message": {
        "de": "Zu '{name}' gibt es kein passendes Paket.",
        "en": "There's no matching pack for '{name}'.",
    },
    "tab_store.pack_not_recognized_hint": {
        "de": ("Die Datei muss so heißen wie das Paket, also zum Beispiel "
               "'wienerisch.txt'. Benenne sie um und versuche es erneut."),
        "en": ("The file must be named like the pack, e.g. "
               "'wienerisch.txt'. Rename it and try again."),
    },
    "tab_store.file_not_readable_title": {
        "de": "Datei nicht lesbar",
        "en": "File Not Readable",
    },
    "tab_store.file_not_readable_message": {
        "de": "{name} konnte nicht gelesen werden.",
        "en": "{name} couldn't be read.",
    },
    "tab_store.technical_details_import_texts": {
        "de": "Technische Details: {error}",
        "en": "Technical details: {error}",
    },
    "tab_store.nothing_found_lines_message": {
        "de": "In {name} steht keine einzige verwertbare Zeile.",
        "en": "{name} doesn't contain a single usable line.",
    },
    "tab_store.nothing_found_lines_hint": {
        "de": ("Jede Zeile braucht die Form\n"
               "  Nummer | Bedeutung | Dialekttext\n\n"
               "Hat die KI das Format geändert, gib ihr die Datei noch einmal "
               "mit dem Hinweis, den Aufbau der Zeilen beizubehalten."),
        "en": ("Every line needs the form\n"
               "  Number | Meaning | Dialect text\n\n"
               "If the AI changed the format, hand it the file again with "
               "a note to keep the line structure."),
    },
    "tab_store.unknown_numbers_hint": {
        "de": "{count} Nummern gibt es bei diesem Dialekt nicht und wurden übergangen: {list}",
        "en": "{count} numbers don't exist for this dialect and were skipped: {list}",
    },
    "tab_store.empty_lines_hint": {
        "de": "{count} Zeilen hatten keinen Text - diese Ansagen bleiben, wie sie waren.",
        "en": "{count} lines had no text - these announcements stay as they were.",
    },
    "tab_store.apply_texts_title": {
        "de": "Texte übernehmen?",
        "en": "Apply Texts?",
    },
    "tab_store.apply_texts_question": {
        "de": "Sollen diese Texte für {name} übernommen werden?",
        "en": "Apply these texts for {name}?",
    },
    "tab_store.texts_taken_over_log": {
        "de": "{name}: {count} Texte aus {filename} übernommen.",
        "en": "{name}: {count} texts taken over from {filename}.",
    },
    "tab_store.discarded_recordings_note": {
        "de": ("\n\n{count} bereits gesprochene Aufnahmen wurden verworfen, "
               "damit sie mit dem neuen Text neu entstehen. Alle übrigen "
               "bleiben liegen und kosten kein Kontingent."),
        "en": ("\n\n{count} already-spoken recordings were discarded so "
               "they're re-created with the new text. All the rest stay "
               "and cost no quota."),
    },
    "tab_store.texts_applied_title": {
        "de": "Texte übernommen",
        "en": "Texts Applied",
    },
    "tab_store.texts_applied_message": {
        "de": "{count} von {total} Ansagen weichen jetzt vom mitgelieferten Text ab.",
        "en": "{count} of {total} announcements now differ from the built-in text.",
    },
    "tab_store.changes_kept_note": {
        "de": "Die Änderungen bleiben erhalten, auch nach einem Neustart.",
        "en": "The changes are kept, even after a restart.",
    },

    # --- _on_show_texts -------------------------------------------------
    "tab_store.edit_texts_window_title": {
        "de": "{name} - {count} Ansagen bearbeiten",
        "en": "{name} - Edit {count} Announcements",
    },
    "tab_store.customize_pack_title": {
        "de": "{name} anpassen",
        "en": "Customize {name}",
    },
    "tab_store.customize_pack_subtitle": {
        "de": ("Ändere die Texte, wie du sie hören willst. Was du leer "
               "lässt, bleibt auf der deutschen Originalstimme."),
        "en": ("Change the texts to however you want to hear them. "
               "What you leave empty stays on the German original voice."),
    },
    "tab_store.search_label": {
        "de": "Suche",
        "en": "Search",
    },
    "tab_store.building_list_status": {
        "de": "Liste wird aufgebaut ...",
        "en": "Building the list ...",
    },
    "tab_store.edited_marker": {
        "de": "   ·  geändert",
        "en": "   ·  edited",
    },
    "tab_store.shown_count": {
        "de": "{shown} von {total} Ansagen",
        "en": "{shown} of {total} announcements",
    },
    "tab_store.discarded_recordings_note_own_text": {
        "de": "\n\n{count} bereits gesprochene Aufnahmen wurden verworfen, damit sie neu mit deinem Text entstehen.",
        "en": "\n\n{count} already-spoken recordings were discarded so they're re-created with your text.",
    },
    "tab_store.texts_saved_title": {
        "de": "Texte gespeichert",
        "en": "Texts Saved",
    },
    "tab_store.texts_saved_message": {
        "de": "{count} von {total} Ansagen weichen jetzt vom mitgelieferten Text ab.",
        "en": "{count} of {total} announcements now differ from the built-in text.",
    },
    "tab_store.reset_confirm_title": {
        "de": "Zurücksetzen",
        "en": "Reset",
    },
    "tab_store.reset_confirm_message": {
        "de": "Alle eigenen Änderungen an {name} verwerfen und die mitgelieferten Texte wiederherstellen?",
        "en": "Discard all custom changes to {name} and restore the built-in texts?",
    },
    "tab_store.save_button": {
        "de": "Speichern",
        "en": "Save",
    },
    "tab_store.reset_to_default_button": {
        "de": "Auf Standard zurücksetzen",
        "en": "Reset to Default",
    },
    "tab_store.text_editor_cancel_button": {
        "de": "Abbrechen",
        "en": "Cancel",
    },

    # --- _speak_text ------------------------------------------------
    "tab_store.no_text_title": {
        "de": "Kein Text",
        "en": "No Text",
    },
    "tab_store.no_text_message": {
        "de": "In dieser Zeile steht nichts zum Vorlesen.",
        "en": "This line has nothing to read out.",
    },
    "tab_store.connect_first_title": {
        "de": "Erst verbinden",
        "en": "Connect First",
    },
    "tab_store.connect_first_message": {
        "de": "Für ElevenLabs brauchst du Schlüssel und Stimme.",
        "en": "ElevenLabs needs a key and a voice.",
    },
    "tab_store.connect_first_hint": {
        "de": "Ohne beides kann der Satz nicht gesprochen werden. Mit der Windows-Stimme geht es sofort.",
        "en": "The sentence can't be spoken without both. With the Windows voice it works right away.",
    },
    "tab_store.no_german_voice_title": {
        "de": "Keine deutsche Stimme",
        "en": "No German Voice",
    },
    "tab_store.no_german_voice_message": {
        "de": "Es ist keine deutsche Sprachausgabe installiert.",
        "en": "No German text-to-speech voice is installed.",
    },
    "tab_store.playback_not_possible_title": {
        "de": "Wiedergabe nicht möglich",
        "en": "Playback Not Possible",
    },
    "tab_store.recording_here_hint": {
        "de": "Die Aufnahme liegt hier:\n{path}",
        "en": "The recording is here:\n{path}",
    },
    "tab_store.reading_aloud_failed_title": {
        "de": "Vorlesen fehlgeschlagen",
        "en": "Reading Aloud Failed",
    },

    # --- _on_preview_dialect ---------------------------------------------
    "tab_store.connect_first_preview_message": {
        "de": ("Trage deinen ElevenLabs-Schlüssel ein, klicke auf "
               "'Verbinden und Stimmen laden' und wähle eine Stimme aus. "
               "Danach kannst du sie hier anhören."),
        "en": ("Enter your ElevenLabs key, click 'Connect and Load "
               "Voices', and choose a voice. Then you can preview it "
               "here."),
    },
    "tab_store.speaking_sample_badge": {
        "de": "Spreche die Kostprobe ...",
        "en": "Speaking the sample ...",
    },
    "tab_store.sample_ready_badge": {
        "de": "Kostprobe fertig - {count} Sätze",
        "en": "Sample Ready - {count} Sentences",
    },
    "tab_store.playing_log": {
        "de": "Spiele ab ...",
        "en": "Playing ...",
    },
    "tab_store.couldnt_play_log": {
        "de": "Konnte {filename} nicht abspielen: {error}",
        "en": "Couldn't play {filename}: {error}",
    },
    "tab_store.sample_failed_badge": {
        "de": "Kostprobe fehlgeschlagen",
        "en": "Sample Failed",
    },
    "tab_store.sample_failed_title": {
        "de": "Kostprobe fehlgeschlagen",
        "en": "Sample Failed",
    },

    # --- _build_engine_chooser -------------------------------------------
    "tab_store.who_speaks_heading": {
        "de": "Wer spricht?",
        "en": "Who Speaks?",
    },
    "tab_store.windows_tts_radio": {
        "de": "Windows-Sprachausgabe",
        "en": "Windows Text-to-Speech",
    },
    "tab_store.windows_voice_info": {
        "de": ("   Offline, kostenlos, sofort einsatzbereit - aber hochdeutsche "
               "Aussprache. Der Dialekt steckt nur in den Worten. Stefan ist "
               "die einzige männliche deutsche Stimme; System.Speech kennt sie "
               "nicht, die App holt sie über die Windows-Runtime."),
        "en": ("   Offline, free, ready to use right away - but standard "
               "German pronunciation. The dialect only lives in the "
               "wording. Stefan is the only male German voice; System.Speech doesn't "
               "know it, the app fetches it via the Windows Runtime."),
    },
    "tab_store.rate_label": {
        "de": "   Tempo",
        "en": "   Rate",
    },
    "tab_store.pitch_label": {
        "de": "   Tonhöhe",
        "en": "   Pitch",
    },
    "tab_store.reset_button": {
        "de": "Zurücksetzen",
        "en": "Reset",
    },
    "tab_store.elevenlabs_radio": {
        "de": "ElevenLabs - echte Dialektaussprache",
        "en": "ElevenLabs - genuine dialect pronunciation",
    },
    "tab_store.elevenlabs_info": {
        "de": ("   Ein frei verfügbares Dialekt-Sprachmodell gibt es nicht - "
               "geprüft: Piper hat nur Hochdeutsch, Thorsten-Voice nur Hessisch, "
               "und der einzige bayerische Sprachkorpus gehört dem Bayerischen "
               "Rundfunk. ElevenLabs bietet Dialekte dagegen ausdrücklich an, "
               "mit 10.000 Freizeichen im Monat. Ein Dialektpaket braucht ab "
               "{needed} Zeichen; volle Abdeckung eher das Doppelte. Geht das "
               "Kontingent aus, macht die App beim nächsten Mal dort weiter.\n"
               "   Du brauchst ein eigenes (kostenloses) Konto. Die App legt "
               "keins an. Übertragen werden nur die Ansagetexte."),
        "en": ("   No freely available dialect speech model exists - "
               "checked: Piper only has standard German, Thorsten-Voice "
               "only Hessian, and the only Bavarian speech corpus "
               "belongs to Bayerischer Rundfunk. ElevenLabs, on the "
               "other hand, explicitly offers dialects, with 10,000 "
               "free characters a month. A dialect pack needs at "
               "least {needed} characters; full coverage more like "
               "double that. If the quota runs out, the app picks up "
               "there next time.\n"
               "   You need your own (free) account. The app doesn't "
               "create one. Only the announcement texts are transmitted."),
    },
    "tab_store.access_key_label": {
        "de": "   Zugangsschlüssel",
        "en": "   Access Key",
    },
    "tab_store.connect_load_voices_button": {
        "de": "Verbinden und Stimmen laden",
        "en": "Connect and Load Voices",
    },
    "tab_store.get_key_button": {
        "de": "Schlüssel holen",
        "en": "Get a Key",
    },
    "tab_store.forget_key_button": {
        "de": "Schlüssel vergessen",
        "en": "Forget Key",
    },
    "tab_store.voice_label": {
        "de": "   Stimme",
        "en": "   Voice",
    },
    "tab_store.search_voice_library_button": {
        "de": "Stimmen-Bibliothek durchsuchen",
        "en": "Search Voice Library",
    },
    "tab_store.custom_voice_id_label": {
        "de": "   Eigene Stimmen-ID",
        "en": "   Custom Voice ID",
    },
    "tab_store.add_id_apply_button": {
        "de": "Übernehmen",
        "en": "Apply",
    },
    "tab_store.copy_voice_id_hint": {
        "de": "(in ElevenLabs: drei Punkte an der Stimme > Copy Voice ID)",
        "en": "(in ElevenLabs: three dots on the voice > Copy Voice ID)",
    },
    "tab_store.model_label": {
        "de": "   Modell",
        "en": "   Model",
    },
    "tab_store.default_model_label": {
        "de": "Standard ({model})",
        "en": "Default ({model})",
    },
    "tab_store.use_voice_settings_checkbox": {
        "de": "Klang der Stimme übernehmen",
        "en": "Use the voice's own sound",
    },
    "tab_store.liveliness_label": {
        "de": "   Lebendigkeit",
        "en": "   Liveliness",
    },
    "tab_store.expression_label": {
        "de": "   Ausdruck",
        "en": "   Expression",
    },
    "tab_store.voice_settings_info": {
        "de": ("   'Klang der Stimme übernehmen' benutzt genau die "
               "Einstellungen, die du in ElevenLabs an der Stimme "
               "hinterlegt hast - so klingt sie wie dort in der Vorschau. "
               "Ohne den Haken kannst du selbst regeln: weniger Stabilität "
               "heißt mehr Schwung, mehr Stabilität heißt gleichförmiger."),
        "en": ("   'Use the voice's own sound' uses exactly the "
               "settings you've set on the voice in ElevenLabs - so it "
               "sounds like the preview there. Without the checkbox you "
               "control it yourself: lower stability means more life, "
               "higher stability means more uniform."),
    },
    "tab_store.rate_slower": {
        "de": "langsamer",
        "en": "slower",
    },
    "tab_store.rate_faster": {
        "de": "schneller",
        "en": "faster",
    },
    "tab_store.pitch_lower": {
        "de": "tiefer",
        "en": "lower",
    },
    "tab_store.pitch_higher": {
        "de": "höher",
        "en": "higher",
    },
    "tab_store.liveliness_very_lively": {
        "de": "sehr lebendig",
        "en": "very lively",
    },
    "tab_store.liveliness_lively": {
        "de": "lebendig",
        "en": "lively",
    },
    "tab_store.liveliness_balanced": {
        "de": "ausgewogen",
        "en": "balanced",
    },
    "tab_store.liveliness_uniform": {
        "de": "gleichförmig",
        "en": "uniform",
    },

    # --- _refresh_voice_info ---------------------------------------------
    "tab_store.no_german_voice_full_message": {
        "de": ("   Es ist keine deutsche Sprachausgabe installiert. "
               "Windows-Einstellungen > Zeit und Sprache > Sprache > "
               "Deutsch > Optionen > Sprachausgabe hinzufügen, danach die "
               "App neu starten."),
        "en": ("   No German text-to-speech voice is installed. "
               "Windows Settings > Time and Language > Language > "
               "German > Options > Add speech, then restart the app."),
    },

    # --- _refresh_key_location / _on_forget_key / _open_api_key_page -----
    "tab_store.key_location_credential_manager": {
        "de": ("   Schlüssel liegt im Windows-Anmeldeinformationsspeicher - "
               "einsehbar unter Systemsteuerung > "
               "Anmeldeinformationsverwaltung > Windows-Anmeldeinformationen "
               "> „DreameSprachpaket:ElevenLabs“. Die config.json enthält "
               "ihn nicht."),
        "en": ("   Key is stored in the Windows Credential Manager - "
               "viewable under Control Panel > Credential Manager > "
               "Windows Credentials > “DreameSprachpaket:ElevenLabs”. "
               "config.json doesn't contain it."),
    },
    "tab_store.key_location_config_json": {
        "de": ("   Schlüssel liegt verschlüsselt in der config.json "
               "(der Windows-Anmeldespeicher war nicht erreichbar)."),
        "en": ("   Key is stored encrypted in config.json "
               "(the Windows Credential Manager wasn't reachable)."),
    },
    "tab_store.key_location_none": {
        "de": "   Schlüssel ist nicht gespeichert.",
        "en": "   Key isn't saved.",
    },
    "tab_store.forget_key_confirm_title": {
        "de": "Schlüssel vergessen",
        "en": "Forget Key",
    },
    "tab_store.forget_key_confirm_message": {
        "de": ("Der gespeicherte ElevenLabs-Schlüssel wird entfernt - aus dem "
               "Windows-Anmeldespeicher und aus der config.json.\n\n"
               "Fortfahren?"),
        "en": ("The saved ElevenLabs key will be removed - from the "
               "Windows Credential Manager and from config.json.\n\n"
               "Continue?"),
    },
    "tab_store.key_removed_status": {
        "de": "   Schlüssel entfernt.",
        "en": "   Key removed.",
    },
    "tab_store.get_access_key_title": {
        "de": "Zugangsschlüssel holen",
        "en": "Get an Access Key",
    },
    "tab_store.get_access_key_message": {
        "de": ("Es öffnet sich die Seite, auf der ElevenLabs den Schlüssel erzeugt.\n\n"
               "Dort auf 'Create API Key' klicken. Der Schlüssel wird nur ein "
               "einziges Mal vollständig angezeigt - sofort kopieren und hier "
               "einfügen.\n\n"
               "Falls die Seite nicht direkt aufgeht: unten links auf dein Profil, "
               "dann Settings > API Keys.\n\n"
               "Im Free-Plan ist das enthalten (10.000 Zeichen pro Monat)."),
        "en": ("The page where ElevenLabs generates the key will open.\n\n"
               "Click 'Create API Key' there. The key is only shown in full "
               "once - copy it immediately and paste it here.\n\n"
               "If the page doesn't open directly: bottom left on your "
               "profile, then Settings > API Keys.\n\n"
               "This is included in the free plan (10,000 characters a month)."),
    },

    # --- _on_connect_elevenlabs ------------------------------------------
    "tab_store.access_key_missing_title": {
        "de": "Zugangsschlüssel fehlt",
        "en": "Access Key Missing",
    },
    "tab_store.access_key_missing_connect_message": {
        "de": "Lege dir ein kostenloses ElevenLabs-Konto an und kopiere den Zugangsschlüssel hier herein.",
        "en": "Create a free ElevenLabs account and paste the access key in here.",
    },
    "tab_store.access_key_missing_connect_hint": {
        "de": ("Zu finden unter elevenlabs.io/app/settings/api-keys > "
               "Create API Key. Die App legt kein Konto für dich an."),
        "en": ("Found under elevenlabs.io/app/settings/api-keys > "
               "Create API Key. The app doesn't create an account for you."),
    },
    "tab_store.key_unusual_title": {
        "de": "Schlüssel sieht ungewöhnlich aus",
        "en": "Key Looks Unusual",
    },
    "tab_store.key_unusual_connect_message": {
        "de": "Der eingetragene Zugangsschlüssel beginnt nicht mit 'sk_'.",
        "en": "The entered access key doesn't start with 'sk_'.",
    },
    "tab_store.key_unusual_connect_hint": {
        "de": ("Eingetragen ist etwas mit {count} Zeichen, das mit "
               "'{prefix}…' anfängt. Falls das eine Stimmen-ID ist: die "
               "gehört ins Feld darunter.\n\nDie Verbindung wird trotzdem "
               "versucht - vielleicht hat ElevenLabs das Format geändert."),
        "en": ("What's entered is {count} characters starting with "
               "'{prefix}…'. If this is a voice ID: that belongs in "
               "the field below.\n\nThe connection will be attempted "
               "anyway - maybe ElevenLabs changed the format."),
    },
    "tab_store.connecting_status": {
        "de": "Verbinde ...",
        "en": "Connecting ...",
    },
    "tab_store.quota_for_pack": {
        "de": "das Paket '{name}'",
        "en": "the pack '{name}'",
    },
    "tab_store.quota_for_generic_pack": {
        "de": "ein Paket",
        "en": "a pack",
    },
    "tab_store.quota_connected_status": {
        "de": "   Verbunden. Kontingent: {quota}. Für {target} werden rund {needed} Zeichen gebraucht - {enough}",
        "en": "   Connected. Quota: {quota}. {target} needs about {needed} characters - {enough}",
    },
    "tab_store.quota_enough": {
        "de": "das reicht.",
        "en": "that's enough.",
    },
    "tab_store.quota_not_enough": {
        "de": "das reicht derzeit nicht.",
        "en": "that's not enough right now.",
    },
    "tab_store.voices_in_account": {
        "de": "\n   {count} Stimmen im Konto",
        "en": "\n   {count} voices in the account",
    },
    "tab_store.voices_self_created": {
        "de": ", davon {count} selbst erzeugt (stehen oben)",
        "en": ", {count} of them self-created (listed above)",
    },
    "tab_store.no_bavarian_in_library": {
        "de": (". Keine davon ist als bayerisch ausgewiesen - die "
               "Bibliotheksstimmen taugen dafür erfahrungsgemäß wenig. "
               "Besser: in ElevenLabs mit Voice Design eine eigene "
               "bauen und ihre ID unten eintragen."),
        "en": (". None of them are labeled Bavarian - library "
               "voices tend to be poor at it. Better: build your "
               "own with Voice Design in ElevenLabs and enter "
               "its ID below."),
    },

    # --- _on_add_voice_id -------------------------------------------------
    "tab_store.access_key_missing_add_id_message": {
        "de": "Trage zuerst deinen ElevenLabs-Schlüssel ein.",
        "en": "First enter your ElevenLabs key.",
    },
    "tab_store.no_id_entered_title": {
        "de": "Keine ID eingetragen",
        "en": "No ID Entered",
    },
    "tab_store.no_id_entered_message": {
        "de": "Kopiere die ID deiner Stimme aus ElevenLabs hier herein.",
        "en": "Copy your voice's ID from ElevenLabs in here.",
    },
    "tab_store.no_id_entered_hint": {
        "de": ("Du findest sie in der Stimmenübersicht: die drei Punkte an der "
               "Stimme anklicken und 'Copy Voice ID' wählen. Sie ist rund "
               "20 Zeichen lang."),
        "en": ("You'll find it in the voice overview: click the three "
               "dots on the voice and choose 'Copy Voice ID'. It's about "
               "20 characters long."),
    },
    "tab_store.fields_swapped_title": {
        "de": "Felder vertauscht?",
        "en": "Fields Swapped?",
    },
    "tab_store.fields_swapped_message": {
        "de": "Im Feld für die Stimmen-ID steht ein Zugangsschlüssel.",
        "en": "The voice ID field has an access key in it.",
    },
    "tab_store.fields_swapped_hint": {
        "de": ("Schlüssel beginnen mit 'sk_', Stimmen-IDs nicht. Der "
               "Schlüssel gehört ins obere Feld, die Stimmen-ID hierher."),
        "en": ("Keys start with 'sk_', voice IDs don't. The key belongs "
               "in the field above, the voice ID here."),
    },
    "tab_store.key_unusual_addid_message": {
        "de": "Der eingetragene Zugangsschlüssel beginnt nicht mit 'sk_'.",
        "en": "The entered access key doesn't start with 'sk_'.",
    },
    "tab_store.key_unusual_addid_hint": {
        "de": ("Eingetragen ist etwas mit {count} Zeichen, das mit "
               "'{prefix}…' anfängt. Ein ElevenLabs-Schlüssel sieht so aus: "
               "sk_ gefolgt von rund 45 weiteren Zeichen.\n\n"
               "Neuen Schlüssel holen: elevenlabs.io/app/settings/api-keys "
               "> Create API Key. Er wird nur einmal vollständig angezeigt."),
        "en": ("What's entered is {count} characters starting with "
               "'{prefix}…'. An ElevenLabs key looks like this: "
               "sk_ followed by about 45 more characters.\n\n"
               "Get a new key: elevenlabs.io/app/settings/api-keys "
               "> Create API Key. It's only shown in full once."),
    },
    "tab_store.fetching_voice_status": {
        "de": "   Hole die Stimme ...",
        "en": "   Fetching the voice ...",
    },
    "tab_store.voice_selected_status": {
        "de": "   '{name}' ist ausgewählt. Hör sie dir mit 'Kostprobe anhören' an.",
        "en": "   '{name}' is selected. Preview it with 'Listen to Sample'.",
    },
    "tab_store.voice_not_found_title": {
        "de": "Stimme nicht gefunden",
        "en": "Voice Not Found",
    },

    # --- _on_search_bavarian -----------------------------------------------
    "tab_store.access_key_missing_search_message": {
        "de": "Trage zuerst deinen ElevenLabs-Schlüssel ein.",
        "en": "First enter your ElevenLabs key.",
    },
    "tab_store.searching_library_status": {
        "de": "   Durchsuche die Stimmenbibliothek ...",
        "en": "   Searching the voice library ...",
    },
    "tab_store.no_bavarian_found_status": {
        "de": ("   In der Bibliothek war gerade keine als bayerisch "
               "ausgewiesene Stimme zu finden. Am besten baust du dir "
               "in ElevenLabs selbst eine (Voice Design) und trägst "
               "ihre ID unten ein."),
        "en": ("   No voice labeled Bavarian was found in the "
               "library right now. Best to build your own in "
               "ElevenLabs (Voice Design) and enter its ID below."),
    },

    # --- _show_voice_chooser / _add_voice ---------------------------------
    "tab_store.choose_voice_window_title": {
        "de": "Stimme auswählen",
        "en": "Choose a Voice",
    },
    "tab_store.voices_found_title": {
        "de": "{count} Stimmen gefunden",
        "en": "{count} Voices Found",
    },
    "tab_store.voices_found_subtitle": {
        "de": ("Wähle die Stimme, die in dein ElevenLabs-Konto übernommen "
               "werden soll. Anhören kannst du sie danach mit 'Kostprobe'."),
        "en": ("Choose the voice to add to your ElevenLabs account. "
               "You can preview it afterward with 'Listen to Sample'."),
    },
    "tab_store.listen_on_elevenlabs_button": {
        "de": "bei ElevenLabs anhören",
        "en": "Listen on ElevenLabs",
    },
    "tab_store.add_selected_voice_button": {
        "de": "Ausgewählte Stimme übernehmen",
        "en": "Add Selected Voice",
    },
    "tab_store.voice_chooser_cancel_button": {
        "de": "Abbrechen",
        "en": "Cancel",
    },
    "tab_store.none_fit_hint": {
        "de": ("Keine passt? Bau dir in ElevenLabs mit Voice Design eine "
               "eigene und trage ihre ID im Feld unten ein."),
        "en": ("None of these fit? Build your own in ElevenLabs "
               "with Voice Design and enter its ID in the field "
               "below."),
    },
    "tab_store.voice_added_status": {
        "de": "   '{name}' ist jetzt in deinem Konto und ausgewählt.",
        "en": "   '{name}' is now in your account and selected.",
    },

    # --- generate_dialect --------------------------------------------------
    "tab_store.original_pack_missing_generate_message": {
        "de": ("Lade zuerst unter 'Einzelne Ansagen' das offizielle Sprachpaket deines Roboters "
               "herunter - es ist die Grundlage jedes Pakets."),
        "en": ("First download your robot's official voice pack under "
               "'Individual Announcements' - it's the foundation of every pack."),
    },
    "tab_store.access_key_missing_generate_message": {
        "de": "Trage deinen ElevenLabs-Schlüssel ein und klicke auf 'Verbinden und Stimmen laden'.",
        "en": "Enter your ElevenLabs key and click 'Connect and Load Voices'.",
    },
    "tab_store.no_voice_chosen_title": {
        "de": "Keine Stimme gewählt",
        "en": "No Voice Chosen",
    },
    "tab_store.no_voice_chosen_message": {
        "de": ("Klicke auf 'Verbinden und Stimmen laden' und wähle danach "
               "eine Stimme aus - am besten eine bayerische."),
        "en": ("Click 'Connect and Load Voices' and then choose a "
               "voice - preferably a Bavarian one."),
    },
    "tab_store.no_bavarian_voice_title": {
        "de": "Keine bayerische Stimme",
        "en": "No Bavarian Voice",
    },
    "tab_store.no_bavarian_voice_message": {
        "de": ("'{name}' ist nicht als bayerisch ausgewiesen. Das "
               "Ergebnis klingt dann nicht nach Dialekt.\n\nTrotzdem "
               "fortfahren?"),
        "en": ("'{name}' isn't labeled Bavarian. The result "
               "won't sound like the dialect then.\n\nContinue "
               "anyway?"),
    },
    "tab_store.no_german_voice_generate_message": {
        "de": ("Es ist keine deutsche Sprachausgabe installiert.\n\n"
               "Windows-Einstellungen > Zeit und Sprache > Sprache > Deutsch > "
               "Optionen > Sprachausgabe hinzufügen. Danach die App neu "
               "starten."),
        "en": ("No German text-to-speech voice is installed.\n\n"
               "Windows Settings > Time and Language > Language > "
               "German > Options > Add speech. Then restart the app."),
    },
    "tab_store.ffmpeg_missing_title": {
        "de": "ffmpeg fehlt",
        "en": "ffmpeg Missing",
    },
    "tab_store.ffmpeg_missing_message": {
        "de": ("Zum Umwandeln der gesprochenen Ansagen wird ffmpeg gebraucht.\n\n"
               "Wechsle kurz unter 'Einzelne Ansagen' - dort richtet die App es ein."),
        "en": ("ffmpeg is needed to convert the spoken announcements.\n\n"
               "Briefly switch to 'Individual Announcements' - the app "
               "sets it up there."),
    },
    "tab_store.question_already_spoken": {
        "de": "Bereits gesprochen: {done} von {total} Ansagen.\nNoch offen: {remaining} ({chars} Zeichen).\n\n",
        "en": "Already spoken: {done} of {total} announcements.\nStill open: {remaining} ({chars} characters).\n\n",
    },
    "tab_store.question_quota_free": {
        "de": "Dein Kontingent: {rest} Zeichen frei.\n",
        "en": "Your quota: {rest} characters free.\n",
    },
    "tab_store.question_not_enough": {
        "de": ("\nDAS REICHT NICHT FÜR ALLES: etwa {doable} der "
               "{remaining} offenen Ansagen sind machbar.\n\n"
               "Die App bricht deshalb nicht ab. Sie spricht so viel "
               "wie möglich, baut das Paket damit, und der Rest bleibt "
               "auf Hochdeutsch. Nächsten Monat einfach wieder auf "
               "'Paket erzeugen' klicken - dann macht sie genau hier "
               "weiter und spricht nur noch das Fehlende.\n"),
        "en": ("\nTHAT'S NOT ENOUGH FOR EVERYTHING: about {doable} of "
               "the {remaining} remaining announcements are "
               "doable.\n\n"
               "The app won't abort because of this. It speaks as "
               "much as possible, builds the pack with that, and "
               "the rest stays in standard German. Next month just "
               "click 'Generate Pack' again - it picks up exactly "
               "here and only speaks what's missing.\n"),
    },
    "tab_store.question_enough_for_all": {
        "de": "\nDas reicht für alles Offene.\n",
        "en": "\nThat's enough for everything remaining.\n",
    },
    "tab_store.question_privacy_continue": {
        "de": "\nÜbertragen werden nur die Ansagetexte, keine persönlichen Daten.\n\nFortfahren?",
        "en": "\nOnly the announcement texts are transmitted, no personal data.\n\nContinue?",
    },
    "tab_store.question_windows_intro": {
        "de": "Die App spricht jetzt {count} Ansagen auf {name} und baut daraus ein Sprachpaket.",
        "en": "The app will now speak {count} announcements for {name} and build a voice pack from them.",
    },
    "tab_store.question_already_spoken_skipped": {
        "de": "\n\n{count} sind schon gesprochen und werden übersprungen.",
        "en": "\n\n{count} are already spoken and will be skipped.",
    },
    "tab_store.question_windows_local_continue": {
        "de": ("\n\nDas dauert ein paar Minuten und passiert vollständig auf "
               "diesem PC - es wird nichts hochgeladen.\n\nFortfahren?"),
        "en": ("\n\nThis takes a few minutes and happens entirely on "
               "this PC - nothing gets uploaded.\n\nContinue?"),
    },
    "tab_store.generate_confirm_title": {
        "de": "{name} erzeugen?",
        "en": "Generate {name}?",
    },
    "tab_store.name_for_pack_generate_title": {
        "de": "Name für dieses Paket",
        "en": "Name for This Pack",
    },
    "tab_store.name_for_pack_generate_prompt": {
        "de": ("Unter welchem Namen soll das Paket gespeichert werden?\n\n"
               "Der Vorschlag enthält Dialekt und Stimme, damit mehrere "
               "Fassungen nebeneinander liegen können. Ein vorhandenes Paket "
               "wird nie überschrieben - notfalls hängt die App eine Zahl an."),
        "en": ("What name should the pack be saved under?\n\n"
               "The suggestion includes dialect and voice, so several "
               "versions can exist side by side. An existing pack is never "
               "overwritten - the app appends a number if needed."),
    },
    "tab_store.generating_dialect_log": {
        "de": "Erzeuge Dialektpaket: {name}",
        "en": "Generating dialect pack: {name}",
    },
    "tab_store.speaking_announcements_badge": {
        "de": "Spreche die Ansagen ...",
        "en": "Speaking the announcements ...",
    },
    "tab_store.engine_windows_tts": {
        "de": "Windows-Sprachausgabe",
        "en": "Windows Text-to-Speech",
    },
    "tab_store.generate_done_badge": {
        "de": "Fertig - {count} Ansagen auf {name}",
        "en": "Done - {count} announcements for {name}",
    },
    "tab_store.generate_missing_hint": {
        "de": ("\n\n{count} Ansagen fehlen noch - vermutlich war das "
               "ElevenLabs-Kontingent aufgebraucht. Das Gesprochene ist "
               "gespeichert: starte die Erzeugung im nächsten Monat einfach "
               "erneut, dann macht die App genau dort weiter."),
        "en": ("\n\n{count} announcements are still missing - the "
               "ElevenLabs quota was probably used up. What's spoken is "
               "saved: just start generating again next month, and the app "
               "picks up exactly there."),
    },
    "tab_store.generate_ready_title": {
        "de": "{name} ist fertig",
        "en": "{name} Is Ready",
    },
    "tab_store.generate_ready_message": {
        "de": ("{count} Ansagen sprechen jetzt {name}, der "
               "Rest bleibt auf Hochdeutsch.{hint}\n\n"
               "Gespeichert als:\n{filename}\n\n"
               "Frühere Pakete bleiben erhalten. Wechsle unter 'Fertige Stimmen' - dort "
               "wählst du aus, welches installiert wird."),
        "en": ("{count} announcements now speak {name}, "
               "the rest stays in standard German.{hint}\n\n"
               "Saved as:\n{filename}\n\n"
               "Earlier packs are kept. Switch to 'Ready-Made Voices' - "
               "there you choose which one gets installed."),
    },
    "tab_store.cancelled_badge": {
        "de": "Abgebrochen",
        "en": "Cancelled",
    },
    "tab_store.operation_cancelled_log": {
        "de": "Vorgang abgebrochen.",
        "en": "Operation cancelled.",
    },
    "tab_store.cancelled_title": {
        "de": "Abgebrochen",
        "en": "Cancelled",
    },
    "tab_store.no_pack_built_message": {
        "de": "Es wurde kein Paket gebaut.",
        "en": "No pack was built.",
    },
    "tab_store.cancelled_spoken_info": {
        "de": "{count} von {total} Ansagen sind gesprochen und bleiben gespeichert.",
        "en": "{count} of {total} announcements are spoken and stay saved.",
    },
    "tab_store.cancelled_quota_note_eleven": {
        "de": (" Das dafür verbrauchte ElevenLabs-Kontingent ist weg, "
               "aber beim nächsten Anlauf macht die App genau hier "
               "weiter und fordert nur noch das Fehlende an."),
        "en": (" The ElevenLabs quota spent on those is gone, but "
               "next time the app picks up exactly here and only "
               "requests what's missing."),
    },
    "tab_store.cancelled_quota_note_windows": {
        "de": " Beim nächsten Anlauf macht die App genau hier weiter.",
        "en": " Next time the app picks up exactly here.",
    },
    "tab_store.generate_failed_badge": {
        "de": "Fehlgeschlagen",
        "en": "Failed",
    },
    "tab_store.error_title": {
        "de": "Fehler",
        "en": "Error",
    },

    # --- _on_cancel_work --------------------------------------------------
    "tab_store.cancelling_badge": {
        "de": "Wird abgebrochen ...",
        "en": "Cancelling ...",
    },
    "tab_store.cancel_requested_log": {
        "de": "Abbruch angefordert - die laufende Ansage wird noch zu Ende gesprochen.",
        "en": "Cancellation requested - the current announcement will still finish being spoken.",
    },

    # --- use_pack -----------------------------------------------------
    "tab_store.original_pack_missing_use_message": {
        "de": ("Lade zuerst unter 'Einzelne Ansagen' das offizielle "
               "Sprachpaket deines Roboters herunter. Erst damit kann ein "
               "Fremdpaket sicher auf dein Modell angepasst werden."),
        "en": ("First download your robot's official voice pack under "
               "'Individual Announcements'. Only then can a third-party "
               "pack be safely adapted to your model."),
    },
    "tab_store.use_pack_confirm_title": {
        "de": "'{name}' verwenden?",
        "en": "Use '{name}'?",
    },
    "tab_store.use_pack_confirm_message": {
        "de": ("Das Paket wird von folgender Quelle geladen:\n\n{url}\n\n"
               "Anschließend wird es auf das offizielle Paket deines Modells "
               "gelegt. Danach kannst du es unter 'Bauen und Aufspielen' "
               "installieren.\n\nFortfahren?"),
        "en": ("The pack will be downloaded from this source:\n\n{url}\n\n"
               "It'll then be laid over your model's official pack. "
               "After that you can install it under 'Build and "
               "Install'.\n\nContinue?"),
    },
    "tab_store.downloading_log": {
        "de": "Lade '{name}' von {url}",
        "en": "Downloading '{name}' from {url}",
    },
    "tab_store.downloading_badge": {
        "de": "Lade herunter ...",
        "en": "Downloading ...",
    },
    "tab_store.downloaded_log": {
        "de": "Heruntergeladen: {filename}",
        "en": "Downloaded: {filename}",
    },
    "tab_store.adapting_pack_log": {
        "de": "Passe das Paket auf dein Modell an ...",
        "en": "Adapting the pack to your model ...",
    },
    "tab_store.use_pack_ready_badge": {
        "de": "Bereit - {covered} von {total} Ansagen ersetzt",
        "en": "Ready - {covered} of {total} announcements replaced",
    },
    "tab_store.pack_prepared_title": {
        "de": "Paket vorbereitet",
        "en": "Pack Prepared",
    },
    "tab_store.pack_prepared_message": {
        "de": ("'{name}' wurde auf dein Modell angepasst.\n\n"
               "{covered} von {total} Ansagen bekommen die neue Stimme, der Rest "
               "bleibt auf Deutsch.\n\nWechsle jetzt zu "
               "'Bauen und Aufspielen' und klicke auf "
               "'Sprachpaket auf Roboter installieren'."),
        "en": ("'{name}' has been adapted to your model.\n\n"
               "{covered} of {total} announcements get the new voice, the "
               "rest stays in German.\n\nNow switch to "
               "'Build and Install' and click "
               "'Install Voice Pack on Robot'."),
    },
    "tab_store.use_pack_failed_badge": {
        "de": "Fehlgeschlagen",
        "en": "Failed",
    },
    "tab_store.use_pack_error_title": {
        "de": "Fehler",
        "en": "Error",
    },
})
