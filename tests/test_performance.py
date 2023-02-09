from typing import (
    Generator,
    List,
    Dict,
)
import pytest
from py_linq import Enumerable


@pytest.fixture
def test_generator() -> Generator:
    return ({"id": x, "value": x} for x in range(0, 80000))


@pytest.fixture
def test_enumerable(test_generator) -> Enumerable:
    return Enumerable(test_generator)


def test_constructor(benchmark, test_generator: Generator) -> None:
    data = benchmark(Enumerable, test_generator)
    assert data is not None


def test_select(benchmark, test_enumerable: Enumerable) -> None:
    benchmark(test_enumerable.select, lambda b: {"id": b["id"]})


def test_to_list(benchmark, test_enumerable: Enumerable) -> None:
    benchmark(test_enumerable.to_list)


def test_list_comprehension(benchmark, test_generator: Generator) -> None:
    def to_list() -> List[Dict[str, int]]:
        return [{"id": b["id"]} for b in test_generator]

    benchmark(to_list)


def test_list(benchmark, test_generator: Generator) -> None:
    benchmark(list, test_generator)

def test_iter(benchmark, test_enumerable: Enumerable) -> None:
    def iterate():
        it = iter(test_enumerable)
        try:
            while next(it):
                continue
        except StopIteration:
            pass
    benchmark(iterate)
