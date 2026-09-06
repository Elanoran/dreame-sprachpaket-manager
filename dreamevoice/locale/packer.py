"""German/English strings for packer.py (building the custom voice pack)."""

from __future__ import annotations

from ..i18n import register

register({
    "packer.foreign_pack_not_zip": {
        "de": "Das Fremdpaket ist kein lesbares zip-Archiv.",
        "en": "The foreign pack isn't a readable zip archive.",
    },
    "packer.foreign_pack_not_zip_or_targz": {
        "de": "Das Fremdpaket ist weder ein lesbares tar.gz- noch ein "
              "zip-Archiv.",
        "en": "The foreign pack is neither a readable tar.gz nor a zip "
              "archive.",
    },
    "packer.technical_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "packer.summary_replaced": {
        "de": "{replaced} von {total} Ansagen ersetzt",
        "en": "{replaced} of {total} announcements replaced",
    },
    "packer.base_pack_missing_title": {
        "de": "Das Originalpaket fehlt.",
        "en": "The original pack is missing.",
    },
    "packer.base_pack_missing_hint": {
        "de": "Lade unter 'Einzelne Ansagen' zuerst das offizielle Paket "
              "deines Roboters herunter - es dient als sichere Grundlage.",
        "en": "First download your robot's official pack under 'Individual "
              "Announcements' - it serves as the safe foundation.",
    },
    "packer.no_assignments_title": {
        "de": "Es ist noch keine einzige Ansage ausgetauscht.",
        "en": "Not a single announcement has been replaced yet.",
    },
    "packer.no_assignments_hint": {
        "de": "Weise mindestens einer Ansage eine eigene Audiodatei zu.",
        "en": "Assign at least one announcement an audio file of your own.",
    },
    "packer.log_preparing_audio": {
        "de": "Bereite Audiodateien vor ...",
        "en": "Preparing audio files ...",
    },
    "packer.announcement_error": {
        "de": "Ansage {id}: {message}",
        "en": "Announcement {id}: {message}",
    },
    "packer.converted_suffix": {
        "de": "  (umgewandelt)",
        "en": "  (converted)",
    },
    "packer.asis_suffix": {
        "de": "  (übernommen)",
        "en": "  (used as-is)",
    },
    "packer.log_building_archive": {
        "de": "Baue Archiv auf Basis des Originalpakets ...",
        "en": "Building the archive based on the original pack ...",
    },
    "packer.warning_new_announcement": {
        "de": "Ansage {id} kommt im Originalpaket nicht vor und wurde neu "
              "hinzugefügt. Ob der Roboter sie nutzt, ist offen.",
        "en": "Announcement {id} doesn't exist in the original pack and "
              "was newly added. Whether the robot uses it is open.",
    },
    "packer.archive_write_failed_title": {
        "de": "Das Archiv konnte nicht geschrieben werden.",
        "en": "The archive couldn't be written.",
    },
    "packer.archive_write_failed_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "packer.pack_save_failed_title": {
        "de": "Das Paket konnte nicht gespeichert werden.",
        "en": "The pack couldn't be saved.",
    },
    "packer.pack_save_failed_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "packer.log_done_md5": {
        "de": "Fertig: {size:.1f} MB, MD5 {md5}",
        "en": "Done: {size:.1f} MB, MD5 {md5}",
    },
    "packer.reopen_failed_title": {
        "de": "Das gebaute Paket ließ sich nicht wieder öffnen.",
        "en": "The built pack couldn't be reopened.",
    },
    "packer.reopen_failed_hint": {
        "de": "Es wird nicht installiert. Technische Details: {details}",
        "en": "It won't be installed. Technical details: {details}",
    },
    "packer.missing_files_title": {
        "de": "Im gebauten Paket fehlen {count} Dateien aus dem Original.",
        "en": "The built pack is missing {count} files from the original.",
    },
    "packer.missing_files_hint": {
        "de": "Das Paket wird sicherheitshalber nicht installiert. "
              "Bitte baue es erneut.",
        "en": "As a precaution, the pack won't be installed. "
              "Please build it again.",
    },
    "packer.file_not_found": {
        "de": "Die Datei wurde nicht gefunden:\n{path}",
        "en": "The file wasn't found:\n{path}",
    },
    "packer.unreadable_pack_title": {
        "de": "Das ist kein lesbares Sprachpaket.",
        "en": "That's not a readable voice pack.",
    },
    "packer.unreadable_pack_hint": {
        "de": "Erwartet wird ein tar.gz-Archiv mit Ansagen als .ogg-Dateien. "
              "Technische Details: {details}",
        "en": "A tar.gz archive with announcements as .ogg files is expected. "
              "Technical details: {details}",
    },
    "packer.no_announcements_title": {
        "de": "In dieser Datei sind keine Ansagen enthalten.",
        "en": "This file contains no announcements.",
    },
    "packer.no_announcements_hint": {
        "de": "Ein Sprachpaket besteht aus Dateien wie 7.ogg, 12.ogg und "
              "so weiter.",
        "en": "A voice pack consists of files like 7.ogg, 12.ogg, and so on.",
    },
    "packer.warning_missing_metadata": {
        "de": "Diesem Paket fehlen die Steuerdateien des Originals. Es "
              "stammt vermutlich von einem anderen Modell. Sicherer ist "
              "es, das Paket unter 'Eigene Stimmen' auf dein Modell "
              "anpassen zu lassen.",
        "en": "This pack is missing the original's control files. It "
              "probably comes from a different model. It's safer to have "
              "the pack adapted to your model under 'Custom Voices'.",
    },
    "packer.overlay_base_missing_title": {
        "de": "Das Originalpaket deines Modells fehlt.",
        "en": "Your model's original pack is missing.",
    },
    "packer.overlay_base_missing_hint": {
        "de": "Lade es unter 'Einzelne Ansagen' herunter.",
        "en": "Download it under 'Individual Announcements'.",
    },
    "packer.log_reading_overlay": {
        "de": "Lese Fremdpaket ...",
        "en": "Reading the third-party pack ...",
    },
    "packer.overlay_empty": {
        "de": "Das Fremdpaket enthält keine Ansagen (.ogg-Dateien).",
        "en": "The third-party pack contains no announcements (.ogg files).",
    },
    "packer.log_overlay_count": {
        "de": "Fremdpaket enthält {count} Ansagen.",
        "en": "The third-party pack contains {count} announcements.",
    },
    "packer.overlay_build_failed_title": {
        "de": "Das angepasste Paket konnte nicht gebaut werden.",
        "en": "The adapted pack couldn't be built.",
    },
    "packer.overlay_build_failed_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "packer.warning_unused_overlay": {
        "de": "{count} Ansagen des Fremdpakets haben im Originalpaket "
              "deines Modells keine Entsprechung und wurden weggelassen.",
        "en": "{count} announcements from the third-party pack have no "
              "match in your model's original pack and were left out.",
    },
    "packer.log_overlay_done": {
        "de": "Fertig: {size:.1f} MB, {count} Ansagen übernommen",
        "en": "Done: {size:.1f} MB, {count} announcements taken over",
    },
})
