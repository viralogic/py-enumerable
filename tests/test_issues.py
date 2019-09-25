from unittest import TestCase
from py_linq import Enumerable
from tests import _empty, _simple, _complex
from py_linq import exceptions


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

    # def test_first_last(self):
    #     self.assertRaises(NoElementsError, self.empty.last)
    #     self.assertEqual(
    #         self.empty.last_or_default(),
    #         None,
    #         u"Last or default should be None")
    #     self.assertIsInstance(
    #         self.simple.last(),
    #         int,
    #         u"Last element in simple enumerable is int")
    #     self.assertEqual(
    #         self.simple.last(),
    #         3,
    #         u"Last element in simple enumerable is 3")
    #     self.assertEqual(
    #         self.simple.last(),
    #         self.simple.last_or_default(),
    #         u"Last and last or default should equal")
    #     self.assertIsInstance(
    #         self.complex.last(),
    #         dict,
    #         u"Last element in complex enumerable is dict")
    #     self.assertDictEqual(
    #         self.complex.last(),
    #         {'value': 3},
    #         u"Last element in complex enumerable is not correct dict")
    #     self.assertDictEqual(
    #         self.complex.last(),
    #         self.complex.last_or_default(),
    #         u"Last and last or default should equal")
    #     self.assertEqual(
    #         self.simple.last(),
    #         self.complex.select(lambda x: x['value']).last(),
    #         u"Last values in simple and complex should equal")

    def test_first_with_lambda(self):
        self.assertRaises(IndexError, self.empty.first, lambda x: x == 0)
        self.assertEqual(2, self.simple.first(lambda x: x == 2))
        self.assertDictEqual({'value': 2}, self.complex.first(lambda x: x['value'] == 2))

    def test_first_or_default_with_lambda(self):
        self.assertIsNone(self.empty.first_or_default(lambda x: x == 0))
        self.assertEqual(self.simple.first(lambda x: x == 2), self.simple.first_or_default(lambda x: x == 2))
        self.assertEqual(self.complex.first(lambda x: x['value'] == 2), self.complex.first_or_default(lambda x: x['value'] == 2))

    def test_last_with_lambda(self):
        self.assertRaises(IndexError, self.empty.last, lambda x: x == 0)
        self.assertEqual(2, self.simple.last(lambda x: x == 2))
        self.assertDictEqual({'value': 2}, self.complex.last(lambda x: x['value'] == 2))
        self.assertEqual(self.simple.first(lambda x: x == 2), self.simple.last(lambda x: x == 2))

    def test_last_or_default_with_lambda(self):
        self.assertIsNone(self.empty.last_or_default(lambda x: x == 0))
        self.assertEqual(self.simple.last(lambda x: x == 2), self.simple.last_or_default(lambda x: x == 2))
        self.assertEqual(self.complex.last(lambda x: x['value'] == 2), self.complex.last_or_default(lambda x: x['value'] == 2))
        self.assertEqual(self.simple.first_or_default(lambda x: x == 2), self.simple.last_or_default(lambda x: x == 2))
