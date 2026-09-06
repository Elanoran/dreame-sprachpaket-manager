# How a source file gets a language

One `dreamevoice/locale/<module>.py` per translated source file. Each
calls `register()` once with its own strings; `dreamevoice/i18n.py`
collects all of them and looks them up by key. Never edit another
file's locale module, and never put two files' strings in one locale
module - that's what let this be done as many parallel, non-conflicting
edits instead of one huge shared file.

## Getting both languages for a string

Every string in this app was translated German -> English earlier.
The German original is still in git history, at the commit tagged
`upstream-de` (equivalently: the last commit before `HEAD~N` where the
UI translation happened - `git log --oneline -- <path>` shows it).
For any file:

```bash
git show upstream-de:dreamevoice/ui/tab_store.py > /tmp/original_de.py
```

Diff that against the current file to see exactly which literal each
English string replaced. That diffed pair is your `"de"` / `"en"`.

## Key naming

`"<module_stem>.<short_snake_case_slug>"`, e.g. `"tab_store.create_pack_button"`.
The module prefix means keys never collide across files - don't spend
time deduplicating identical text at two different call sites, just
give each call site its own key.

## Worked examples

**Plain string:**

```python
# dreamevoice/locale/tab_store.py
from ..i18n import register

register({
    "tab_store.create_pack_button": {
        "de": "Eigenes Paket anlegen",
        "en": "Create Custom Pack ...",
    },
})
```

```python
# dreamevoice/ui/tab_store.py
from ..i18n import t
...
ttk.Button(eigene, text=t("tab_store.create_pack_button"), ...)
```

**One placeholder** (an f-string becomes a named `.format()` slot -
named, not positional, so German word order can move it):

```python
# before
raise PackError(f"unknown server {teil.hostname or '?'}")

# locale/official.py
register({
    "official.unknown_server": {
        "de": "unbekannter Server {host}",
        "en": "unknown server {host}",
    },
})

# after
raise PackError(t("official.unknown_server", host=teil.hostname or "?"))
```

**Multiple placeholders**, same rule, just more keyword args:

```python
register({
    "tab_install.pack_summary": {
        "de": "{count} Ansagen, {size} MB",
        "en": "{count} announcements, {size} MB",
    },
})
...
t("tab_install.pack_summary", count=n, size=mb)
```

## What NOT to touch

Same boundary as the original translation pass:

- Code comments, docstrings, variable/function names - stay as-is.
- Dialect speech content (`TEXTE` dicts in `dreamevoice/dialects/*.py`,
  `RAUM_NAMEN`, `AKKU_MUSTER`, `RAUM_MUSTER`) - these are the actual
  dialect scripts, not app UI, and must keep working as dialect text
  regardless of the UI language.
- Log-only messages that never reach a dialog, label, or other
  user-visible surface - not worth the churn.
- `sound_catalog.json` - already carries independent `de`/`en` fields
  per entry for a different purpose (catalog display), unrelated to
  this table.

## Verifying your file

```bash
python -m py_compile dreamevoice/locale/<module>.py dreamevoice/ui/<module>.py
python -c "from dreamevoice import i18n; i18n.set_language('de'); print('ok')"
```

The second command imports every locale module (including yours) and
will raise immediately on a duplicate key or a syntax error in the
table.
