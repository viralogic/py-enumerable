import os
import io
from unittest import TestCase
from py_linq import Enumerable
from tests import _empty, _simple, _complex
from py_linq import exceptions
import itertools


class IssueTests(TestCase):
    def setUp(self):
        self.empty = Enumerable(_empty)
        self.simple = Enumerable(_simple)
        self.complex = Enumerable(_complex)

    def test_issue19_1(self):
        foo = Enumerable([1])
        bar = Enumerable([1])
        self.assertEqual(foo.intersect(bar).count(), 1)

    def test_issue19_2(self):
        foo = Enumerable([1])
        bar = Enumerable([1]).distinct()
        self.assertEqual(foo.intersect(bar).count(), 1)

    def test_issue19_3(self):
        foo = Enumerable([1]).distinct()
        bar = Enumerable([1])
        self.assertEqual(foo.intersect(bar).count(), 1)

    def test_issue22(self):
        def my_iter():
            for i in range(10):
                yield i

        data = my_iter()
        a = Enumerable(data)

        low = a.where(lambda x: x < 5)
        high = a.where(lambda x: x >= 5)

        self.assertListEqual(
            [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)], low.zip(high).to_list()
        )

        self.assertListEqual(
            [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)], list(zip(low, high))
        )

    def test_generator_to_Enumerable(self):
        def first_3():
            for i in range(3):
                yield i

        p2 = Enumerable(first_3())
        self.assertListEqual([0, 1, 2], p2.to_list())

        p3 = Enumerable((i for i in first_3()))
        self.assertListEqual([0, 1, 2], p3.to_list())

    def test_issue22_join(self):
        class Val(object):
            def __init__(self, number, power):
                self.number = number
                self.power = power

            def __str__(self):
                return "VAL {0}: {1}".format(self.number, self.power)

        def powers_of_2():
            for i in range(2):
                yield Val(i, 2 ** i)

        def powers_of_10():
            for i in range(2):
                yield Val(i, 10 ** i)

        en2 = Enumerable(powers_of_2())
        en10 = Enumerable(powers_of_10())
        joined = en2.join(
            en10,
            lambda x: x.number,
            lambda y: y.number,
            lambda r: (r[0].power, r[1].power),
        )
        truth = zip([2 ** i for i in range(2)], [10 ** y for y in range(2)])
        self.assertListEqual(list(truth), joined.to_list())

    def test_first_with_lambda(self):
        self.assertRaises(IndexError, self.empty.first, lambda x: x == 0)
        self.assertEqual(2, self.simple.first(lambda x: x == 2))
        self.assertDictEqual(
            {"value": 2}, self.complex.first(lambda x: x["value"] == 2)
        )

    def test_first_or_default_with_lambda(self):
        self.assertIsNone(self.empty.first_or_default(lambda x: x == 0))
        self.assertEqual(
            self.simple.first(lambda x: x == 2),
            self.simple.first_or_default(lambda x: x == 2),
        )
        self.assertEqual(
            self.complex.first(lambda x: x["value"] == 2),
            self.complex.first_or_default(lambda x: x["value"] == 2),
        )

    def test_last_with_lambda(self):
        self.assertRaises(IndexError, self.empty.last, lambda x: x == 0)
        self.assertEqual(2, self.simple.last(lambda x: x == 2))
        self.assertDictEqual({"value": 2}, self.complex.last(lambda x: x["value"] == 2))
        self.assertEqual(
            self.simple.first(lambda x: x == 2), self.simple.last(lambda x: x == 2)
        )

    def test_last_or_default_with_lambda(self):
        self.assertIsNone(self.empty.last_or_default(lambda x: x == 0))
        self.assertEqual(
            self.simple.last(lambda x: x == 2),
            self.simple.last_or_default(lambda x: x == 2),
        )
        self.assertEqual(
            self.complex.last(lambda x: x["value"] == 2),
            self.complex.last_or_default(lambda x: x["value"] == 2),
        )
        self.assertEqual(
            self.simple.first_or_default(lambda x: x == 2),
            self.simple.last_or_default(lambda x: x == 2),
        )

    def test_issue_34(self):
        class Obj(object):
            def __init__(self, n, v):
                self.n = n
                self.v = v

        foo = Enumerable([Obj("foo", 1), Obj("bar", 2)])
        self.assertTrue(foo.any(lambda x: x.n == "foo"))
        self.assertTrue(foo.any(lambda x: x.n == "foo"))
        filtered_foo = foo.where(lambda x: x.n == "foo")
        self.assertIsNotNone(filtered_foo.first())
        self.assertEqual("foo", filtered_foo.first().n)
        self.assertTrue(filtered_foo.any(lambda x: x.v == 1))
        self.assertTrue(filtered_foo.any(lambda x: x.v == 1))

    def test_issue_35(self):
        a = Enumerable([9, 8, -7, 6, 5])
        b = a.order_by(lambda x: x)
        self.assertEqual(-7, b.first())
        self.assertEqual(-7, list(b)[0])
        self.assertEqual(-7, b.first())

    def test_issue_36(self):
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
        self.assertEqual(1, len(result))
        self.assertEqual("This line should be counted", result[0])

    def test_issue_47(self):
        marks = Enumerable([(25, "a"), (49, "b"), (50, "c"), (80, "d"), (90, "e")])
        passing = marks.where(lambda x: x[0] >= 50)
        self.assertListEqual([(50, "c"), (80, "d"), (90, "e")], passing.to_list())
        omarks = Enumerable([(80, "eighty"), (49, "fortynine")])
        join_result = omarks.join(
            passing, lambda o: o[0], lambda y: y[0], lambda result: result
        ).to_list()
        self.assertListEqual([((80, "eighty"), (80, "d"))], join_result)

    def test_empty_join(self):
        marks = Enumerable([(25, "a"), (49, "b"), (50, "c"), (80, "d"), (90, "e")])
        passing = marks.where(lambda x: x[0] > 90)
        self.assertListEqual([], passing.to_list())
        omarks = Enumerable([(80, "eighty"), (49, "fortynine")])
        join_result = omarks.join(
            passing, lambda o: o[0], lambda y: y[0], lambda result: result
        ).to_list()
        self.assertListEqual([], join_result)

    def test_issue_50(self):
        """
        Only single char for key value on group_by
        """

        class MyObject(object):
            def __init__(self, name):
                self.field = name

            def get_field(self):
                return self.field

        test = Enumerable(
            [MyObject("Bruce"), MyObject("Bruce"), MyObject("Fenske"), MyObject("Luke")]
        )
        group = test.group_by(key_names=["field_name"], key=lambda r: r.get_field())
        self.assertEqual("Bruce", group[0].key.field_name)

    def test_issue_50_2(self):
        class MyObject(object):
            def __init__(self, name):
                self.field = name

            def get_field(self):
                return self.field

        def get_field(item):
            return item.get_field()

        test = Enumerable(
            [MyObject("Bruce"), MyObject("Bruce"), MyObject("Fenske"), MyObject("Luke")]
        )
        group = test.group_by(key_names=["field_name"], key=get_field).order_by(
            lambda g: g.key.field_name
        )
        self.assertEqual("Bruce", group[0].key.field_name)

    def test_issue_53(self):
        test = Enumerable([{"name": "test", "value": "test"}])
        test.add({"name": "test2", "value": "test2"})
        self.assertListEqual(
            [
                {"name": "test", "value": "test"},
                {"name": "test2", "value": "test2"},
            ],
            test.to_list(),
        )
        test.add(42)
        self.assertListEqual(
            [
                {"name": "test", "value": "test"},
                {"name": "test2", "value": "test2"},
                42,
            ],
            test.to_list(),
        )

    def test_issue_53_2(self):
        test = Enumerable()
        self.assertListEqual([], test.to_list())
        test.add({"name": "test", "value": "test"})
        self.assertListEqual([{"name": "test", "value": "test"}], test.to_list())
        test.add(42)
        self.assertListEqual([{"name": "test", "value": "test"}, 42], test.to_list())

    def test_issue_52(self):
        def func(r):
            return r

        e1 = Enumerable([{"value": 1}, {"value": 2}, {"value": 3}, {"value": 0}])
        e2 = Enumerable([1, 2, 3, 1, 2, 1])
        res = e1.group_join(
            e2,
            outer_key=lambda x: x["value"],
            inner_key=lambda y: y,
            result_func=lambda r: func(r),
        )

        expected = [
            ({"value": 1}, {"key": "{'id': 1}", "enumerable": "[1, 1, 1]"}),
            ({"value": 2}, {"key": "{'id': 2}", "enumerable": "[2, 2]"}),
            ({"value": 3}, {"key": "{'id': 3}", "enumerable": "[3]"}),
        ]

        self.assertEqual(len(expected), res.count())
        self.assertEqual(3, next(res)[1].count())
        self.assertEqual(2, next(res)[1].count())
        self.assertEqual(1, next(res)[1].count())

    def test_issue_52_2(self):

        e1 = Enumerable([{"value": 1}, {"value": 2}, {"value": 3}, {"value": 0}])
        e2 = Enumerable([1, 2, 3, 1, 2, 1])
        res = e1.group_join(
            e2,
            outer_key=lambda x: x["value"],
            inner_key=lambda y: y,
            result_func=lambda r: (r[0], r[1].to_list()),
        )

        self.assertListEqual(
            [
                ({"value": 1}, [1, 1, 1]),
                ({"value": 2}, [2, 2]),
                ({"value": 3}, [3]),
            ],
            res.to_list(),
        )
