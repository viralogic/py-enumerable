# py-linq — Working in this repo

## Adding a new LINQ method

- Add the method to `Enumerable` in `py_linq.py`
- Use **snake_case** (Python convention, not .NET's PascalCase)
- **Lazy by default**: return `Enumerable(...)` wrapping a generator, `map`, `filter`, or `itertools.islice`
- **Subclass** only if iteration behavior needs custom state: copy `SkipWhileEnumerable`, `TakeWhileEnumerable`, or `ZipEnumerable` as a template
- Validate `Enumerable` parameters with `isinstance(x, Enumerable)`, raise `TypeError`
- Use custom exceptions from `py_linq/exceptions.py` for domain errors (`NullArgumentError`, `NoElementsError`, etc.)
- Return a **new** `Enumerable` — never mutate in place
- Document in `docs/<method-name>.md`

## Fixing a bug

1. Reproduce with a minimal `Enumerable(...)` test case
2. Write the failing test first — prefer `@pytest.mark.parametrize` in `test_functions.py`; use standalone `def test_` for complex cases
3. **Critical regression**: repeated calls (`.first()` → `.first()`, iterate → `.any()`) must not break — the `RepeatableIterable` linked-list cache is the top failure mode
4. `poetry run flake8 .` → `poetry run pytest tests` — in that order

## Testing conventions

- Test data goes in `tests/fixtures.py` as **module-level vars** (`_simple`, `_complex`, `_locations`) — only use `@pytest.fixture` if setup logic is needed
- Parametrize heavily: cases as tuples, grouped as `test_executors` (assert `value == total`) or `test_non_executors` (assert `to_list() == expected`)
- `Grouping` comparison: construct `Grouping(Key({"name": val}), data=[...])`
- `tests/test_performance.py` is fully commented out — skip it
- `pytest.ini`: `log_cli = 1`, `log_cli_level = INFO`

## Tech debt

- **Version sync**: both `pyproject.toml` (`[tool.poetry].version`) and `py_linq/__init__.py` (`__version__`) must match — check both when bumping
- **Python 2 compat**: `six`, `future`, and `imap`/`ifilter`/`izip` fallbacks in `py_linq.py` — assess removal if dropping Py2
- **`except_`**: trailing underscore because `except` is a Python keyword

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Methods | `snake_case` | `first_or_default`, `order_by_descending` |
| Classes | `PascalCase` | `SortedEnumerable`, `GroupedEnumerable` |
| Keyword conflicts | trailing `_` | `except_` |

## Branch & PR workflow

- `master` → production publish to PyPI
- `release/*` → dry-run publish to Test PyPI
- All other branches → CI only
- PRs target the `development` branch
- CI order: lint → test (Python 3.7–3.10 matrix)
- No PR template — write a clear title and description

## Prerequisite checklist

```bash
poetry install                 # if deps changed
poetry run pre-commit install  # one-time setup
poetry run flake8 .            # before commit
poetry run pytest tests        # after lint
```
