__author__ = 'Bruce Fenske'

import unittest

testclasses = [
    'tests.Constructor',
    'tests.Functions'
]
suite = unittest.TestLoader().loadTestsFromNames(testclasses)
unittest.TextTestRunner(verbosity=2).run(suite)
