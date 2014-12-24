__author__ = 'Viralogic Software'

from unittest import TestCase
from py_linq import Enumerable
from tests import _empty, _simple, _complex


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

    def test_count(self):
        self.assertEqual(self.empty.count(), 0, "Empty enumerable has 0 elements")
        self.assertEqual(self.simple.count(), 3, "Simple enumerable has 3 elements")
        self.assertEqual(self.complex.count(), 3, "Complex enumerable has 3 elements")

    def test_select(self):
        self.assertEqual(self.empty.select(lambda x: x['value']).count(), 0, "Empty enumerable should still have 0 elements")

        simple_select = self.simple.select(lambda x: { 'value' : x })
        first_simple = simple_select[0]
        simple_count = simple_select.count()
        self.assertEqual(simple_count, 3, "Transformed simple enumerable has 3 elements")
        self.assertIsInstance(first_simple, dict, "Transformed simple enumerable element is dictionary")

        complex_select = self.complex.select(lambda x: x['value'])
        first_complex = complex_select[0]
        complex_count = complex_select.count()
        self.assertEqual(complex_count, 3, "Transformed complex enumerable has 3 elements")
        self.assertIsInstance(first_complex, int, "Transformed complex enumerable element is integer")

        self.assertDictEqual(self.complex[0], first_simple, "First element in complex enumerable should match first element of simple transformed")
        self.assertEqual(self.simple[0], first_complex, "First element in simple enumerable should match first element of complex transformed")
