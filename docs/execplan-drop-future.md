# Exec Plan: Drop `future` Dependency

**Issue:** #84 — WinError 225 during pip install (Windows Defender false positive on `future` package)
**Status:** Completed
**Branch:** development
**Commit:** c906fa4

## Problem

The `future` package (v0.18.3) was declared as a runtime dependency in `pyproject.toml`. Windows Defender flagged `future-0.18.3.tar.gz` during pip's `setup.py egg_info`, causing `WinError 225` (`ERROR_VIRUS_INFECTED`) on Windows. The `future` package was only a Python 2/3 compatibility shim and is no longer needed since py-linq requires Python >=3.8.

## Analysis

| Artifact | Location | Action |
|----------|----------|--------|
| Dependency decl | `pyproject.toml` line 10 | Remove `"future>=0.18.2,<0.19"` |
| `from builtins import range` | `py_linq/py_linq.py` line 24 | Remove — no-op on Python >=3.8 |
| `range` usage | `py_linq/py_linq.py` line 575 | Unchanged — resolves to built-in `range` |
| `imap`/`ifilter`/`izip` fallback | `py_linq/py_linq.py` lines 17-23 | Remove — dead code (always fails on Python >=3.8) |
| Tech debt note | `PLANS.md` line 32 | Update to reflect removal |
| Lock file | `uv.lock` | Regenerate via `uv lock` |
| Virtual env | `.venv` | Sync via `uv sync --extra dev` |

## Steps Executed

1. **`py_linq/py_linq.py`** — Removed dead Python 2 compat block (`try: from itertools import imap as map...`) and `from builtins import range`
2. **`pyproject.toml`** — Removed `"future>=0.18.2,<0.19"` from `dependencies`
3. **`PLANS.md`** — Updated tech debt note
4. **`uv lock`** — Regenerated lock file (removed `future` entry)
5. **`uv sync --extra dev`** — Updated `.venv` (removed `future` package)
6. **Verification** — `uv run flake8 .` (clean), `uv run pytest tests` (250/250 passed)
