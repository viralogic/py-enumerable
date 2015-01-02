__author__ = 'Viralogic Software'

from unittest import TestCase
from py_linq import Enumerable
from tests import _empty, _simple, _complex
from py_linq.exceptions import *


class TestFunctions(TestCase):
    def setUp(self):
        self.empty = Enumerable(_empty)
        self.simple = Enumerable(_simple)
        self.complex = Enumerable(_complex)

    def test_to_list(self):
        empty_list = self.empty.to_list()
        simple_list = self.simple.to_list()
        complex_list = self.complex.to_list()

        self.assertIsInstance(empty_list, list, "Empty enumerable not converted to list")
        self.assertIsInstance(simple_list, list, "Simple enumerable not converted to list")
        self.assertIsInstance(complex_list, list, "Complex enumerable not converted to list")

        self.assertEqual(len(empty_list), 0, "Empty enumerable has 0 elements")
        self.assertEqual(len(simple_list), 3, "Simple enumerable has 3 elements")
        self.assertEqual(len(complex_list), 3, "Complex enumerable has 3 elements")

    def test_sum(self):
        self.assertEqual(self.empty.sum(), 0, "Sum of empty enumerable should be 0")
        self.assertEqual(self.simple.sum(), 6, "Sum of simple enumerable should be 6")
        self.assertEqual(self.complex.sum(lambda x: x['value']), 6, "Sum of complex enumerable should be 6")

    def test_count(self):
        self.assertEqual(self.empty.count(), 0, "Empty enumerable has 0 elements")
        self.assertEqual(self.simple.count(), 3, "Simple enumerable has 3 elements")
        self.assertEqual(self.complex.count(), 3, "Complex enumerable has 3 elements")

    def test_select(self):
        self.assertEqual(self.empty.select(lambda x: x['value']).count(), 0, "Empty enumerable should still have 0 elements")

        self.assertRaises(NullArgumentError, self.simple.select, None)
        simple_select = self.simple.select(lambda x: { 'value' : x }).to_list()
        first_simple = simple_select[0]
        simple_count = len(simple_select)
        self.assertIsInstance(first_simple, dict, "Transformed simple enumerable element is dictionary")
        self.assertEqual(simple_count, 3, "Transformed simple enumerable has 3 elements")


        complex_select = self.complex.select(lambda x: x['value']).to_list()
        first_complex = complex_select[0]
        complex_count = len(complex_select)
        self.assertEqual(complex_count, 3, "Transformed complex enumerable has 3 elements")
        self.assertIsInstance(first_complex, int, "Transformed complex enumerable element is integer")

    def test_max_min(self):
        self.assertRaises(NoElementsError, self.empty.min)
        self.assertEqual(self.simple.min(), 1, "Minimum value of simple enumerable is 1")
        self.assertEqual(self.complex.min(lambda x: x['value']), 1, "Min value of complex enumerable is 1")

        self.assertRaises(NoElementsError, self.empty.max)
        self.assertEqual(self.simple.max(), 3, "Max value of simple enumerable is 3")
        self.assertEqual(self.complex.max(lambda x: x['value']), 3, "Max value of complex enumerable is 3")

    def test_avg(self):
        avg = float(2)
        self.assertRaises(NoElementsError, self.empty.avg)
        self.assertEqual(self.simple.avg(), avg, "Avg value of simple enumerable is {0:.5f}".format(avg))
        self.assertEqual(self.complex.avg(lambda x: x['value']), avg, "Avg value of complex enumerable is {0:.5f}".format(avg))

    def test_first_last(self):
        self.assertRaises(NoElementsError, self.empty.first)
        self.assertEqual(self.empty.first_or_default(), None, "First or default should be None")
        self.assertIsInstance(self.simple.first(), int, "First element in simple enumerable is int")
        self.assertEqual(self.simple.first(), 1, "First element in simple enumerable is 1")
        self.assertEqual(self.simple.first(), self.simple.first_or_default(), "First and first or default should equal")
        self.assertIsInstance(self.complex.first(), dict, "First element in complex enumerable is dict")
        self.assertDictEqual(self.complex.first(), {'value': 1}, "First element in complex enumerable is not correct dict")
        self.assertDictEqual(self.complex.first(), self.complex.first_or_default(), "First and first or default should equal")
        self.assertEqual(self.simple.first(), self.complex.select(lambda x: x['value']).first(), "First values in simple and complex should equal")


        self.assertRaises(NoElementsError, self.empty.last)
        self.assertEqual(self.empty.last_or_default(), None, "Last or default should be None")
        self.assertIsInstance(self.simple.last(), int, "Last element in simple enumerable is int")
        self.assertEqual(self.simple.last(), 3, "Last element in simple enumerable is 3")
        self.assertEqual(self.simple.last(), self.simple.last_or_default(), "Last and last or default should equal")
        self.assertIsInstance(self.complex.last(), dict, "Last element in complex enumerable is dict")
        self.assertDictEqual(self.complex.last(), {'value': 3}, "Last element in complex enumerable is not correct dict")
        self.assertDictEqual(self.complex.last(), self.complex.last_or_default(), "Last and last or default should equal")
        self.assertEqual(self.simple.last(), self.complex.select(lambda x: x['value']).last(), "Last values in simple and complex should equal")

    def test_sort(self):
        self.assertRaises(NullArgumentError, self.simple.order_by, None)
        self.assertRaises(NullArgumentError, self.simple.order_by_descending, None)

        self.assertListEqual(self.simple.order_by(lambda x: x).to_list(), self.simple.to_list(), "Simple enumerable sort ascending should yield same list")
        self.assertListEqual(self.simple.order_by_descending(lambda x: x).to_list(), sorted(self.simple, key=lambda x: x, reverse=True), "Simple enumerable sort descending should yield reverse list")

        self.assertListEqual(self.complex.order_by(lambda x: x['value']).to_list(), self.complex.to_list(), "Complex enumerable sort ascending should yield same list")
        self.assertListEqual(self.complex.order_by_descending(lambda x: x['value']).to_list(), sorted(self.complex, key=lambda x: x['value'], reverse=True), "Complex enumerable sort descending should yield reverse list")

        self.assertListEqual(self.simple.order_by(lambda x: x).to_list(), self.complex.select(lambda x: x['value']).order_by(lambda x: x).to_list(), "Projection and sort ascending of complex should yield simple")

    def test_median(self):
        self.assertRaises(NoElementsError, self.empty.median)

        median = float(2)
        self.assertEqual(self.simple.median(), median, "Median of simple enumerable should be {0:.5f}".format(median))
        self.assertEqual(self.complex.median(lambda x: x['value']), median, "Median of complex enumerable should be {0:.5f}".format(median))

    def test_skip_take(self):
        self.assertListEqual(self.empty.skip(2).to_list(), [], "Skip 2 of empty list should yield empty list")
        self.assertListEqual(self.empty.take(2).to_list(), [], "Take 2 of empty list should yield empty list")

        self.assertEqual(self.simple.skip(1).take(1).first(), 2, "Skip 1 and take 1 of simple should yield 2")
        self.assertDictEqual(self.complex.select(lambda x: x['value']).skip(1).take(1).first(), 2, "Skip 1 and take 1 of complex with projection should yield 2")


