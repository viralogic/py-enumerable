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
