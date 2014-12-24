__author__ = 'ViraLogic Software'

from unittest import TestCase
from py_linq import Enumerable
from tests import _empty, _simple, _complex

class TestConstructor(TestCase):
    def setUp(self):
        self.empty = Enumerable(_empty)
        self.simple = Enumerable(_simple)
        self.complex = Enumerable(_complex)

    def test_constructor(self):
        self.assertIsInstance(self.empty, Enumerable, "TypeError: empty py_linq is not Enumerable type")
        self.assertIsInstance(self.simple, Enumerable, "TypeError: simple py_linq is not Enumerable type")
        self.assertIsInstance(self.complex, Enumerable, "TypeError: complex py_linq is not Enumerable type")

        self.assertRaises(TypeError, Enumerable, 1)

    def test_data(self):
        self.assertEqual(self._get_count(Enumerable()), 0, "Void constructor has 0 elements")
        self.assertEqual(self._get_count(self.empty), 0, "Length of empty data should be 0")
        self.assertEqual(self._get_count(self.simple), 3, "Length of simple data should be 3")
        self.assertEqual(self._get_count(self.complex), 3, "Length of complex data should be 3")

    def test_indexer(self):
        with self.assertRaises(IndexError):
            second = self.empty[0]

        self.assertIsInstance(self.simple[1], int, "TypeError: simple enumerable contains only integers")
        self.assertIsInstance(self.complex[2], dict, "TypeError: complex enumerable contains only dicts")

    def _get_count(self, iterable):
        count = 0
        for el in iterable:
            count += 1
        return count