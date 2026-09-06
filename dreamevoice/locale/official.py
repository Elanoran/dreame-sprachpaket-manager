"""German/English strings for official.py (fetching Dreame's official voice packs)."""

from __future__ import annotations

from ..i18n import register

register({
    "official.reason_invalid_identifier": {
        "de": "unzulässige Kennung {id!r}",
        "en": "invalid identifier {id!r}",
    },
    "official.no_scheme": {
        "de": "ohne Schema",
        "en": "no scheme",
    },
    "official.reason_no_https": {
        "de": "Bezugsadresse ohne https ({scheme})",
        "en": "source address without https ({scheme})",
    },
    "official.reason_unknown_server": {
        "de": "unbekannter Server {host}",
        "en": "unknown server {host}",
    },
    "official.reason_bad_checksum": {
        "de": "unbrauchbare Prüfsumme {md5!r}",
        "en": "unusable checksum {md5!r}",
    },
    "official.reason_no_size": {
        "de": "keine Größenangabe",
        "en": "no size given",
    },
    "official.reason_bad_size": {
        "de": "unplausible Größe {size} Bytes",
        "en": "implausible size {size} bytes",
    },
    "official.no_model_title": {
        "de": "Es ist kein Robotermodell bekannt.",
        "en": "No robot model is known.",
    },
    "official.no_model_hint": {
        "de": "Melde dich zuerst unter 'Verbindung' an.",
        "en": "Sign in under 'Connection' first.",
    },
    "official.catalog_unreachable": {
        "de": "Die Sprachpaketliste von Dreame ist nicht erreichbar.",
        "en": "Dreame's voice pack list can't be reached.",
    },
    "official.catalog_unreachable_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "official.model_no_catalog_title": {
        "de": "Für das Modell {model} bietet Dreame keine Sprachpaketliste an.",
        "en": "Dreame doesn't offer a voice pack list for the model {model}.",
    },
    "official.model_no_catalog_hint": {
        "de": "Das Modell ist entweder sehr neu oder wird über einen anderen "
              "Kanal versorgt. Ohne Originalpaket kann kein sicheres eigenes "
              "Paket gebaut werden.",
        "en": "The model is either very new or is served through a "
              "different channel. Without an original pack, no safe "
              "custom pack can be built.",
    },
    "official.http_status": {
        "de": "Dreame antwortete mit HTTP {status}.",
        "en": "Dreame responded with HTTP {status}.",
    },
    "official.catalog_unreadable": {
        "de": "Die Sprachpaketliste war unlesbar.",
        "en": "The voice pack list was unreadable.",
    },
    "official.catalog_bad_shape_title": {
        "de": "Die Sprachpaketliste von Dreame hat eine unerwartete Form.",
        "en": "Dreame's voice pack list has an unexpected shape.",
    },
    "official.catalog_bad_shape_hint": {
        "de": "Erwartet wurde eine Liste von Sprachpaketen. Es wurde nichts "
              "geladen und nichts an den Roboter geschickt. Bleibt es dabei, "
              "hat Dreame das Format geändert - dann hilft nur eine neue "
              "Fassung dieser App.",
        "en": "A list of voice packs was expected. Nothing was loaded and "
              "nothing was sent to the robot. If this persists, Dreame has "
              "changed the format - only a new version of this app can "
              "help then.",
    },
    "official.catalog_all_rejected_title": {
        "de": "Der Sprachpaket-Katalog von Dreame sieht ungewöhnlich aus.",
        "en": "Dreame's voice pack catalog looks unusual.",
    },
    "official.catalog_all_rejected_hint": {
        "de": "Alle {count} Einträge wurden abgelehnt. Grund: {reasons}."
              "\n\nEs wurde nichts geladen und nichts an den Roboter "
              "geschickt. Nennt der Grund einen unbekannten Server, hat "
              "Dreame die Auslieferung umgestellt - dann hilft nur eine "
              "neue Fassung dieser App.",
        "en": "All {count} entries were rejected. Reason: {reasons}."
              "\n\nNothing was loaded and nothing was sent to the "
              "robot. If the reason names an unknown server, Dreame "
              "has changed how it delivers packs - only a new version "
              "of this app can help then.",
    },
    "official.no_packs_for_model": {
        "de": "Dreame listet für {model} keine Sprachpakete auf.",
        "en": "Dreame lists no voice packs for {model}.",
    },
    "official.download_http_error": {
        "de": "Das Originalpaket konnte nicht geladen werden (HTTP {status}).",
        "en": "The original pack couldn't be loaded (HTTP {status}).",
    },
    "official.oversized_title": {
        "de": "Das angebotene Originalpaket ist unerwartet groß.",
        "en": "The offered original pack is unexpectedly large.",
    },
    "official.oversized_hint": {
        "de": "Der Download wurde abgebrochen. Ein Sprachpaket wiegt rund "
              "zehn Megabyte.",
        "en": "The download was aborted. A voice pack weighs about ten "
              "megabytes.",
    },
    "official.download_interrupted_title": {
        "de": "Der Download des Originalpakets ist abgebrochen.",
        "en": "The original pack download was interrupted.",
    },
    "official.download_interrupted_details": {
        "de": "Technische Details: {details}",
        "en": "Technical details: {details}",
    },
    "official.no_checksum_title": {
        "de": "Zu diesem Originalpaket nennt Dreame keine Prüfsumme.",
        "en": "Dreame doesn't give a checksum for this original pack.",
    },
    "official.no_checksum_hint": {
        "de": "Ohne sie lässt sich nicht feststellen, ob die Datei "
              "unterwegs verändert wurde. Sie wurde verworfen.",
        "en": "Without it, there's no way to tell whether the file was "
              "altered in transit. It was discarded.",
    },
    "official.corrupted_title": {
        "de": "Das heruntergeladene Originalpaket ist beschädigt.",
        "en": "The downloaded original pack is corrupted.",
    },
    "official.corrupted_hint": {
        "de": "Erwartete Prüfsumme {expected}, tatsächlich {actual}. "
              "Bitte erneut versuchen.",
        "en": "Expected checksum {expected}, got {actual}. "
              "Please try again.",
    },
    "official.describe_announcements": {
        "de": "{count} Ansagen",
        "en": "{count} announcements",
    },
    "official.describe_control_files": {
        "de": "{count} Steuerdateien",
        "en": "{count} control files",
    },
    "official.describe_built": {
        "de": "Stand {built}",
        "en": "built {built}",
    },
})
