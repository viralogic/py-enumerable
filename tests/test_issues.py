from unittest import TestCase
from py_linq import Enumerable


class IssueTests(TestCase):

    def test_issue19(self):
        foo = Enumerable([1])
        bar = Enumerable([1])
        self.assertEqual(foo.intersect(bar).count(), 1)

        foo = Enumerable([1])
        bar = Enumerable([1]).distinct()
        self.assertEqual(foo.intersect(bar).count(), 1)
