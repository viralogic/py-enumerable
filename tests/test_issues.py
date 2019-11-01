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

    def test_issue22(self):
        def my_iter():
            for i in range(10):
                yield i

        def low_iter():
            for i in range(5):
                yield i

        def high_iter():
            for k in range(5):
                yield k + 5

        data = my_iter()
        a = Enumerable(data)

        low = a.where(lambda x: x < 5)
        high = a.where(lambda x: x >= 5)

        self.assertItemsEqual(low_iter(), low)
        self.assertItemsEqual(high_iter(), high)
        self.assertItemsEqual(my_iter(), a)

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
        joined = en2.join(en10, lambda x: x.number, lambda y: y.number, lambda r: (r[0].power, r[1].power))
        truth = zip([2 ** i for i in range(2)], [10 ** y for y in range(2)])
        self.assertItemsEqual(truth, joined)

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
