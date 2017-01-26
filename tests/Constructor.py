__author__ = 'Bruce Fenske'

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
