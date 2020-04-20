import unittest
import logging
import time
from py_linq import Enumerable

class GeneratorPerformanceTests(unittest.TestCase):
    def setUp(self):
        self.test_generator = ({ "id": x, "value": x } for x in range(0, 80000))
        self.num_experiments = 100
        self.logger = logging.getLogger(__name__)

    def test_constructor(self):
        tic = time.perf_counter()
        for i in range(0, self.num_experiments):
            e = Enumerable(self.test_generator)
        toc = time.perf_counter()
        py_linq_time = (toc - tic) / self.num_experiments
        self.logger.info(f"py_linq constructor time = {py_linq_time:0.6f}")
        self.assertTrue(py_linq_time < 0.035)

    def test_select(self):
        tic = time.perf_counter()
        for i in range(0, self.num_experiments):
             e = Enumerable(self.test_generator).select(lambda b: {'id': b['id']})
        toc = time.perf_counter()
        py_linq_time = (toc - tic) / self.num_experiments
        self.logger.info(f"py_linq select time = {py_linq_time:0.6f}")
        self.assertTrue(py_linq_time < 0.0035)

    def test_to_list(self):
        num_experiments = 10
        tic = time.perf_counter()
        for i in range(0, num_experiments):
            e = Enumerable(({ "id": x, "value": x } for x in range(0, 80000))) \
                .select(lambda b: {'id': b['id']}) \
                .to_list()
        toc = time.perf_counter()
        py_linq_time = (toc - tic) / num_experiments
        self.logger.info(f"py_linq to_list time = {py_linq_time:0.6f}")

        tic = time.perf_counter()
        for i in range(0, num_experiments):
            l = list(map(
                lambda b: {'id': b['id']},
                ({ "id": x, "value": x } for x in range(0, 80000))
            ))
        toc = time.perf_counter()
        python_list_time = (toc - tic) / num_experiments
        self.logger.info(f"python_list_time = {python_list_time:0.6f}")

        tic = time.perf_counter()
        for i in range(0, num_experiments):
            l = [i for i in map(lambda b: { 'id': b['id']}, ({ "id":x, "value": x } for x in range(0, 80000)))]
        toc = time.perf_counter()
        python_list_comp_time = (toc -tic) / num_experiments
        self.logger.info(f"python_list_comp_time = {python_list_comp_time:0.6f}")

        self.assertTrue(py_linq_time < python_list_comp_time * 10)
        