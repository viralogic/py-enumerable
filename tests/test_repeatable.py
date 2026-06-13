import pytest
import itertools
from py_linq.core import RepeatableIterable


def test_iter_none() -> None:
    ri = RepeatableIterable()
    assert sum((1 for item in ri)) == 0


def test_iter_range() -> None:
    ri = RepeatableIterable(range(0, 5))
    for i, v in enumerate(ri):
        assert i == v
    assert ri.current.value == 0


def test_len() -> None:
    ri = RepeatableIterable(range(0, 3))
    assert len(ri) == 3
    assert ri.current.value == 0


def test_next() -> None:
    ri = RepeatableIterable(range(0, 2))
    assert len(ri) == 2
    assert ri.current.value == 0
    assert next(ri) == 1
    with pytest.raises(StopIteration):
        next(ri)


def test_iter_generator() -> None:
    def next_name() -> str:
        for n in ("Bruce", "viralogic", "software"):
            yield n

    ri = RepeatableIterable(next_name())
    assert len(ri) == 3
    assert next(ri) == "viralogic"


def test_reverse_chain() -> None:
    ri = RepeatableIterable(itertools.chain(range(1, 4), [4]))
    reversed_ri = reversed(ri)
    assert [4, 3, 2, 1] == list(reversed_ri)


def test_early_termination_with_break() -> None:
    source = [1, 2, 3, 4, 5]
    ri = RepeatableIterable(source)
    for item in ri:
        assert item == 1
        break
    assert len(ri) == 5
    assert list(ri) == [1, 2, 3, 4, 5]


def test_early_termination_via_enumerable_element_at() -> None:
    from py_linq import Enumerable

    data = [{"aci": i, "hex": "#000000", "rgb": (0, 0, 0)} for i in range(256)]
    e = Enumerable(data)
    assert e.element_at(100) == {"aci": 100, "hex": "#000000", "rgb": (0, 0, 0)}
    assert len(e) == 256


def test_first_with_predicate_after_early_termination() -> None:
    from py_linq import Enumerable

    data = [{"aci": i, "hex": "#000000", "rgb": (0, 0, 0)} for i in range(256)]
    e = Enumerable(data)
    assert e.first(lambda x: x["aci"] == 100) == {
        "aci": 100,
        "hex": "#000000",
        "rgb": (0, 0, 0),
    }
    assert len(e) == 256
