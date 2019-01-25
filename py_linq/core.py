class Key(object):
    def __init__(self, key, **kwargs):
        """
        Constructor for Key class. Autogenerates key properties in object
        given dict or kwargs
        :param key: dict of name-values
        :param kwargs: optional keyword arguments
        :return: void
        """
        key = key if key is not None else kwargs
        self.__dict__.update(key)

    def __repr__(self):
        return self.__dict__.__repr__()


class OrderingDirection(object):
    def __init__(self, key, reverse):
        """
        A container to hold the lambda key and sorting direction
        :param key: lambda function
        :param reverse: boolean. True for reverse sort
        """
        self.key = key
        self.descending = reverse
