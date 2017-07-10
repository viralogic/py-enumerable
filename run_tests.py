__author__ = 'Bruce Fenske'

import unittest

testclasses = [
    'tests.test_constructor',
    'tests.test_functions'
]
suite = unittest.TestLoader().loadTestsFromNames(testclasses)
unittest.TextTestRunner(verbosity=2).run(suite)
