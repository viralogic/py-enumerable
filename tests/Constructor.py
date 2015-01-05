__author__ = 'ViraLogic Software'

from unittest import TestCase
from py_linq import Enumerable
from py_linq.linq import Key
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

class TestKeyConstructor(TestCase):
    def setUp(self):
        self.complex_key = Key(id='value')
        self.complex_key_dict = Key({'id': 'value'})

    def test_constructor(self):
        self.assertRaises(KeyError, Key, {})

        for key in [self.complex_key, self.complex_key_dict]:
            self.assertTrue(hasattr(key, "id"), "Complex key should have 'id' attribute")
            self.assertEqual(key.id, "value", "Complex key.id attribute should have value of 'value'")