# py-linq — AGENTS.md

## Project layout
- `py_linq/__init__.py` — package entry point, exports `Enumerable`; `__version__ = "1.4.0"`
- `py_linq/py_linq.py` — main `Enumerable` class + subclasses (`SortedEnumerable`, `GroupedEnumerable`, `SkipWhileEnumerable`, `TakeWhileEnumerable`, `ZipEnumerable`)
- `py_linq/core.py` — `RepeatableIterable` (caches iteration in linked list for re-iteration), `Key`, `OrderingDirection`, `Node`
- `py_linq/decorators.py` — `deprecated` decorator
- `py_linq/exceptions.py` — `NoElementsError`, `NullArgumentError`, `NoMatchingElement`, `MoreThanOneMatchingElement`

## Python / toolchain
- Python 3.8.20 (`.python-version`); supports `>=3.8`
- **uv** for dependency management. Dev commands use `uv run ...`
- **Pre-commit**: Black (rev 23.1.0, lang py3.7) + Flake8 (rev 6.0.0)
- Black line length: 88 (`.flake8` matches)
- Flake8 ignores: `W503,E712,E231,E203,E501,E741,F401,F811,F841`

## Commands
| Action | Command |
|--------|---------|
| Install deps | `uv sync` |
| Install pre-commit hooks | `uv run pre-commit install` |
| Lint | `uv run flake8 .` |
| Test (single run) | `uv run pytest tests` |
| Test with coverage | `uv run pytest tests --cov=py_linq --cov-branch --cov-report term` |
| Build | `uv build` |
| Publish | `uv publish` |

Run **lint before test** — that is the CI order.

## Testing quirks
- Heavy use of `@pytest.mark.parametrize` — test data lives in `tests/fixtures.py`
- `pytest.ini`: `log_cli = 1`, `log_cli_level = INFO`
- `tests/test_performance.py` is fully commented out — skip it

## Things to not miss
- **Version is duplicated**: `pyproject.toml` (`[project].version`) and `py_linq/__init__.py` (`__version__`) are separate — update both when bumping.
- **`except_`** uses trailing underscore (Python keyword conflict).
- **`RepeatableIterable`** stores iterated results in a linked list internally so repeated calls like `.first()` / `.any()` work on the same source. This is non-obvious but critical.
- **`add()`** is not in-place (functional style, returns new `Enumerable`). Prefer `append()` / `prepend()` for clarity.
- Generators passed to `Enumerable()` are exhausted once — `RepeatableIterable` lists them internally for re-iteration.

## CI / branching
- CI triggers on push to any branch except `master`/`release/*`, and on PRs to `development`
- Test matrix: Python 3.8, 3.9, 3.10
- `release/*` → dry-run publish to Test PyPI. `master` → live publish.
