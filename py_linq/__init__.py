""" Linq for Python """

__version__ = "1.5.0"


try:
    from py_linq import Enumerable
except ImportError:
    from py_linq.py_linq import Enumerable
