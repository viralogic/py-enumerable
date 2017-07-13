__version__ = '0.4.0'

try:
    from py_linq import Enumerable  # noqa
except ImportError:
    from py_linq.py_linq import Enumerable3 as Enumerable  # noqa
