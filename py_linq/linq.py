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
        return len(self.to_list())

    def select(self, func):
        """
        Transforms data into different form
        :param func: lambda expression on how to perform transformation
        :return: new Enumerable object containing transformed data
        """
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

    def first(self, func=lambda x: x):
        """
        Returns the first element
        :param func: lambda expression to transform data
        :return: data element as object or NoElementsError if transformed data contains no elements
        """
        result = self.select(func).to_list()
        if len(result) == 0:
            raise NoElementsError("Iterable contains no elements")
        return result[0]

    def first_or_default(self, func=lambda x: x):
        """
        Return the first element
        :param func: lambda expression to transform data
        :return: data element as object or None if transformed data contains no elements
        """
        try:
            return self.first(func)
        except NoElementsError:
            return None

    def last(self, func=lambda x: x):
        """
        Return the last element
        :param func: lambda expression to transform data
        :return: data element as object or NoElementsError if transformed data contains no elements
        """
        result = self.select(func).to_list()
        if len(result) == 0:
            raise NoElementsError("Iterable contains no elements")
        return result[len(result) - 1]

    def last_or_default(self, func=lambda x: x):
        """
        Return the last element
        :param func: lambda expression to transform data
        :return: data element as object or None if transformed data contains no elements
        """
        try:
            return self.last(func)
        except NoElementsError:
            return None
        


