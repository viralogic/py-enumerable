import unittest
import logging
import time
from py_linq import Enumerable


class GeneratorPerformanceTests(unittest.TestCase):
    def setUp(self):
        self.test_generator = ({"id": x, "value": x} for x in range(0, 80000))
        self.num_experiments = 100
        self.logger = logging.getLogger(__name__)

    def test_constructor(self):
        tic = time.clock()
        for i in range(0, self.num_experiments):
            e = Enumerable(self.test_generator)
        toc = time.clock()
        py_linq_time = (toc - tic) / self.num_experiments
        self.assertTrue(py_linq_time < 0.035)

    def test_select(self):
        tic = time.clock()
        for i in range(0, self.num_experiments):
            e = Enumerable(self.test_generator).select(lambda b: {"id": b["id"]})
        toc = time.clock()
        py_linq_time = (toc - tic) / self.num_experiments
        self.assertTrue(py_linq_time < 0.0035)

    def test_to_list(self):
        num_experiments = 10
        tic = time.clock()
        for i in range(0, num_experiments):
            e = (
                Enumerable(({"id": x, "value": x} for x in range(0, 80000)))
                .select(lambda b: {"id": b["id"]})
                .to_list()
            )
        toc = time.clock()
        py_linq_time = (toc - tic) / num_experiments

        tic = time.clock()
        for i in range(0, num_experiments):
            l = list(
                map(
                    lambda b: {"id": b["id"]},
                    ({"id": x, "value": x} for x in range(0, 80000)),
                )
            )
        toc = time.clock()
        python_list_time = (toc - tic) / num_experiments

        tic = time.clock()
        for i in range(0, num_experiments):
            l = [
                i
                for i in map(
                    lambda b: {"id": b["id"]},
                    ({"id": x, "value": x} for x in range(0, 80000)),
                )
            ]
        toc = time.clock()
        python_list_comp_time = (toc - tic) / num_experiments

        self.assertTrue(py_linq_time < python_list_comp_time * 10)
