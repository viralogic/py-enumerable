from py_linq import Enumerable
import pytest


_simple = [1, 2, 3]
_complex = [{"value": 1}, {"value": 2}, {"value": 3}]

_locations = [
    ("Scotland", "Edinburgh", "Branch1", 20000),
    ("Scotland", "Glasgow", "Branch1", 12500),
    ("Scotland", "Glasgow", "Branch2", 12000),
    ("Wales", "Cardiff", "Branch1", 29700),
    ("Wales", "Cardiff", "Branch2", 30000),
    ("Wales", "Bangor", "Branch1", 12800),
    ("England", "London", "Branch1", 90000),
    ("England", "London", "Branch2", 80000),
    ("England", "London", "Branch3", 70000),
    ("England", "Manchester", "Branch1", 45600),
    ("England", "Manchester", "Branch2", 50000),
    ("England", "Liverpool", "Branch1", 29700),
    ("England", "Liverpool", "Branch2", 25000),
]


@pytest.fixture
def empty() -> Enumerable:
    return Enumerable([])


@pytest.fixture
def simple() -> Enumerable:
    return Enumerable(_simple)


@pytest.fixture
def complex() -> Enumerable:
    return Enumerable(_complex)


@pytest.fixture
def locations() -> Enumerable:
    return Enumerable(_locations)


def simple_generator(max: int):
    for i in range(max + 1):
        yield i


class Val(object):
    def __init__(self, number, power):
        self.number = number
        self.power = power

    def __str__(self):
        return "VAL {0}: {1}".format(self.number, self.power)


def powers(base: int, num_iterations: int = 2):
    for i in range(num_iterations):
        yield Val(i, base ** i)


class Obj(object):
    def __init__(self, n, v):
        self.n = n
        self.v = v


class MyObject(object):
    def __init__(self, name):
        self.field = name

    def get_field(self):
        return self.field


def groupjoin_func(r):
    return (r[0], r[1].count())
