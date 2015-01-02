__author__ = 'ViraLogic Software'

import itertools
from exceptions import *

class Enumerable(object):
    def __init__(self, data=[]):
        """
        Constructor
        :param data: iterable object
        :return: None
        """
        if not hasattr(data, "__iter__"):
            raise TypeError("Enumerable must be instantiated with an iterable object")
        self._data = data

    def __iter__(self):
        for element in self._data.__iter__():
            yield element

    def to_list(self):
        """
        Converts the iterable into a list
        :return: list object
        """
        return list(element for element in self)

    def count(self):
        """
        Returns the number of elements in iterable
        :return: integer object
        """
        return sum(1 for element in self)

    def select(self, func):
        """
        Transforms data into different form
        :param func: lambda expression on how to perform transformation
        :return: new Enumerable object containing transformed data
        """
        if func is None:
            raise NullArgumentError("Func cannot be None")
        return Enumerable(itertools.imap(func, self))

    def sum(self, func=lambda x: x):
        """
        Returns the sum of af data elements
        :param func: lambda expression to transform data
        :return: sum of selected elements
        """
        return sum(self.select(func))

    def min(self, func=lambda x: x):
        """
        Returns the min value of data elements
        :param func: lambda expression to transform data
        :return: minimum value
        """
        if self.count() == 0:
            raise NoElementsError("Iterable contains no elements")
        return min(self.select(func))

    def max(self, func=lambda x: x):
        """
        Returns the max value of data elements
        :param func: lambda expression to transform data
        :return: maximum value
        """
        if self.count() == 0:
            raise NoElementsError("Iterable contains no elements")
        return max(self.select(func))

    def avg(self, func=lambda x: x):
        """
        Returns the average value of data elements
        :param func: lambda expression to transform data
        :return: average value as float object
        """
        count = self.count()
        if count == 0:
            raise NoElementsError("Iterable contains no elements")
        return float(self.sum(func))/float(count)

    def median(self, func=lambda x: x):
        """
        Return the median value of data elements
        :param func: lambda expression to project and sort data
        :return: median value
        """
        if self.count() == 0:
            raise NoElementsError("Iterable contains no elements")
        result = self.order_by(func).select(func).to_list()
        length = len(result)
        i = int(length / 2)
        return result[i] if length % 2 == 1 else (float(result[i - 1]) + float(result[i]))/ float(2)

    def first(self):
        """
        Returns the first element
        :param func: lambda expression to transform data
        :return: data element as object or NoElementsError if transformed data contains no elements
        """
        if self.count() == 0:
            raise NoElementsError("Iterable contains no elements")
        first = Enumerable(itertools.islice(self, 0, 1, 1)).to_list()
        return first[0]

    def first_or_default(self):
        """
        Return the first element
        :param func: lambda expression to transform data
        :return: data element as object or None if transformed data contains no elements
        """
        try:
            return self.first()
        except NoElementsError:
            return None

    def last(self):
        """
        Return the last element
        :param func: lambda expression to transform data
        :return: data element as object or NoElementsError if transformed data contains no elements
        """
        count = self.count()
        if count == 0:
            raise NoElementsError("Iterable contains no elements")
        return Enumerable(itertools.islice(self, count-1, None, 1)).to_list()[0]

    def last_or_default(self):
        """
        Return the last element
        :param func: lambda expression to transform data
        :return: data element as object or None if transformed data contains no elements
        """
        try:
            return self.last()
        except NoElementsError:
            return None

    def order_by(self, key):
        """
        Returns new Enumerable sorted in ascending order by given key
        :param key: key to sort by as lambda expression
        :return: new Enumerable object
        """
        if key is None:
            raise NullArgumentError("No key for sorting given")
        return Enumerable(sorted(self, key=key))

    def order_by_descending(self, key):
        """
        Returns new Enumerable sorted in descending order by given key
        :param key: key to sort by as lambda expression
        :return: new Enumerable object
        """
        if key is None:
            raise NullArgumentError("No key for sorting given")
        return Enumerable(sorted(self, key=key, reverse=True))

    def skip(self, n):
        """
        Returns new Enumerable where n elements have been skipped
        :param n: Number of elements to skip as int
        :return: new Enumerable object
        """
        return Enumerable(itertools.islice(self, n, None, 1))

    def take(self, n):
        """
        Return new Enumerable where first n elements are taken
        :param n: Number of elements to take
        :return: new Enumerable object
        """
        return Enumerable(itertools.islice(self, 0, n, 1))


