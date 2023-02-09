import io
import os
from py_linq import Enumerable
from py_linq.exceptions import (
    NoElementsError,
    NullArgumentError,
    NoMatchingElement,
    MoreThanOneMatchingElement,
)

from py_linq.py_linq import Grouping, Key
import six
import pytest
from tests.fixtures import (
    _simple,
    _complex,
    _locations,
    simple_generator,
    powers,
    Obj,
    MyObject,
    groupjoin_func,
)
from typing import (
    List,
    Any,
    Type,
    Union,
    Callable,
)


def reverse(result, element):
    return element + " " + result


def sum(result, element):
    return result + element


@pytest.mark.parametrize(
    "enumerable",
    [
        Enumerable(),
        Enumerable([]),
        Enumerable(_simple),
        Enumerable(_complex),
    ],
)
def test_constructor(enumerable: Enumerable) -> None:
    assert isinstance(enumerable, Enumerable)


@pytest.mark.parametrize(
    "enumerable, expected",
    [
        (Enumerable(), []),
        (Enumerable([]), []),
        (Enumerable(_simple), _simple),
        (Enumerable(_complex), _complex),
        (Enumerable().select(lambda x: x), []),
        (Enumerable([]).select(lambda x: x), []),
        (Enumerable(_simple).select(lambda x: x), _simple),
        (Enumerable(_complex).select(lambda x: x["value"]), _simple),
        (Enumerable().where(lambda x: x == 2), []),
        (Enumerable([]).where(lambda x: x == 2), []),
        (Enumerable(_simple).where(lambda x: x == 2), [2]),
        (Enumerable(_complex).where(lambda x: x["value"] == 2), [{"value": 2}]),
        (Enumerable().to_list(), []),
        (Enumerable(_simple).to_list(), _simple),
        (Enumerable(_complex).to_list(), _complex),
    ],
)
def test_iter(enumerable: Enumerable, expected: List) -> None:
    assert list(iter(enumerable)) == expected


@pytest.mark.parametrize(
    "enumerable, count",
    [
        (Enumerable(), 0),
        (Enumerable(_simple), len(_simple)),
        (Enumerable(_complex), len(_complex)),
    ],
)
def test_len(enumerable: Enumerable, count: int) -> None:
    assert len(enumerable) == count


@pytest.mark.parametrize(
    "enumerable, index, expected",
    [
        (Enumerable(), 0, None),
        (Enumerable(_simple), 1, 2),
        (Enumerable(_complex), 1, {"value": 2}),
        (Enumerable().select(lambda x: x["value"]), 0, None),
        (Enumerable(_complex).select(lambda x: x["value"]), 1, 2),
        (Enumerable(_simple).select(lambda x: x), 1, 2),
    ],
)
def test_get_item(enumerable: Enumerable, index: int, expected: Any) -> None:
    assert enumerable[index] == expected


@pytest.mark.parametrize(
    "enumerable, index, expected",
    [
        (Enumerable(_simple).element_at, 1, 2),
        (Enumerable(_complex).element_at, 1, {"value": 2}),
    ],
)
def test_element_at(enumerable: Callable, index: int, expected: Any) -> None:
    assert enumerable(index) == expected


@pytest.mark.parametrize(
    "enumerable, index, error",
    [
        (Enumerable().element_at, 0, IndexError),
    ],
)
def test_element_at_error(enumerable: Callable, index: int, error: Exception) -> None:
    with pytest.raises(error):
        enumerable(index)


@pytest.mark.parametrize(
    "value, total",
    [
        (Enumerable().sum(), 0),
        (Enumerable(_simple).sum(), 6),
        (Enumerable(_complex).select(lambda x: x["value"]).sum(), 6),
        (Enumerable(_complex).sum(lambda x: x["value"]), 6),
        (Enumerable().count(), 0),
        (Enumerable(_simple).count(), 3),
        (Enumerable(_complex).count(), 3),
        (Enumerable().count(lambda x: x == 1), 0),
        (Enumerable(_simple).count(lambda x: x == 1), 1),
        (Enumerable(_complex).count(lambda x: x["value"] > 1), 2),
        (Enumerable(_simple).min(), 1),
        (Enumerable(_complex).min(lambda x: x["value"]), 1),
        (Enumerable(_simple).max(), 3),
        (Enumerable(_complex).max(lambda x: x["value"]), 3),
        (Enumerable(_simple).avg(), float(2)),
        (Enumerable(_complex).avg(lambda x: x["value"]), float(2)),
        (Enumerable(_simple).median(), 2),
        (Enumerable(_complex).median(lambda x: x["value"]), 2),
        (Enumerable([1, 2, 3, 4]).median(), 2.5),
        (Enumerable(_simple).first(), 1),
        (Enumerable(_complex).first(), {"value": 1}),
        (Enumerable().first_or_default(), None),
        (Enumerable(_simple).first_or_default(), 1),
        (Enumerable(_complex).first_or_default(), {"value": 1}),
        (Enumerable(_simple).last(), 3),
        (Enumerable(_complex).last(), {"value": 3}),
        (Enumerable().last_or_default(), None),
        (Enumerable(_simple).last_or_default(), 3),
        (Enumerable(_complex).last_or_default(), {"value": 3}),
        (Enumerable(_simple).single(lambda x: x == 2), 2),
        (Enumerable(_complex).single(lambda x: x["value"] == 2), {"value": 2}),
        (Enumerable(_complex).select(lambda x: x["value"]).single(lambda x: x == 2), 2),
        (Enumerable(_simple).single_or_default(lambda x: x > 3), None),
        (Enumerable(_simple).single_or_default(lambda x: x == 3), 3),
        (Enumerable(_simple).add(4).count(), 4),
        (Enumerable(_simple).add(4).add(5).count(), 5),
        (Enumerable(_simple).add(4).add(5).last(), 5),
        (Enumerable(_simple).order_by_descending(lambda x: x)[0], 3),
        (Enumerable(_locations).distinct(lambda x: x[0]).count(), 3),
        (Enumerable().any(lambda x: x == 1), False),
        (Enumerable().any(), False),
        (Enumerable(_simple).any(lambda x: x == 1), True),
        (Enumerable(_simple).any(), True),
        (Enumerable(_complex).any(), True),
        (Enumerable(_complex).any(lambda x: x["value"] < 1), False),
        (Enumerable(_complex).any(lambda x: x["value"] > 1), True),
        (Enumerable().contains(1), False),
        (Enumerable(_simple).contains(1), True),
        (Enumerable(_complex).select(lambda x: x["value"]).contains(1), True),
        (
            Enumerable(_complex)
            .group_join(Enumerable([1, 2, 3, 3]), outer_key=lambda x: x["value"])
            .count(),
            3,
        ),
        (Enumerable([1, 1, 1]).all(lambda x: x == 1), True),
        (Enumerable([]).all(lambda x: x == 1), True),
        (Enumerable(_simple).all(lambda x: x == 1), False),
        (
            Enumerable(["ab", "bc", "cd", "de"]).to_dictionary(lambda t: t[0]),
            {"a": "ab", "b": "bc", "c": "cd", "d": "de"},
        ),
        (
            Enumerable([[0, 1, 2], [3, 4, 5], [6, 7, 8]]).to_dictionary(
                lambda t: t[0], lambda t: t[1:]
            ),
            {0: [1, 2], 3: [4, 5], 6: [7, 8]},
        ),
        (Enumerable(_simple).first(lambda x: x == 2), 2),
        (Enumerable(_complex).first(lambda x: x["value"] == 2), {"value": 2}),
        (Enumerable.empty().first_or_default(lambda x: x == 0), None),
        (
            Enumerable(_simple).first(lambda x: x == 2),
            Enumerable(_simple).first_or_default(lambda x: x == 2),
        ),
        (
            Enumerable(_complex).first(lambda x: x["value"] == 2),
            Enumerable(_complex).first_or_default(lambda x: x["value"] == 2),
        ),
        (
            Enumerable(_simple).last(lambda x: x == 2),
            Enumerable(_simple).last_or_default(lambda x: x == 2),
        ),
        (
            Enumerable(_complex).last(lambda x: x["value"] == 2),
            Enumerable(_complex).last_or_default(lambda x: x["value"] == 2),
        ),
        (
            Enumerable(_simple).first(lambda x: x == 2),
            Enumerable(_simple).last(lambda x: x == 2),
        ),
        (Enumerable.empty().last_or_default(lambda x: x == 0), None),
        (
            Enumerable(_complex).last(lambda x: x["value"] == 2),
            Enumerable(_complex).last_or_default(lambda x: x["value"] == 2),
        ),
        (
            Enumerable(_simple).last_or_default(lambda x: x == 2),
            Enumerable(_simple).first_or_default(lambda x: x == 2),
        ),
    ],
)
def test_executors(value: Union[int, float], total: Union[int, float]) -> None:
    assert value == total


@pytest.mark.parametrize(
    "enumerable, func, error",
    [
        (Enumerable().min, None, NoElementsError),
        (Enumerable().max, None, NoElementsError),
        (Enumerable().avg, None, NoElementsError),
        (Enumerable().median, None, NoElementsError),
        (Enumerable().first, None, IndexError),
        (Enumerable().last, None, IndexError),
        (Enumerable.empty().first, lambda x: x == 0, IndexError),
        (Enumerable.empty().last, lambda x: x == 0, IndexError),
    ],
)
def test_executors_error(
    enumerable: Callable, func: Callable, error: Exception
) -> None:
    with pytest.raises(error):
        enumerable(func)


@pytest.mark.parametrize(
    "enumerable, expected",
    [
        (Enumerable.empty(), []),
        (Enumerable().select(lambda x: x["value"]), []),
        (Enumerable(_simple).select(lambda x: {"value": x}), _complex),
        (Enumerable(_complex).select(lambda x: x["value"]), _simple),
        (Enumerable([2, 1, 3]).order_by(lambda x: x), _simple),
        (
            Enumerable([{"value": 2}, {"value": 1}, {"value": 3}]).order_by(
                lambda x: x["value"]
            ),
            _complex,
        ),
        (Enumerable(_simple).order_by_descending(lambda x: x), list(reversed(_simple))),
        (
            Enumerable(_complex).order_by_descending(lambda x: x["value"]),
            [{"value": 3}, {"value": 2}, {"value": 1}],
        ),
        (
            Enumerable([{"value": 2}, {"value": 1}, {"value": 3}])
            .select(lambda x: x["value"])
            .order_by(lambda x: x),
            _simple,
        ),
        (
            Enumerable(_complex)
            .select(lambda x: x["value"])
            .order_by_descending(lambda x: x),
            [3, 2, 1],
        ),
        (Enumerable([2, 1, 3]).where(lambda x: x >= 2).order_by(lambda x: x), [2, 3]),
        (
            Enumerable(_simple)
            .where(lambda x: x >= 2)
            .order_by_descending(lambda x: x),
            [3, 2],
        ),
        (Enumerable().skip(2), []),
        (Enumerable(_simple).skip(3), []),
        (Enumerable(_simple).skip(1), [2, 3]),
        (Enumerable(_simple).take(4), _simple),
        (Enumerable(_simple).take(0), []),
        (Enumerable(_simple).take(2), [1, 2]),
        (Enumerable(_simple).skip(1).take(1), [2]),
        (Enumerable(_complex).select(lambda x: x["value"]).skip(1).take(1), [2]),
        (Enumerable().where(lambda x: x == 0), []),
        (Enumerable(_simple).where(lambda x: x == 2), [2]),
        (Enumerable(_complex).where(lambda x: x["value"] == 2), [{"value": 2}]),
        (Enumerable(_simple).where(lambda x: x == 0), []),
        (
            Enumerable(_complex)
            .where(lambda x: x["value"] == 2)
            .select(lambda x: x["value"]),
            [2],
        ),
        (Enumerable().concat(Enumerable()), []),
        (Enumerable().concat(Enumerable(_simple)), _simple),
        (Enumerable(_simple).concat(Enumerable()), _simple),
        (
            Enumerable(_simple).concat(
                Enumerable(_complex).select(lambda c: c["value"])
            ),
            [1, 2, 3, 1, 2, 3],
        ),
        (
            Enumerable(_complex)
            .select(lambda c: c["value"])
            .concat(Enumerable(_simple)),
            [1, 2, 3, 1, 2, 3],
        ),
        (
            Enumerable(_simple).concat(Enumerable(_complex)),
            [1, 2, 3, {"value": 1}, {"value": 2}, {"value": 3}],
        ),
        (Enumerable([[], [], []]).select_many(), []),
        (
            Enumerable([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).select_many(),
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        (
            Enumerable(
                [
                    {"key": 1, "values": [1, 2, 3]},
                    {"key": 2, "values": [4, 5, 6]},
                    {"key": 3, "values": [7, 8, 9]},
                ]
            ).select_many(lambda x: x["values"]),
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        (Enumerable.empty().distinct(), []),
        (Enumerable(_simple).concat(Enumerable(_simple)).distinct(), _simple),
        (Enumerable().default_if_empty(), [None]),
        (Enumerable(_simple).default_if_empty(), _simple),
        (Enumerable(_complex).default_if_empty(), _complex),
        (Enumerable().join(Enumerable()), []),
        (Enumerable().join(Enumerable(_simple)), []),
        (Enumerable().join(Enumerable(_complex)), []),
        (Enumerable(_simple).join(Enumerable(_simple)), [(1, 1), (2, 2), (3, 3)]),
        (
            Enumerable(_simple).join(
                Enumerable(_complex),
                inner_key=lambda x: x["value"],
                result_func=lambda x: (x[0], x[1]["value"]),
            ),
            [(1, 1), (2, 2), (3, 3)],
        ),
        (
            Enumerable(_complex).join(
                Enumerable(_complex),
                result_func=lambda x: (x[0]["value"], x[1]["value"]),
            ),
            [(1, 1), (2, 2), (3, 3)],
        ),
        (Enumerable().intersect(Enumerable(), lambda x: x), []),
        (Enumerable().intersect(Enumerable(_simple), lambda x: x), []),
        (Enumerable(_simple).intersect(Enumerable(_simple), lambda x: x), _simple),
        (Enumerable(_simple).intersect(Enumerable([2]), lambda x: x), [2]),
        (Enumerable(_simple).intersect(Enumerable(_complex), lambda x: x["value"]), []),
        (
            Enumerable(_complex).intersect(Enumerable(_complex), lambda x: x["value"]),
            _complex,
        ),
        (
            Enumerable(_complex).intersect(
                Enumerable([{"value": 1}]), lambda x: x["value"]
            ),
            [{"value": 1}],
        ),
        (
            Enumerable(
                [{"course": "Chemistry", "mark": 90}, {"course": "Biology", "mark": 85}]
            ).intersect(
                Enumerable(
                    [
                        {"course": "Chemistry", "mark": 65},
                        {"course": "Computer Science", "mark": 96},
                    ]
                ),
                lambda c: c["course"],
            ),
            [{"course": "Chemistry", "mark": 90}],
        ),
        (Enumerable().except_(Enumerable(), lambda x: x), []),
        (Enumerable().except_(Enumerable(_simple), lambda x: x), []),
        (Enumerable(_simple).except_(Enumerable(_simple), lambda x: x), []),
        (Enumerable(_simple).except_(Enumerable([2]), lambda x: x), [1, 3]),
        (Enumerable(_simple).except_(Enumerable(), lambda x: x), _simple),
        (Enumerable(_simple).except_(Enumerable(_complex), lambda x: x["value"]), []),
        (
            Enumerable(_complex)
            .select(lambda x: x["value"])
            .except_(Enumerable(_simple), lambda x: x),
            [],
        ),
        (
            Enumerable(_complex).except_(
                Enumerable(_complex), key=lambda x: x["value"]
            ),
            [],
        ),
        (
            Enumerable(_complex).except_(
                Enumerable([{"value": 1}]), key=lambda x: x["value"]
            ),
            [{"value": 2}, {"value": 3}],
        ),
        (
            Enumerable(
                [
                    {"course": "Chemistry", "mark": 90},
                    {"course": "Biology", "mark": 85},
                ]
            ).except_(
                Enumerable(
                    [
                        {"course": "Chemistry", "mark": 65},
                        {"course": "Computer Science", "mark": 96},
                    ]
                ),
                lambda c: c["course"],
            ),
            [{"course": "Biology", "mark": 85}],
        ),
        (Enumerable().union(Enumerable(), lambda x: x), []),
        (Enumerable().union(Enumerable(_simple), lambda x: x), _simple),
        (Enumerable(_simple).union(Enumerable.empty(), lambda x: x), _simple),
        (
            Enumerable(_complex).union(Enumerable.empty(), lambda x: x["value"]),
            _complex,
        ),
        (Enumerable().union(Enumerable(_complex), lambda x: x["value"]), _complex),
        (Enumerable(_simple).union(Enumerable([4, 5]), lambda x: x), [1, 2, 3, 4, 5]),
        (
            Enumerable(_simple).union(Enumerable([1, 4, 5]), lambda x: x),
            [1, 2, 3, 4, 5],
        ),
        (
            Enumerable(_complex).union(
                Enumerable([{"value": 4}, {"value": 5}]), lambda x: x["value"]
            ),
            [{"value": 1}, {"value": 2}, {"value": 3}, {"value": 4}, {"value": 5}],
        ),
        (
            Enumerable(_complex).union(
                Enumerable([{"value": 1}, {"value": 4}, {"value": 5}]),
                lambda x: x["value"],
            ),
            [{"value": 1}, {"value": 2}, {"value": 3}, {"value": 4}, {"value": 5}],
        ),
        (Enumerable().group_join(Enumerable()), []),
        (Enumerable(_simple).group_join(Enumerable()), []),
        (
            Enumerable(_complex)
            .group_join(Enumerable([1, 2, 3, 3]), outer_key=lambda x: x["value"])
            .select(lambda t: (t[0], t[1].to_list())),
            [({"value": 1}, [1]), ({"value": 2}, [2]), ({"value": 3}, [3, 3])],
        ),
        (
            Enumerable(_simple).group_join(
                Enumerable([2, 3]),
                result_func=lambda x: {"number": x[0], "collection": x[1].to_list()},
            ),
            [{"number": 2, "collection": [2]}, {"number": 3, "collection": [3]}],
        ),
        (
            Enumerable(_locations)
            .order_by(lambda l: l[0])
            .then_by(lambda l: l[1])
            .select(lambda l: f"{l[1]}, {l[0]}"),
            [
                "Liverpool, England",
                "Liverpool, England",
                "London, England",
                "London, England",
                "London, England",
                "Manchester, England",
                "Manchester, England",
                "Edinburgh, Scotland",
                "Glasgow, Scotland",
                "Glasgow, Scotland",
                "Bangor, Wales",
                "Cardiff, Wales",
                "Cardiff, Wales",
            ],
        ),
        (
            Enumerable(_locations)
            .order_by(lambda l: l[0])
            .then_by_descending(lambda l: l[3])
            .select(lambda l: f"{l[1]}, {l[0]}: {l[3]}"),
            [
                "London, England: 90000",
                "London, England: 80000",
                "London, England: 70000",
                "Manchester, England: 50000",
                "Manchester, England: 45600",
                "Liverpool, England: 29700",
                "Liverpool, England: 25000",
                "Edinburgh, Scotland: 20000",
                "Glasgow, Scotland: 12500",
                "Glasgow, Scotland: 12000",
                "Cardiff, Wales: 30000",
                "Cardiff, Wales: 29700",
                "Bangor, Wales: 12800",
            ],
        ),
        (Enumerable(_simple).append(4), [1, 2, 3, 4]),
        (Enumerable(_simple).prepend(4), [4, 1, 2, 3]),
        (Enumerable.range(1, 3), _simple),
        (
            Enumerable.repeat("Z", 10),
            ["Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z"],
        ),
        (Enumerable().reverse(), []),
        (Enumerable(_simple).reverse(), [3, 2, 1]),
        (Enumerable(_simple).reverse().reverse(), _simple),
        (
            Enumerable(
                "the quick brown fox jumps over the lazy dog".split(" ")
            ).reverse(),
            ["dog", "lazy", "the", "over", "jumps", "fox", "brown", "quick", "the"],
        ),
        (
            Enumerable(simple_generator(4)).zip(Enumerable(simple_generator(4))),
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
        ),
        (
            Enumerable(simple_generator(9))
            .where(lambda i: i < 5)
            .zip(Enumerable(simple_generator(9)).where(lambda i: i >= 5)),
            [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)],
        ),
        (
            Enumerable(simple_generator(9))
            .where(lambda i: i >= 5)
            .zip(Enumerable(simple_generator(9)).where(lambda i: i < 5)),
            [(5, 0), (6, 1), (7, 2), (8, 3), (9, 4)],
        ),
        (Enumerable(simple_generator(2)), [0, 1, 2]),
        (Enumerable((i for i in simple_generator(2))), [0, 1, 2]),
        (
            Enumerable(powers(2)).join(
                Enumerable(powers(10)),
                lambda x: x.power,
                lambda y: y.power,
                lambda r: (r[0].power, r[1].power),
            ),
            [(1, 1)],
        ),
    ],
)
def test_non_executors(enumerable: Enumerable, expected: List) -> None:
    assert enumerable.to_list() == expected


@pytest.mark.parametrize(
    "enumerable, func, error",
    [
        (Enumerable(_simple).order_by, None, NullArgumentError),
        (Enumerable(_simple).order_by_descending, None, NullArgumentError),
        (Enumerable().single, lambda x: x == 0, NoMatchingElement),
        (Enumerable().single, None, NoMatchingElement),
        (Enumerable(_simple).single, lambda x: x == 0, NoMatchingElement),
        (Enumerable(_simple).single, None, MoreThanOneMatchingElement),
        (Enumerable(_complex).single, lambda x: x["value"] == 0, NoMatchingElement),
        (Enumerable(_complex).single, None, MoreThanOneMatchingElement),
        (Enumerable(_simple).single, lambda x: x > 0, MoreThanOneMatchingElement),
        (
            Enumerable(_complex).single,
            lambda x: x["value"] > 0,
            MoreThanOneMatchingElement,
        ),
        (
            Enumerable(_simple).single_or_default,
            lambda x: x > 0,
            MoreThanOneMatchingElement,
        ),
        (
            Enumerable(_complex).single_or_default,
            lambda x: x["value"] > 0,
            MoreThanOneMatchingElement,
        ),
        (Enumerable().join, None, TypeError),
        (Enumerable().intersect, None, TypeError),
        (Enumerable().except_, None, TypeError),
        (Enumerable().union, None, TypeError),
        (Enumerable.empty().group_join, None, TypeError),
        (
            Enumerable(_locations).order_by(lambda l: l[0]).then_by,
            None,
            NullArgumentError,
        ),
    ],
)
def test_non_executors_error(
    enumerable: Callable, func: Callable, error: Exception
) -> None:
    with pytest.raises(error):
        enumerable(func)


@pytest.mark.parametrize(
    "enumerable, expected",
    [
        (
            Enumerable(_simple).group_by(key_names=["id"]),
            [
                Grouping(Key({"id": 1}), data=[1]),
                Grouping(Key({"id": 2}), data=[2]),
                Grouping(Key({"id": 3}), data=[3]),
            ],
        ),
        (
            Enumerable(_complex).group_by(
                key_names=["value"], key=lambda x: x["value"]
            ),
            [
                Grouping(Key({"value": 1}), data=[{"value": 1}]),
                Grouping(Key({"value": 2}), data=[{"value": 2}]),
                Grouping(Key({"value": 3}), data=[{"value": 3}]),
            ],
        ),
    ],
)
def test_group_by_structure(enumerable: Enumerable, expected: List) -> None:
    assert len(enumerable) == len(expected)
    for i, v in enumerate(enumerable):
        v == expected[i]


def test_group_by_operations() -> None:
    locations_grouped = Enumerable(_locations).group_by(
        key_names=["country", "city"], key=lambda x: [x[0], x[1]]
    )
    assert locations_grouped.count() == 7

    london = locations_grouped.single(
        lambda c: c.key.city == "London" and c.key.country == "England"
    )
    assert london.sum(lambda c: c[3]) == 240000


@pytest.mark.parametrize(
    "enumerable, args, expected",
    [
        (
            Enumerable("the quick brown fox jumps over the lazy dog".split()),
            [reverse],
            ["dog lazy the over jumps fox brown quick the"],
        ),
        (Enumerable(), [lambda x: x[0] + x[1]], 0),
        (Enumerable(_simple), [sum, 0], 6),
    ],
)
def test_aggregate(enumerable: Enumerable, args: Callable, expected: Any) -> None:
    return enumerable.aggregate(*args) == expected


def test_repeated_first_calls() -> None:
    """
    This is a test case submitted for Issue 35
    """
    foo = Enumerable([Obj("foo", 1), Obj("bar", 2)])

    assert foo.any(lambda x: x.n == "foo")
    assert foo.any(lambda x: x.n == "foo")

    filtered_foo = foo.where(lambda x: x.n == "foo")
    assert filtered_foo.first() is not None
    assert filtered_foo.first().n == "foo"
    assert filtered_foo.any(lambda x: x.v == 1)
    assert filtered_foo.any(lambda x: x.v == 1)

    a = Enumerable([9, 8, -7, 6, 5])
    b = a.order_by(lambda x: x)
    assert b.first() == -7
    assert list(b)[0] == -7
    assert b.first() == -7


def test_aggregate_callback() -> None:
    """
    This is a test case submitted for Issue 36
    """

    def append_to_list(lst, element):
        lst.append(element)

    filepath = os.path.join(os.getcwd(), "tests", "files", "test_file1.txt")
    result = []
    with io.open(filepath) as f:
        lines = (
            Enumerable(f)
            .skip(1)
            .where(lambda l: not l.startswith("#"))
            .aggregate(append_to_list, result)
        )
    assert len(result) == 1
    assert result[0] == "This line should be counted"


def test_join_operation() -> None:
    marks = Enumerable([(25, "a"), (49, "b"), (50, "c"), (80, "d"), (90, "e")])
    passing = marks.where(lambda x: x[0] >= 50)
    assert passing.to_list() == [(50, "c"), (80, "d"), (90, "e")]

    omarks = Enumerable([(80, "eighty"), (49, "fortynine")])
    join_result = omarks.join(
        passing, lambda o: o[0], lambda y: y[0], lambda result: result
    ).to_list()
    assert join_result == [((80, "eighty"), (80, "d"))]


def test_group_by_keys() -> None:
    """
    This is a test case for Issue 50 where grouping on an object field was giving
    single character keys
    """
    test = Enumerable(
        [MyObject("Bruce"), MyObject("Bruce"), MyObject("Fenske"), MyObject("Luke")]
    )
    group = test.group_by(
        key_names=["field_name"], key=lambda r: r.get_field()
    ).order_by(lambda g: g.key.field_name)
    assert group[0].key.field_name == "Bruce"


def test_group_by_keys_with_grouping_callback() -> None:
    """
    This is another test case for Issue 50
    """

    def get_field(item):
        return item.get_field()

    test = Enumerable(
        [MyObject("Bruce"), MyObject("Bruce"), MyObject("Fenske"), MyObject("Luke")]
    )
    group = test.group_by(key_names=["field_name"], key=get_field).order_by(
        lambda g: g.key.field_name
    )
    assert group[0].key.field_name == "Bruce"


def test_add_operation() -> None:
    """
    This is a test case for Issue 53
    """
    test = Enumerable([{"name": "test", "value": "test"}])
    test = test.add({"name": "test2", "value": "test2"})
    assert [
        {"name": "test", "value": "test"},
        {"name": "test2", "value": "test2"},
    ] == test.to_list()

    test = test.add(42)

    assert [
        {"name": "test", "value": "test"},
        {"name": "test2", "value": "test2"},
        42,
    ] == test.to_list()

    test = Enumerable()
    assert [] == test.to_list()

    test = test.add({"name": "test", "value": "test"})
    assert [{"name": "test", "value": "test"}] == test.to_list()

    test = test.add(42)
    assert [{"name": "test", "value": "test"}, 42] == test.to_list()


@pytest.mark.parametrize(
    "enumerable1, enumerable2, result_callback, expected",
    [
        (
            Enumerable([{"value": 1}, {"value": 2}, {"value": 3}, {"value": 0}]),
            Enumerable([1, 2, 3, 1, 2, 1]),
            lambda r: (r[0], r[1].to_list()),
            [
                ({"value": 1}, [1, 1, 1]),
                ({"value": 2}, [2, 2]),
                ({"value": 3}, [3]),
            ],
        ),
        (
            Enumerable([{"value": 1}, {"value": 2}, {"value": 3}, {"value": 0}]),
            Enumerable([1, 2, 3, 1, 2, 1]),
            groupjoin_func,
            [
                ({"value": 1}, 3),
                ({"value": 2}, 2),
                ({"value": 3}, 1),
            ],
        ),
    ],
)
def test_group_join(
    enumerable1: Enumerable,
    enumerable2: Enumerable,
    result_callback: Callable,
    expected: List[Any],
) -> None:
    result = enumerable1.group_join(
        enumerable2,
        outer_key=lambda x: x["value"],
        inner_key=lambda y: y,
        result_func=result_callback,
    ).to_list()

    assert expected == result


def test_retain_ordering():
    """
    This is a test case submitted around the ordering of an Enumerable not being
    retained around successive executor calls. This bug forced a re-implementation
    of underlying Enumerable data structure.
    """
    e = Enumerable((x for x in range(0, 5)))
    assert e.first() == 0
    assert e.first() == 0
