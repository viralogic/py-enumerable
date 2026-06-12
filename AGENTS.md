# py-linq — AGENTS.md

## Project layout
- `py_linq/__init__.py` — package entry point, exports `Enumerable`; `__version__ = "1.2.4"`
- `py_linq/py_linq.py` — main `Enumerable` class + subclasses (`SortedEnumerable`, `GroupedEnumerable`, `SkipWhileEnumerable`, `TakeWhileEnumerable`, `ZipEnumerable`)
- `py_linq/core.py` — `RepeatableIterable` (caches iteration in linked list for re-iteration), `Key`, `OrderingDirection`, `Node`
- `py_linq/decorators.py` — `deprecated` decorator
- `py_linq/exceptions.py` — `NoElementsError`, `NullArgumentError`, `NoMatchingElement`, `MoreThanOneMatchingElement`

## Python / toolchain
- Python 3.7.15 (`.python-version`); supports `>=3.6.1`
- **Poetry** for dependency management. Dev commands use `poetry run ...`
- **Pre-commit**: Black (rev 23.1.0, lang py3.7) + Flake8 (rev 6.0.0)
- Black line length: 88 (`.flake8` matches)
- Flake8 ignores: `W503,E712,E231,E203,E501,E741,F401,F811,F841`

## Commands
| Action | Command |
|--------|---------|
| Install deps | `poetry install` |
| Install pre-commit hooks | `poetry run pre-commit install` |
| Lint | `poetry run flake8 .` |
| Test (single run) | `poetry run pytest tests` |
| Test with coverage | `poetry run pytest tests --cov=py_linq --cov-branch --cov-report term` |
| Build & publish | `poetry publish --build` |

Run **lint before test** — that is the CI order.

## Testing quirks
- Heavy use of `@pytest.mark.parametrize` — test data lives in `tests/fixtures.py`
- `pytest.ini`: `log_cli = 1`, `log_cli_level = INFO`
- `tests/test_performance.py` is fully commented out — skip it

## Things to not miss
- **Version is duplicated**: `pyproject.toml` (`[tool.poetry].version`) and `py_linq/__init__.py` (`__version__`) are separate — update both when bumping.
- **`except_`** uses trailing underscore (Python keyword conflict).
- **`RepeatableIterable`** stores iterated results in a linked list internally so repeated calls like `.first()` / `.any()` work on the same source. This is non-obvious but critical.
- **`add()`** is not in-place (functional style, returns new `Enumerable`). Prefer `append()` / `prepend()` for clarity.
- Generators passed to `Enumerable()` are exhausted once — `RepeatableIterable` lists them internally for re-iteration.

## CI / branching
- CI triggers on push to any branch except `master`/`release/*`, and on PRs to `development`
- Test matrix: Python 3.7, 3.8, 3.9, 3.10
- `release/*` → dry-run publish to Test PyPI. `master` → live publish.
