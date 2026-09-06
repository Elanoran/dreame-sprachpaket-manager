"""Central lookup for the app's user-facing strings, German or English.

Mirrors the existing dark-mode pattern (see ui/app.py's _toggle_theme):
the language takes effect the next time the app starts, not live -
rebuilding every already-built view while it's open would lose
whatever the user was in the middle of typing.

Each dreamevoice/locale/<module>.py calls register() once at import
time with its own slice of the table; this module just collects and
looks them up. Splitting the table per source file (instead of one
shared file everyone edits) is deliberate: it's what let this rollout
happen as many independent, non-conflicting edits at once.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import Any, Dict

_STRINGS: Dict[str, Dict[str, str]] = {}
_language = "en"

_VALID_LANGUAGES = ("en", "de")


def set_language(language: str) -> None:
    global _language
    _language = language if language in _VALID_LANGUAGES else "en"


def get_language() -> str:
    return _language


def register(strings: Dict[str, Dict[str, str]]) -> None:
    """Adds one module's slice of the table. Called by locale/*.py only.

    Raises on a key that already exists - almost always means two
    locale files picked the same key by accident.
    """
    for key, value in strings.items():
        if key in _STRINGS:
            raise ValueError(f"duplicate i18n key: {key!r}")
        _STRINGS[key] = value


def t(key: str, **kwargs: Any) -> str:
    """Looks up `key` in the current language.

    Falls back to English, then German, then the bare key itself -
    a visible-but-wrong string beats a crash on a missing translation.
    """
    entry = _STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(_language) or entry.get("en") or entry.get("de") or key
    return text.format(**kwargs) if kwargs else text


def _load_all_locales() -> None:
    from . import locale as locale_pkg
    for info in pkgutil.iter_modules(locale_pkg.__path__):
        importlib.import_module(f"{locale_pkg.__name__}.{info.name}")


_load_all_locales()
