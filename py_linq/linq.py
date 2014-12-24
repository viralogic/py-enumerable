__author__ = 'ViraLogic Software'

import itertools

class Enumerable(object):
    def __init__(self, data=[]):
        """
        Constructor
        :param data: iterable object
        :return: None
        """
        if not hasattr(data, "__iter__"):
            raise TypeError("Enumerable must be instantiated with an iterable object")
        self._data = iter(data) if not hasattr(data, "__next__") or not hasattr(data, "next") else data

    def __iter__(self):
        return self._data

    def __next__(self):
        """
        For Python 3 compatibility
        :yield: The next object in the iterator
        """
        yield self.next()

    def next(self):
        """
        Gets the next object in iterator
        :return: Next object in iterator
        """
        yield self._data.next()

    def __getitem__(self, item):
        """
        Indexer into data
        :param item: integer object as index value
        :return: item at specified index if within bounds, else raises error
        """
        return self.to_list().__getitem__(item)

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
        return sum(self.select(lambda x: 1))

    def select(self, func):
        """
        Transforms data into different form
        :param func: lambda expression on how to perform transformation
        :return: new Enumerable object containing transformed elements
        """
        return Enumerable(itertools.imap(func, self))




