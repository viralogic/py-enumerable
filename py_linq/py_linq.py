from ast import Call
import itertools
import json
from typing import (
    List,
    Any,
    Iterable,
    TypeVar,
    Union,
    Dict,
    Optional,
    Callable,
)
from queue import LifoQueue
from six import string_types

# python 2 to 3 compatibility imports
try:
    from itertools import imap as map
    from itertools import ifilter as filter
    from itertools import izip as zip
except ImportError:
    pass
from builtins import range
from .core import Key, OrderingDirection, RepeatableIterable, Node
from .decorators import deprecated
from .exceptions import (
    NoElementsError,
    NoMatchingElement,
    NullArgumentError,
    MoreThanOneMatchingElement,
)


TEnumerable = TypeVar("TEnumerable", bound="Enumerable")
TGrouping = TypeVar("TGrouping", bound="Grouping")
TSortedEnumerable = TypeVar("TSortedEnumerable", bound="SortedEnumerable")
TGroupedEnumerable = TypeVar("TGroupedEnumerable", bound="GroupedEnumerable")
Number = Union[float, int]


class Enumerable(object):
    def __init__(self, data=None):
        """
        Constructor
        ** Note: no type checking of the data elements are performed during
         instantiation. **
        :param data: iterable object
        :return: None
        """
        self._iterable = RepeatableIterable(data)

    def __iter__(self) -> Iterable[Any]:
        return iter(self._iterable)

    def __reversed__(self) -> Iterable[Any]:
        return reversed(self._iterable)

    def next(self) -> Any:
        return next(self._iterable)

    def __next__(self) -> Any:
        return self.next()

    def __getitem__(self, n) -> Any:
        """
        Gets item in iterable at specified zero-based index
        :param n: the index of the item to get
        :returns the element at the specified index.
        :raises IndexError if n > number of elements in the iterable
        """
        for i, e in enumerate(self):
            if i == n:
                return e

    def __len__(self) -> int:
        """
        Gets the number of elements in the collection
        """
        return len(self._iterable)

    def __repr__(self) -> str:
        return list(self).__repr__()

    def to_list(self) -> List[Any]:
        """
        Converts the iterable into a list
        :return: list object
        """
        return [x for x in self]

    def count(self, predicate=None) -> int:
        """
        Returns the number of elements in iterable
        :return: integer object
        """
        if predicate is not None:
            return sum(1 for element in self.where(predicate))
        return sum(1 for element in self)

    def select(self, func=lambda x: x) -> TEnumerable:
        """
        Transforms data into different form
        :param func: lambda expression on how to perform transformation
        :return: new Enumerable object containing transformed data
        """
        return Enumerable(map(func, self))

    def sum(self, func=lambda x: x) -> Number:
        """
        Returns the sum of af data elements
        :param func: lambda expression to transform data
        :return: sum of selected elements
        """
        return sum(func(x) for x in self)

    def min(self, func=lambda x: x) -> Number:
        """
        Returns the min value of data elements
        :param func: lambda expression to transform data
        :return: minimum value
        """
        if len(self) == 0:
            raise NoElementsError(u"Iterable contains no elements")
        return func(min(self, key=func))

    def max(self, func=lambda x: x) -> Number:
        """
        Returns the max value of data elements
        :param func: lambda expression to transform data
        :return: maximum value
        """
        if len(self) == 0:
            raise NoElementsError(u"Iterable contains no elements")
        return func(max(self, key=func))

    def avg(self, func=lambda x: x) -> Number:
        """
        Returns the average value of data elements
        :param func: lambda expression to transform data
        :return: average value as float object
        """
        if len(self) == 0:
            raise NoElementsError(u"Iterable contains no elements")
        return float(self.sum(func)) / float(self.count())

    def median(self, func=lambda x: x) -> Number:
        """
        Return the median value of data elements
        :param func: lambda expression to project and sort data
        :return: median value
        """
        if len(self) == 0:
            raise NoElementsError(u"Iterable contains no elements")
        result = self.order_by(func).select(func).to_list()
        length = len(result)
        i = int(length / 2)
        return (
            result[i]
            if length % 2 == 1
            else (float(result[i - 1]) + float(result[i])) / float(2)
        )

    def element_at(self, n) -> Any:
        """
        Returns element at given index.
            * Raises IndexError if no element found at specified position
        :param n: index as int object
        :return: Element at given index
        """
        if not isinstance(n, int):
            raise TypeError("Must be an integer")
        result = self[n]
        if result is None:
            raise IndexError
        return result

    def element_at_or_default(self, n) -> Optional[Any]:
        """
        Returns element at given index or None if no element found
            * Raises IndexError if n is greater than the number of elements in
            enumerable
        :param n: index as int object
        :return: Element at given index
        """
        try:
            return self.element_at(n)
        except IndexError:
            return None

    def first(self, func=None) -> Any:
        """
        Returns the first element in a collection
        :func: predicate as lambda expression used to filter collection
        :return: data element as object or NoElementsError if transformed data
        contains no elements
        """
        if func is not None:
            return self.where(func).element_at(0)
        return self.element_at(0)

    def first_or_default(self, func=None) -> Optional[Any]:
        """
        Return the first element in a collection. If collection is empty, then returns None
        :func: predicate as lambda expression used to filter collection
        :return: data element as object or None if transformed data contains no
         elements
        """
        if func is not None:
            return self.where(func).element_at_or_default(0)
        return self.element_at_or_default(0)

    def last(self, func=None) -> Any:
        """
        Return the last element in a collection
        :func: predicate as a lambda expression used to filter collection
        :return: data element as object or NoElementsError if transformed data
        contains no elements
        """
        if func is not None:
            self.reverse().where(func).first()
        return self.reverse().first()

    def last_or_default(self, func=None) -> Optional[Any]:
        """
        Return the last element in a collection or None if the collection is empty
        :func: predicate as a lambda expression used to filter collection
        :return: data element as object or None if transformed data contains no
         elements
        """
        if func is not None:
            return self.reverse().where(func).first_or_default()
        return self.reverse().first_or_default()

    def order_by(self, key):
        """
        Returns new Enumerable sorted in ascending order by given key
        :param key: key to sort by as lambda expression
        :return: new Enumerable object
        """
        if key is None:
            raise NullArgumentError(u"No key for sorting given")
        kf = [OrderingDirection(key, reverse=False)]
        return SortedEnumerable(Enumerable(iter(self)), key_funcs=kf)

    def order_by_descending(self, key):
        """
        Returns new Enumerable sorted in descending order by given key
        :param key: key to sort by as lambda expression
        :return: new Enumerable object
        """
        if key is None:
            raise NullArgumentError(u"No key for sorting given")
        kf = [OrderingDirection(key, reverse=True)]
        return SortedEnumerable(Enumerable(iter(self)), key_funcs=kf)

    def skip(self, n) -> TEnumerable:
        """
        Returns new Enumerable where n elements have been skipped
        :param n: Number of elements to skip as int
        :return: new Enumerable object
        """
        return Enumerable(data=itertools.islice(self, n, None, 1))

    def take(self, n) -> TEnumerable:
        """
        Return new Enumerable where first n elements are taken
        :param n: Number of elements to take
        :return: new Enumerable object
        """
        return Enumerable(data=itertools.islice(self, 0, n, 1))

    def where(self, predicate) -> TEnumerable:
        """
        Returns new Enumerable where elements matching predicate are selected
        :param predicate: predicate as a lambda expression
        :return: new Enumerable object
        """
        if predicate is None:
            raise NullArgumentError("No predicate given for where clause")
        return Enumerable(filter(predicate, self))

    def single(self, predicate=None) -> Any:
        """
        Returns single element that matches given predicate.
        Raises:
            * NoMatchingElement error if no matching elements are found
            * MoreThanOneMatchingElement error if more than one matching
            element is found
        :param predicate: predicate as a lambda expression
        :return: Matching element as object
        """
        result = self.where(predicate) if predicate is not None else self
        if len(result) == 0:
            raise NoMatchingElement("No matching elements are found")
        if result.count() > 1:
            raise MoreThanOneMatchingElement("More than one matching element is found")
        return result.to_list()[0]

    def single_or_default(self, predicate=None) -> Optional[Any]:
        """
        Return single element that matches given predicate. If no matching
        element is found, returns None
        Raises:
            * MoreThanOneMatchingElement error if more than one matching
            element is found
        :param predicate: predicate as a lambda expression
        :return: Matching element as object or None if no matches are found
        """
        try:
            return self.single(predicate)
        except NoMatchingElement:
            return None

    def select_many(self, func=lambda x: x) -> TEnumerable:
        """
        Flattens an iterable of iterables returning a new Enumerable
        :param func: selector as lambda expression
        :return: new Enumerable object
        """
        selected = self.select(func)
        return Enumerable(data=itertools.chain.from_iterable(selected))

    def add(self, element) -> TEnumerable:
        """
        Adds an element to the enumerable.
        :param element: An element
        :return: new Enumerable object

        The behavior here is no longer in place to conform more to typical
        functional programming practices. This is a breaking change from
        1.X versions.
        """
        if element is None:
            return self
        return self.concat(Enumerable([element]))

    def concat(self, enumerable) -> TEnumerable:
        """
        Adds enumerable to an enumerable
        :param enumerable: An iterable object
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable argument must be an instance of Enumerable")
        return Enumerable(data=itertools.chain(self._iterable, enumerable._iterable))

    def group_by(
        self, key_names=[], key=lambda x: x, result_func=lambda x: x
    ) -> TEnumerable:
        """
        Groups an enumerable on given key selector. Index of key name
        corresponds to index of key lambda function.

        Usage:
            Enumerable([1,2,3]).group_by(key_names=['id'], key=lambda x: x) _
                .to_list() -->
                Enumerable object [
                    Grouping object {
                        key.id: 1,
                        _data: [1]
                    },
                    Grouping object {
                        key.id: 2,
                        _data: [2]
                    },
                    Grouping object {
                        key.id: 3,
                        _data: [3]
                    }
                ]
            Thus the key names for each grouping object can be referenced
            through the key property. Using the above example:

            Enumerable([1,2,3]).group_by(key_names=['id'], key=lambda x: x) _
            .select(lambda g: { 'key': g.key.id, 'count': g.count() }

        :param key_names: list of key names
        :param key: key selector as lambda expression
        :param result_func: transformation function as lambda expression
        :return: Enumerable of grouping objects
        """
        return GroupedEnumerable(self, key, key_names, result_func)

    def distinct(self, key=lambda x: x) -> TEnumerable:
        """
        Returns enumerable containing elements that are distinct based on
        given key selector
        :param key: key selector as lambda expression
        :return: new Enumerable object
        """
        return GroupedEnumerable(self, key, ["distinct"], lambda g: g.first())

    def join(
        self,
        inner_enumerable,
        outer_key=lambda x: x,
        inner_key=lambda x: x,
        result_func=lambda x: x,
    ):
        """
        Return enumerable of inner equi-join between two enumerables
        :param inner_enumerable: inner enumerable to join to self
        :param outer_key: key selector of outer enumerable as lambda expression
        :param inner_key: key selector of inner enumerable as lambda expression
        :param result_func: lambda expression to transform result of join
        :return: new Enumerable object
        """
        if not isinstance(inner_enumerable, Enumerable):
            raise TypeError(
                u"inner_enumerable parameter must be an instance of Enumerable"
            )
        return (
            Enumerable(data=itertools.product(self, inner_enumerable))
            .where(lambda r: outer_key(r[0]) == inner_key(r[1]))
            .select(lambda r: result_func(r))
        )

    def default_if_empty(self, value=None):
        """
        Returns an enumerable containing a single None element if enumerable is
        empty, otherwise the enumerable itself
        :return: an Enumerable object
        """
        if len(self) == 0:
            return Enumerable([value])
        return self

    def group_join(
        self,
        inner_enumerable: TEnumerable,
        outer_key: Callable = lambda x: x,
        inner_key: Callable = lambda x: x,
        result_func: Callable = lambda x: x,
    ):
        """
        Return enumerable of group join between two enumerables
        :param inner_enumerable: inner enumerable to join to self
        :param outer_key: key selector of outer enumerable as lambda expression
        :param inner_key: key selector of inner enumerable as lambda expression
        :param result_func: lambda expression to transform the result of group
        join
        :return: new Enumerable object
        """
        if not isinstance(inner_enumerable, Enumerable):
            raise TypeError(
                u"inner enumerable parameter must be an instance of Enumerable"
            )
        group_joined = self.join(
            inner_enumerable=inner_enumerable.group_by(key_names=["id"], key=inner_key),
            outer_key=outer_key,
            inner_key=lambda g: g.key.id,
            result_func=lambda gj: (gj[0], Enumerable(gj[1]._iterable)),
        ).select(result_func)
        return group_joined

    def any(self, predicate: Callable = None):
        """
        Returns true if any elements that satisfy predicate are found
        :param predicate: condition to satisfy as lambda expression
        :return: boolean True or False
        """
        return self.first_or_default(predicate) is not None

    def intersect(self, enumerable: TEnumerable, key: Callable):
        """
        Returns enumerable that is the intersection between given enumerable
        and self
        :param enumerable: enumerable object
        :param key: key selector as lambda expression
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable parameter must be an instance of Enumerable")
        membership = set((key(j) for j in enumerable))
        intrsct = (i for i in self if key(i) in membership)
        return Enumerable(data=intrsct).distinct(key)

    def aggregate(self, func: Callable, seed: Any = None) -> Any:
        """
        Perform a calculation over a given enumerable using the initial seed
        value
        :param func: calculation to perform over every the enumerable.
        This function will ingest (aggregate_result, next element) as parameters
        :param seed: initial seed value for the calculation. If None, then the
        first element is used as the seed
        :return: result of the calculation
        """
        result = seed
        for i, e in enumerate(self):
            if i == 0 and seed is None:
                result = e
                continue
            result = func(result, e)
        return result

    def union(self, enumerable: TEnumerable, key: Callable):
        """
        Returns enumerable that is a union of elements between self and given
        enumerable
        :param enumerable: enumerable to union self to
        :param key: key selector used to determine uniqueness
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable parameter must be an instance of Enumerable")
        return Enumerable(data=self.concat(enumerable)).distinct(key)

    def except_(self, enumerable: TEnumerable, key: Callable):
        """
        Returns enumerable that subtracts given enumerable elements from self
        :param enumerable: enumerable object
        :param key: key selector as lambda expression
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable parameter must be an instance of Enumerable")
        membership = set((key(j) for j in enumerable))
        exc = (i for i in self if key(i) not in membership)
        return Enumerable(data=exc).distinct(key)

    def contains(self, element, key=lambda x: x):
        """
        Returns True if element is found in enumerable, otherwise False
        :param element: the element being tested for membership in enumerable
        :param key: key selector to use for membership comparison
        :return: boolean True or False
        """
        return self.select(key).any(lambda x: x == key(element))

    def all(self, predicate: Callable) -> bool:
        """
        Determines whether all elements in an enumerable satisfy the given
        predicate
        :param predicate: the condition to test each element as lambda function
        :return: boolean True or False
        """
        return all(predicate(e) for e in self)

    def append(self, element):
        """
        Appends an element to the end of an enumerable
        :param element: the element to append to the enumerable
        :return: Enumerable object with appended element
        """
        return self.concat(Enumerable([element]))

    def prepend(self, element):
        """
        Prepends an element to the beginning of an enumerable
        :param element: the element to prepend to the enumerable
        :return: Enumerable object with the prepended element
        """
        return Enumerable([element]).concat(self)

    @staticmethod
    def empty():
        """
        Returns an empty enumerable
        :return: Enumerable object that contains no elements
        """
        return Enumerable()

    @staticmethod
    def range(start, length):
        """
        Generates a sequence of integers starting from start with length of length
        :param start: the starting value of the sequence
        :param length: the number of integers in the sequence
        :return: Enumerable of the generated sequence
        """
        return Enumerable(range(start, start + length, 1))

    @staticmethod
    def repeat(element, length):
        """
        Generates an enumerable containing an element repeated length times
        :param element: the element to repeat
        :param length: the number of times to repeat the element
        :return: Enumerable of the repeated elements
        """
        return Enumerable(data=itertools.repeat(element, length))

    def reverse(self):
        """
        Inverts the order of the elements in a sequence
        :return: Enumerable with elements in reversed order
        """
        return Enumerable(data=reversed(self))

    def skip_last(self, n):
        """
        Skips the last n elements in a sequence
        :param n: the number of elements to skip
        :return: Enumerable with n last elements removed
        """
        return self.take(self.count() - n)

    def skip_while(self, predicate):
        """
        Bypasses elements in a sequence while the predicate is True. After predicate fails
        remaining elements in sequence are returned
        :param predicate: a predicate as a lambda expression
        :return: Enumerable
        """
        return SkipWhileEnumerable(Enumerable(iter(self)), predicate)

    def take_last(self, n):
        """
        Takes the last n elements in a sequence
        :param n: the number of elements to take
        :return: Enumerable containing last n elements
        """
        return self.skip(self.count() - n)

    def take_while(self, predicate):
        """
        Includes elements in a sequence while the predicate is True. After predicate fails
        remaining elements in a sequence are removed
        :param predicate: a predicate as a lambda expression
        :return: Enumerable
        """
        return TakeWhileEnumerable(Enumerable(iter(self)), predicate)

    def to_dictionary(self, key=lambda x: x, value=lambda x: x):
        """
        Converts the enumerable into a dictionary
        :param key: key selector to use to create dictionary keys
        :param value: optional value selector to use to assign values to dictionary keys
        :return: dict
        """
        result = {}
        for i, e in enumerate(self):
            result[key(e)] = value(e)
        return result

    def zip(self, enumerable, func=lambda x: x):
        """
        Merges 2 Enumerables using the given function. If the 2 collections are of unequal length, then
        merging continues until the end of one of the collections is reached
        :param enumerable: Enumerable collection to merge with
        :param func: a function to perform the merging
        :return: Enumerable
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError()
        return ZipEnumerable(Enumerable(iter(self)), enumerable, func)


class SkipWhileEnumerable(Enumerable):
    """
    Class to hold state for skipping elements while a given predicate is true
    """

    def __init__(self, enumerable, predicate):
        super(SkipWhileEnumerable, self).__init__(enumerable)
        self.predicate = predicate

    def __iter__(self):
        return itertools.dropwhile(self.predicate, self._iterable)


class TakeEnumerable(Enumerable):
    """
    Class to hold state for taking subset of consecutive elements in a collection
    """

    def __init__(self, enumerable, n):
        super(TakeEnumerable, self).__init__(enumerable)
        self.n = n

    def __iter__(self):
        for index, element in enumerate(self._iterable):
            if index < self.n:
                yield element


class TakeWhileEnumerable(Enumerable):
    """
    Class to hold state for taking elements while a given predicate is true
    """

    def __init__(self, enumerable, predicate):
        super(TakeWhileEnumerable, self).__init__(enumerable)
        self.predicate = predicate

    def __iter__(self):
        return itertools.takewhile(self.predicate, self._iterable)


class GroupedEnumerable(Enumerable):
    def __init__(
        self,
        data: Iterable,
        key: Callable,
        key_names: List[Dict],
        func: Callable = lambda x: x,
    ) -> None:
        """
        Constructor for GroupedEnumerable class
        :param data: Iterable of grouped data obtained by itertools.groupby. The data structure is
            (key, grouper) where grouper is an iterable of items that match the key
        :param key: function to get the key
        :param key_names: list of names to use for the keys
        :param func: function to transform the Grouping result.
        """
        self._iterable = GroupedRepeatableIterable(key, key_names, func, data)


class Grouping(Enumerable):
    def __init__(self, key, data):
        """
        Constructor of Grouping class used for group by operations of
        Enumerable class
        :param key: Key instance
        :param data: iterable object
        :return: void
        """
        if not isinstance(key, Key):
            raise Exception("key argument should be a Key instance")
        self.key = key
        super(Grouping, self).__init__(data)

    def __repr__(self):
        return {
            "key": self.key.__repr__(),
            "enumerable": list(self._iterable).__repr__(),
        }.__repr__()


class GroupedRepeatableIterable(RepeatableIterable):
    def __init__(
        self,
        key: Callable,
        key_names: List[Dict],
        func: Callable,
        data: Iterable[Any] = None,
    ):
        self.key = key
        self.key_names = key_names
        self.func = func
        super().__init__(data)

    def _can_enumerate(self, key_value):
        return (
            hasattr(key_value, "__len__")
            and len(key_value) > 0
            and not isinstance(key_value, string_types)
        )

    def __iter__(self) -> Any:
        if self._root is None:
            grouped_iterable = (
                (k, list(g))
                for k, g in itertools.groupby(
                    sorted(self._data, key=self.key), self.key
                )
            )
            i = 0
            for key, group in grouped_iterable:
                key_prop = {}
                for j, prop in enumerate(self.key_names):
                    key_prop.setdefault(
                        prop, key[j] if self._can_enumerate(key) else key
                    )
                key_object = Key(key_prop)
                node = Node(value=self.func(Grouping(key_object, list(group))))
                if i == 0:
                    self._root = node
                    self._current = self._root
                else:
                    self._current.next = node
                    self._current = self._current.next
                yield node.value
                i += 1
            self._len = i
        else:
            while self._current is not None:
                yield self._current.value
                self._current = self._current.next
        self._current = self._root


class SortedEnumerable(Enumerable):
    def __init__(self, data: Iterable, key_funcs):
        """
        Constructor
        :param key_funcs: list of OrderingDirection instances in order of primary key --> less important keys
        :param data: data as iterable
        """
        if key_funcs is None:
            raise NullArgumentError(u"key_funcs argument cannot be None")
        if not isinstance(key_funcs, list):
            raise TypeError(u"key_funcs should be a list instance")
        self._key_funcs = [f for f in key_funcs if isinstance(f, OrderingDirection)]
        for o in reversed(self._key_funcs):
            data = sorted(data, key=o.key, reverse=o.descending)
        super(SortedEnumerable, self).__init__(data)

    def then_by(self, func):
        """
        Subsequent sorting function in ascending order
        :param func: lambda expression for secondary sort key
        :return: SortedEnumerable instance
        """
        if func is None:
            raise NullArgumentError(u"then by requires a lambda function arg")
        self._key_funcs.append(OrderingDirection(key=func, reverse=False))
        return SortedEnumerable(self, self._key_funcs)

    def then_by_descending(self, func):
        """
        Subsequent sorting function in descending order
        :param func: lambda function for secondary sort key
        :return: SortedEnumerable instance
        """
        if func is None:
            raise NullArgumentError(
                u"then_by_descending requires a lambda function arg"
            )
        self._key_funcs.append(OrderingDirection(key=func, reverse=True))
        return SortedEnumerable(self, self._key_funcs)


class ZipEnumerable(Enumerable):
    """
    Class to hold state for zipping 2 collections together
    """

    def __init__(self, enumerable1, enumerable2, result_func):
        super(ZipEnumerable, self).__init__(enumerable1)
        self.enumerable = enumerable2
        self.result_func = result_func

    def __iter__(self):
        return map(
            lambda r: self.result_func(r), zip(iter(self._iterable), self.enumerable)
        )
