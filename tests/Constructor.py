__author__ = 'ViraLogic Software'

from unittest import TestCase
from enumerable import Enumerable

class TestConstructor(TestCase):
    _empty = []
    _simple = [1, 2, 3]
    _complex = [
        {
            'value': 1
        },
        {
            'value': 2
        },
        {
            'value': 3
        }
    ]
    def setUp(self):
        self.empty = Enumerable(self._empty)
        self.simple = Enumerable(self._simple)
        self.complex = Enumerable(self._complex)

    def test_constructor(self):
        self.assertEqual(type(self.empty._data), iter(self._empty))
        self.assertEqual(type(self.simple._data), iter(self._simple))
        self.assertEqual(type(self.complex._data), iter(self._complex))

    def test_data(self):
        self.assertE