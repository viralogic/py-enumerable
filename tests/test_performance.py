import unittest
import logging
try:
    from time import clock as clock
except ImportError:
    from time import perf_counter as clock
import time
from py_linq import Enumerable


class GeneratorPerformanceTests(unittest.TestCase):
    def setUp(self):
        self.test_generator = ({"id": x, "value": x} for x in range(0, 80000))
        self.num_experiments = 100
        self.logger = logging.getLogger(__name__)

    def test_constructor(self):
        tic = clock()
        for i in range(0, self.num_experiments):
            e = Enumerable(self.test_generator)
        toc = clock()
        py_linq_time = (toc - tic) / self.num_experiments
        self.assertTrue(py_linq_time < 0.035)

    def test_select(self):
        tic = clock()
        for i in range(0, self.num_experiments):
            e = Enumerable(self.test_generator).select(lambda b: {"id": b["id"]})
        toc = clock()
        py_linq_time = (toc - tic) / self.num_experiments
        self.assertTrue(py_linq_time < 0.0035)

    def test_to_list(self):
        num_experiments = 10
        tic = clock()
        for i in range(0, num_experiments):
            e = (
                Enumerable(({"id": x, "value": x} for x in range(0, 80000)))
                .select(lambda b: {"id": b["id"]})
                .to_list()
            )
        toc = clock()
        py_linq_time = (toc - tic) / num_experiments

        tic = clock()
        for i in range(0, num_experiments):
            l = list(
                map(
                    lambda b: {"id": b["id"]},
                    ({"id": x, "value": x} for x in range(0, 80000)),
                )
            )
        toc = clock()
        python_list_time = (toc - tic) / num_experiments

        tic = clock()
        for i in range(0, num_experiments):
            l = [
                i
                for i in map(
                    lambda b: {"id": b["id"]},
                    ({"id": x, "value": x} for x in range(0, 80000)),
                )
            ]
        toc = clock()
        python_list_comp_time = (toc - tic) / num_experiments

        self.assertTrue(py_linq_time < python_list_comp_time * 10)
