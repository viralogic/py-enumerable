# Fix #79: `reverse()` not reversing — Result

## Root Cause Analysis

### The Bug
`Enumerable.reverse()` returns elements in the original order rather than reversed when the source `Enumerable` has already been iterated.

### Execution Flow (with bug)

```python
e = Enumerable([1,2,3])
print(e)              # triggers __repr__ -> list(self) -> iterates e
print(e.reverse())    # BUG: returns [1, 2, 3] instead of [3, 2, 1]
```

1. `Enumerable.reverse()` → `Enumerable(data=reversed(self))`
2. `reversed(self)` → `self.__reversed__()` → `reversed(self._iterable)`
3. `self._iterable` is a `RepeatableIterable` (the original, already iterated)
4. `reversed(self._iterable)` calls `RepeatableIterable.__reversed__()`
5. **`RepeatableIterable.__reversed__()`**: `self._root` is NOT `None` (set during `print(e)`), so it enters the `else` branch
6. The `else` branch traverses the **singly**-linked list **forward** (following `next` only) — no reversal occurs

### The `else` branch at `core.py:94-97`

```python
else:
    while self._current is not None:
        yield self._current.value
        self._current = self._current.next
```

### Secondary Bug in `last()` / `last_or_default()`

`py_linq.py:221`: The `func`-with-predicate branch of `last()` is missing a `return`:
```python
if func is not None:
    self.reverse().where(func).first()   # <-- missing return!
return self.reverse().first()             # always executes regardless
```

## Git History

- **`0ab3621`** (Feb 2023): Changed `reverse()` from `ReversedEnumerable` (LifoQueue stack) to `Enumerable(data=reversed(self))`. Rewrote `RepeatableIterable` from `itertools.cycle` to singly-linked list. **Introduced this bug.**
- **Pre-`0ab3621`**: `reverse()` used `ReversedEnumerable` — always correct but always eager.

## Chosen Design: Doubly-Linked List + `_tail`

### Changes Applied

#### 1. `py_linq/core.py` — `Node` gains `prev`

```python
@dataclass
class Node(object):
    value: Any
    next: Optional[TNode] = None
    prev: Optional[TNode] = None
```

#### 2. `py_linq/core.py` — `RepeatableIterable` gains `_tail`

```python
class RepeatableIterable(object):
    def __init__(self, data=None):
        ...
        self._tail: TNode = None
```

#### 3. `RepeatableIterable.__iter__()` — wire `prev` and set `_tail`

When building the linked list from `_data`, set `node.prev = self._current` on each new node.

End result: `_root` → n1 → n2 → ... → `_tail`.

#### 4. `RepeatableIterable.__reversed__()` — build forward, traverse backward

Two cases:
- **First call (`_root is None`)**: build the forward list by iterating `_data`, then traverse from `_tail` backward via `prev` pointers.
- **Subsequent calls (`_root is set`)**: traverse from `_tail` backward via `prev` pointers — **zero allocation, zero re-iteration**.

Removed `import inspect` (no longer needed after eliminating the generator-to-list conversion hack).

#### 5. `py_linq/py_linq.py` — Fix `last()` missing `return`

```python
def last(self, func=None) -> Any:
    if func is not None:
        return self.reverse().where(func).first()   # <-- added 'return'
    return self.reverse().first()
```

### Memory Impact

| Change | Cost |
|--------|------|
| `prev` pointer per Node | 1 reference (~8 bytes) per element |
| `_tail` on RepeatableIterable | 1 reference |

Negligible. No runtime list allocation during reversal.

### Lazy/Eager Assessment

After the linked list is built (cache exists), `__reversed__` is **fully lazy** — it just walks `prev` pointers from `_tail` backward. No re-iteration of the source data, no list allocation, no copying.

| Source type | `__iter__` behavior | `__reversed__` behavior |
|-------------|---------------------|------------------------|
| Already iterated (cache exists) | Traverse `_root→_tail` via `next` | Traverse `_tail→_root` via `prev` — no allocation |
| Fresh list/sequence | Build linked list, yield | Build linked list, then traverse `prev` |
| Fresh generator | Build linked list as data consumed | Build linked list, then traverse `prev` |

## Tests Added

`test_reverse_issue_79` in `tests/test_functions.py` covers 11 cases:

| Case | What it tests |
|------|---------------|
| 1 | Reporter's scenario: iterate → reverse → `[3,2,1]` |
| 2 | Empty + add chain: `Enumerable().add(1).add(2).add(3).reverse()` |
| 3 | Add chain after iteration → reverse |
| 4 | Double reverse after iteration → original order |
| 5 | Single element `[42]` → reverse → `[42]` |
| 6 | `None` values: `[None, 1, None, 3]` → reverse → `[3, None, 1, None]` |
| 7 | Generator source after iteration |
| 8 | `last()`/`last_or_default()` with predicate (missing return fix) |
| 9 | Chained `where(x > 2).reverse()` after iteration |
| 10 | Multiple reverse calls (re-entry) |
| 11 | String data |

## Verification

All 250 tests pass. 91% branch coverage.

```
uv run flake8 .          # only pre-existing lint issues, no new ones
uv run pytest tests      # 250 passed in 0.14s
uv run pytest tests --cov=py_linq --cov-branch --cov-report term  # 91% coverage
```

## Files Modified

- `py_linq/core.py` — `Node` (add `prev`), `RepeatableIterable.__init__` (add `_tail`), `__iter__`, `__reversed__`, remove `import inspect`
- `py_linq/py_linq.py` — `last()` add `return` on predicate branch
- `tests/test_functions.py` — added `test_reverse_issue_79`
- `.opencode/plans/fix-issue-79-reverse.md` — this file
