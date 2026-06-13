import itertools
import io
from dataclasses import dataclass
from typing import (
    TypeVar,
    Any,
    Iterable,
    Optional,
)
from copy import deepcopy

TNode = TypeVar("TNode", bound="Node")


@dataclass
class Node(object):
    """
    Node for linked list
    """

    value: Any
    next: Optional[TNode] = None
    prev: Optional[TNode] = None


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


class RepeatableIterable(object):
    def __init__(self, data: Iterable[Any] = None):
        """
        Constructor. Pretty straight forward except for the is_generator check. This is so we
        can detect when a function that generates data is passed as a datasource. In this case we
        need to exhaust the values in the function generator
        """
        if data is None:
            data = []
        if not hasattr(data, "__iter__"):
            raise TypeError(
                u"RepeatableIterable must be instantiated with an iterable object"
            )
        self._data: Iterable[Any] = data
        self._len = None
        self._root: TNode = None
        self._current: TNode = None
        self._tail: TNode = None

    def __len__(self):
        if self._len is None:
            self._len = sum(1 for item in iter(self))
        return self._len

    def __reversed__(self) -> Any:
        if self._root is None:
            prev_node = None
            for i, item in enumerate(self._data):
                node = Node(value=item, prev=prev_node)
                if i == 0:
                    self._root = node
                else:
                    prev_node.next = node
                prev_node = node
            self._tail = prev_node
            self._len = i + 1 if prev_node else 0
            self._current = self._root
        tail = self._tail
        if tail is None and self._root is not None:
            cur = self._root
            while cur.next is not None:
                cur = cur.next
            tail = cur
        current = tail
        while current is not None:
            yield current.value
            current = current.prev

    def __iter__(self) -> Any:
        if self._root is not None and self._len is None and not hasattr(self._data, '__next__'):
            self._root = None
            self._current = None
            self._tail = None
            self._len = None
        if self._root is None:
            i = 0
            prev_node = None
            for index, item in enumerate(self._data):
                node = Node(value=item, prev=prev_node)
                if index == 0:
                    self._root = node
                else:
                    prev_node.next = node
                yield node.value
                prev_node = node
                i += 1
            self._tail = prev_node
            self._len = i
        else:
            self._current = self._root
            last_node = None
            i = 0
            while self._current is not None:
                yield self._current.value
                last_node = self._current
                self._current = self._current.next
                i += 1
            if self._len is None:
                prev_node = last_node
                for item in self._data:
                    node = Node(value=item, prev=prev_node)
                    prev_node.next = node
                    yield node.value
                    prev_node = node
                    i += 1
                self._tail = prev_node
                self._len = i
        self._current = self._root

    def __next__(self):
        if self._current.next is None:
            self._current = self._root
            raise StopIteration
        self._current = self._current.next
        return self._current.value

    @property
    def current(self) -> Optional[TNode]:
        return self._current

    @current.setter
    def current(self, node: TNode) -> None:
        self._current = node

    @property
    def head(self) -> Optional[TNode]:
        return self._root

    @head.setter
    def head(self, node: TNode) -> None:
        self._root = node

    def next(self):
        return self.__next__()
