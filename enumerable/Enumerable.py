__author__ = 'ViraLogic Software'

class Enumerable(object):
    def __init__(self, data):
        """
        Constructor
        :param data: iterable object
        :return: None
        """
        self._data = iter(data)

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




