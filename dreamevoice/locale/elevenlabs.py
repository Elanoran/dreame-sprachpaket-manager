"""German/English strings for elevenlabs.py (ElevenLabs TTS client)."""

from __future__ import annotations

from ..i18n import register

register({
    "elevenlabs.voice_creation_self": {"de": "selbst erzeugt", "en": "self-created"},
    "elevenlabs.voice_creation_cloned": {"de": "geklont", "en": "cloned"},
    "elevenlabs.voice_no_name": {"de": "(ohne Namen)", "en": "(no name)"},

    "elevenlabs.quota_left": {
        "de": "{left} von {limit} Zeichen übrig",
        "en": "{left} of {limit} characters left",
    },

    "elevenlabs.unreachable_title": {
        "de": "ElevenLabs ist nicht erreichbar.",
        "en": "ElevenLabs can't be reached.",
    },
    "elevenlabs.unreachable_detail": {
        "de": "Aufruf: {method} {url}\nTechnische Details: {error}",
        "en": "Call: {method} {url}\nTechnical details: {error}",
    },

    "elevenlabs.auth_rejected_title": {
        "de": "Der Zugangsschlüssel wurde nicht akzeptiert.",
        "en": "The access key wasn't accepted.",
    },
    "elevenlabs.auth_rejected_detail": {
        "de": ("Aufruf: {method} {url}\n"
               "Antwort: {response}\n\n"
               "Prüfe den Schlüssel unter elevenlabs.io/app/settings/api-keys. "
               "Er beginnt mit 'sk_'. Achte darauf, dass beim Kopieren nichts "
               "abgeschnitten wurde und kein Leerzeichen mitgekommen ist."),
        "en": ("Call: {method} {url}\n"
               "Response: {response}\n\n"
               "Check the key at elevenlabs.io/app/settings/api-keys. "
               "It starts with 'sk_'. Make sure nothing was cut off when "
               "copying and no space came along."),
    },

    "elevenlabs.quota_exhausted_title": {
        "de": "Das Kontingent bei ElevenLabs ist aufgebraucht.",
        "en": "The quota at ElevenLabs is used up.",
    },
    "elevenlabs.quota_exhausted_detail": {
        "de": ("Das Freikontingent füllt sich jeden Monat wieder auf. Bis "
               "dahin kannst du das Paket mit der Windows-Stimme erzeugen."),
        "en": ("The free quota refills every month. Until then you can "
               "generate the pack with the Windows voice."),
    },

    "elevenlabs.no_response_given": {"de": "(ohne Angabe)", "en": "(none given)"},
    "elevenlabs.throttled_title": {
        "de": "ElevenLabs nimmt gerade keine weitere Anfrage an.",
        "en": "ElevenLabs isn't accepting further requests right now.",
    },
    "elevenlabs.throttled_detail": {
        "de": ("Der Dienst begrenzt, wie viele Ansagen gleichzeitig gesprochen "
               "werden dürfen. Die App drosselt sich selbst und versucht es "
               "erneut - das ist kein Fehler.\n\n"
               "Antwort des Dienstes: {response}"),
        "en": ("The service limits how many announcements can be spoken at "
               "once. The app throttles itself and tries again - this isn't "
               "an error.\n\n"
               "Service response: {response}"),
    },

    "elevenlabs.no_key_entered": {
        "de": "Es wurde kein Zugangsschlüssel eingetragen.",
        "en": "No access key was entered.",
    },
    "elevenlabs.http_error_generic": {
        "de": "ElevenLabs antwortete mit HTTP {status}.",
        "en": "ElevenLabs responded with HTTP {status}.",
    },
    "elevenlabs.voice_list_failed": {
        "de": "Die Stimmenliste kam nicht an (HTTP {status}).",
        "en": "The voice list didn't come through (HTTP {status}).",
    },

    "elevenlabs.no_custom_voices": {
        "de": ("Wichtig: In dem Konto, zu dem dieser Zugangsschlüssel "
               "gehört, gibt es überhaupt keine eigenen Stimmen - nur die "
               "mitgelieferten. Die gesuchte Stimme wurde also sehr "
               "wahrscheinlich in einem anderen ElevenLabs-Konto "
               "angelegt. Trag oben den Schlüssel des Kontos ein, in dem "
               "die Stimme steht.\n\n"),
        "en": ("Important: the account this access key belongs to has no "
               "custom voices at all - only the built-in ones. So the "
               "voice you're looking for was very likely created in a "
               "different ElevenLabs account. Enter the key for the "
               "account the voice is in above.\n\n"),
    },
    "elevenlabs.custom_voices_count": {
        "de": ("Zur Einordnung: In dem Konto zu diesem Schlüssel liegen "
               "{count} eigene Stimmen - die gesuchte ist nicht darunter.\n\n"),
        "en": ("For reference: the account for this key has "
               "{count} custom voices - the one you're looking for isn't "
               "among them.\n\n"),
    },

    "elevenlabs.no_voice_id_title": {
        "de": "Es wurde keine Stimmen-ID eingetragen.",
        "en": "No voice ID was entered.",
    },
    "elevenlabs.no_voice_id_detail": {
        "de": ("Die ID steht in ElevenLabs bei der Stimme unter den drei Punkten "
               "('Copy Voice ID') und ist rund 20 Zeichen lang."),
        "en": ("The ID is on the voice in ElevenLabs under the three dots "
               "('Copy Voice ID') and is about 20 characters long."),
    },

    "elevenlabs.id_field_has_key_title": {
        "de": "Im Feld für die Stimmen-ID steht ein Zugangsschlüssel.",
        "en": "The voice ID field has an access key in it.",
    },
    "elevenlabs.id_field_has_key_detail": {
        "de": ("Schlüssel beginnen mit 'sk_', Stimmen-IDs nicht. Die beiden "
               "Felder sind vermutlich vertauscht: der Schlüssel gehört nach "
               "oben, die Stimmen-ID hierher."),
        "en": ("Keys start with 'sk_', voice IDs don't. The two fields are "
               "probably swapped: the key belongs above, the voice ID here."),
    },

    "elevenlabs.voice_key_rejected_title": {
        "de": "ElevenLabs hat den Zugangsschlüssel abgelehnt.",
        "en": "ElevenLabs rejected the access key.",
    },
    "elevenlabs.voice_key_rejected_detail": {
        "de": ("Antwort des Servers (HTTP {status}):\n{message}\n\n"
               "Ein gültiger Schlüssel beginnt mit 'sk_'. Häufigste Ursachen:\n"
               "· beim Kopieren wurde nur ein Teil erwischt\n"
               "· der Schlüssel wurde in ElevenLabs zurückgezogen oder neu erzeugt\n"
               "· Schlüssel und Stimmen-ID sind in den Feldern vertauscht\n\n"
               "Neuen Schlüssel holen: elevenlabs.io/app/settings/api-keys"),
        "en": ("Server response (HTTP {status}):\n{message}\n\n"
               "A valid key starts with 'sk_'. Most common causes:\n"
               "· only part of it was caught when copying\n"
               "· the key was revoked or regenerated in ElevenLabs\n"
               "· key and voice ID are swapped in the fields\n\n"
               "Get a new key: elevenlabs.io/app/settings/api-keys"),
    },

    "elevenlabs.voice_not_found_title": {
        "de": "Zu der ID '{voice_id}' konnte keine Stimme geladen werden.",
        "en": "No voice could be loaded for the ID '{voice_id}'.",
    },
    "elevenlabs.voice_not_found_detail": {
        "de": ("Antwort des Servers (HTTP {status}):\n{message}\n\n"
               "{account_hint}"
               "Prüfe die ID in deinem ElevenLabs-Konto: bei der Stimme auf die "
               "drei Punkte klicken und 'Copy Voice ID' wählen. Stimmen aus der "
               "öffentlichen Bibliothek musst du erst deinem Konto hinzufügen, "
               "bevor du sie über die ID ansprechen kannst."),
        "en": ("Server response (HTTP {status}):\n{message}\n\n"
               "{account_hint}"
               "Check the ID in your ElevenLabs account: click the three "
               "dots on the voice and choose 'Copy Voice ID'. Voices from "
               "the public library must first be added to your account "
               "before you can address them by ID."),
    },

    "elevenlabs.voice_load_failed_title": {
        "de": "Die Stimme konnte nicht geladen werden (HTTP {status}).",
        "en": "The voice couldn't be loaded (HTTP {status}).",
    },
    "elevenlabs.voice_load_failed_detail": {
        "de": "Antwort des Servers:\n{message}",
        "en": "Server response:\n{message}",
    },

    "elevenlabs.settings_defaults": {
        "de": "Standardwerte von ElevenLabs", "en": "ElevenLabs defaults",
    },
    "elevenlabs.stability_lively": {"de": "lebendig", "en": "lively"},
    "elevenlabs.stability_balanced": {"de": "ausgewogen", "en": "balanced"},
    "elevenlabs.stability_uniform": {"de": "gleichförmig", "en": "uniform"},
    "elevenlabs.stability_label": {
        "de": "Stabilität {value:.2f} ({kind})",
        "en": "Stability {value:.2f} ({kind})",
    },
    "elevenlabs.style_label": {
        "de": "Stil {value:.2f}", "en": "Style {value:.2f}",
    },
    "elevenlabs.rate_label": {
        "de": "Tempo {value:.2f}", "en": "Rate {value:.2f}",
    },
    "elevenlabs.settings_custom": {
        "de": "eigene Einstellungen", "en": "custom settings",
    },

    "elevenlabs.add_voice_failed": {
        "de": "Die Stimme konnte nicht ins Konto übernommen werden.",
        "en": "The voice couldn't be added to the account.",
    },

    "elevenlabs.no_voice_selected": {
        "de": "Es wurde keine Stimme ausgewählt.",
        "en": "No voice was selected.",
    },
    "elevenlabs.no_texts_provided": {
        "de": "Es wurden keine Texte übergeben.",
        "en": "No texts were provided.",
    },
    "elevenlabs.voice_sound_log": {
        "de": "Klang der Stimme: {settings}",
        "en": "Voice sound: {settings}",
    },
    "elevenlabs.announcements_reused": {
        "de": "{count} Ansagen liegen schon vor und werden wiederverwendet.",
        "en": "{count} announcements already exist and will be reused.",
    },
    "elevenlabs.announcement_failed": {
        "de": "Ansage {id} konnte nicht gesprochen werden (HTTP {status}).",
        "en": "Announcement {id} couldn't be spoken (HTTP {status}).",
    },

    "elevenlabs.throttled_repeatedly_title": {
        "de": "ElevenLabs hat mehrfach gebremst.",
        "en": "ElevenLabs throttled repeatedly.",
    },
    "elevenlabs.throttled_repeatedly_detail": {
        "de": ("Ansage {id} ließ sich auch nach {attempts} Versuchen nicht "
               "sprechen. Versuche es später noch einmal - das Bisherige "
               "bleibt gespeichert."),
        "en": ("Announcement {id} couldn't be spoken even after {attempts} "
               "attempts. Try again later - what's already done stays "
               "saved."),
    },

    "elevenlabs.quota_used_up_progress": {
        "de": "Kontingent aufgebraucht nach {done} von {total} Ansagen.",
        "en": "Quota used up after {done} of {total} announcements.",
    },
    "elevenlabs.quota_resume_note": {
        "de": ("Das Bisherige bleibt gespeichert. Beim nächsten "
               "Versuch macht die App genau hier weiter."),
        "en": ("What's already done stays saved. The app "
               "picks up exactly here next time."),
    },

    "elevenlabs.aborted_at_announcement": {
        "de": "Abbruch bei Ansage {id}: {error}",
        "en": "Aborted at announcement {id}: {error}",
    },
    "elevenlabs.announcements_done_saved": {
        "de": "{count} Ansagen sind fertig und bleiben erhalten.",
        "en": "{count} announcements are done and stay saved.",
    },

    "elevenlabs.throttled_persistent_title": {
        "de": "ElevenLabs bremst dauerhaft.",
        "en": "ElevenLabs is throttling persistently.",
    },
    "elevenlabs.throttled_persistent_detail": {
        "de": ("Auch nach {waves} Versuchen mit immer weniger gleichzeitigen "
               "Anfragen kam keine einzige Ansage durch. Versuche es später "
               "noch einmal - das Bisherige bleibt gespeichert."),
        "en": ("Even after {waves} attempts with fewer and fewer "
               "simultaneous requests, not a single announcement got "
               "through. Try again later - what's already done stays "
               "saved."),
    },
    "elevenlabs.throttling_now_running": {
        "de": "ElevenLabs bremst - es laufen jetzt {count} Ansagen gleichzeitig.",
        "en": "ElevenLabs is throttling - now running {count} announcements at once.",
    },
    "elevenlabs.progress_spoken": {
        "de": "  {done} von {total} Ansagen gesprochen ...",
        "en": "  {done} of {total} announcements spoken ...",
    },
    "elevenlabs.no_announcement_generated": {
        "de": "Es wurde keine einzige Ansage erzeugt.",
        "en": "Not a single announcement was generated.",
    },
    "elevenlabs.announcements_received": {
        "de": "{count} Ansagen von ElevenLabs erhalten.",
        "en": "{count} announcements received from ElevenLabs.",
    },
})
