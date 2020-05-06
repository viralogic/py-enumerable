""" Linq for Python """

__version__ = "1.2.3"

try:
    from py_linq import Enumerable
except ImportError:
    from py_linq.py_linq import Enumerable
