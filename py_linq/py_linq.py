import itertools
import json
import io
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
from .core import Key, OrderingDirection, RepeatableIterable
from .decorators import deprecated
from .exceptions import (
    NoElementsError,
    NoMatchingElement,
    NullArgumentError,
    MoreThanOneMatchingElement,
)


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

    def __iter__(self):
        return iter(self._iterable)

    def next(self):
        return next(self._iterable)

    def __next__(self):
        return self.next()

    def __getitem__(self, n):
        """
        Gets item in iterable at specified zero-based index
        :param n: the index of the item to get
        :returns the element at the specified index.
        :raises IndexError if n > number of elements in the iterable
        """
        for i, e in enumerate(self):
            if i == n:
                return e

    def __len__(self):
        """
        Gets the number of elements in the collection
        """
        return len(self._iterable)

    def __repr__(self):
        return list(self).__repr__()

    def to_list(self):
        """
        Converts the iterable into a list
        :return: list object
        """
        return [x for x in self]

    def count(self, predicate=None):
        """
        Returns the number of elements in iterable
        :return: integer object
        """
        if predicate is not None:
            return sum(1 for element in self.where(predicate))
        return sum(1 for element in self)

    def select(self, func=lambda x: x):
        """
        Transforms data into different form
        :param func: lambda expression on how to perform transformation
        :return: new Enumerable object containing transformed data
        """
        return SelectEnumerable(Enumerable(iter(self)), func)

    def sum(self, func=lambda x: x):
        """
        Returns the sum of af data elements
        :param func: lambda expression to transform data
        :return: sum of selected elements
        """
        return sum(func(x) for x in self)

    def min(self, func=lambda x: x):
        """
        Returns the min value of data elements
        :param func: lambda expression to transform data
        :return: minimum value
        """
        if not self.any():
            raise NoElementsError(u"Iterable contains no elements")
        return func(min(self, key=func))

    def max(self, func=lambda x: x):
        """
        Returns the max value of data elements
        :param func: lambda expression to transform data
        :return: maximum value
        """
        if not self.any():
            raise NoElementsError(u"Iterable contains no elements")
        return func(max(self, key=func))

    def avg(self, func=lambda x: x):
        """
        Returns the average value of data elements
        :param func: lambda expression to transform data
        :return: average value as float object
        """
        if not self.any():
            raise NoElementsError(u"Iterable contains no elements")
        return float(self.sum(func)) / float(self.count())

    def median(self, func=lambda x: x):
        """
        Return the median value of data elements
        :param func: lambda expression to project and sort data
        :return: median value
        """
        if not self.any():
            raise NoElementsError(u"Iterable contains no elements")
        result = self.order_by(func).select(func).to_list()
        length = len(result)
        i = int(length / 2)
        return (
            result[i]
            if length % 2 == 1
            else (float(result[i - 1]) + float(result[i])) / float(2)
        )

    def element_at(self, n):
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

    def element_at_or_default(self, n):
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

    def first(self, func=None):
        """
        Returns the first element in a collection
        :func: predicate as lambda expression used to filter collection
        :return: data element as object or NoElementsError if transformed data
        contains no elements
        """
        if func is not None:
            return self.where(func).element_at(0)
        return self.element_at(0)

    def first_or_default(self, func=None):
        """
        Return the first element in a collection. If collection is empty, then returns None
        :func: predicate as lambda expression used to filter collection
        :return: data element as object or None if transformed data contains no
         elements
        """
        if func is not None:
            return self.where(func).element_at_or_default(0)
        return self.element_at_or_default(0)

    def last(self, func=None):
        """
        Return the last element in a collection
        :func: predicate as a lambda expression used to filter collection
        :return: data element as object or NoElementsError if transformed data
        contains no elements
        """
        if func is not None:
            return self.where(func).reverse().first()
        return self.reverse().first()

    def last_or_default(self, func=None):
        """
        Return the last element in a collection or None if the collection is empty
        :func: predicate as a lambda expression used to filter collection
        :return: data element as object or None if transformed data contains no
         elements
        """
        if func is not None:
            return self.where(func).reverse().first_or_default()
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

    def skip(self, n):
        """
        Returns new Enumerable where n elements have been skipped
        :param n: Number of elements to skip as int
        :return: new Enumerable object
        """
        return SkipEnumerable(Enumerable(iter(self)), n)

    def take(self, n):
        """
        Return new Enumerable where first n elements are taken
        :param n: Number of elements to take
        :return: new Enumerable object
        """
        return TakeEnumerable(Enumerable(iter(self)), n)

    def where(self, predicate):
        """
        Returns new Enumerable where elements matching predicate are selected
        :param predicate: predicate as a lambda expression
        :return: new Enumerable object
        """
        if predicate is None:
            raise NullArgumentError("No predicate given for where clause")
        return WhereEnumerable(Enumerable(iter(self)), predicate)

    def single(self, predicate=None):
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
        if not result.any():
            raise NoMatchingElement("No matching elements are found")
        if result.count() > 1:
            raise MoreThanOneMatchingElement("More than one matching element is found")
        return result.to_list()[0]

    def single_or_default(self, predicate=None):
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

    def select_many(self, func=lambda x: x):
        """
        Flattens an iterable of iterables returning a new Enumerable
        :param func: selector as lambda expression
        :return: new Enumerable object
        """
        return SelectManyEnumerable(Enumerable(iter(self)), func)

    def add(self, element):
        """
        Adds an element to the enumerable.
        :param element: An element
        :return: new Enumerable object
        """
        if element is None:
            return self
        return self.concat(Enumerable([element]))

    def concat(self, enumerable):
        """
        Adds enumerable to an enumerable
        :param enumerable: An iterable object
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable argument must be an instance of Enumerable")
        concatenated = ConcatenateEnumerable(Enumerable(iter(self)), enumerable)
        self._iterable = concatenated
        return concatenated

    def group_by(self, key_names=[], key=lambda x: x, result_func=lambda x: x):
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
        return GroupedEnumerable(Enumerable(iter(self)), key, key_names, result_func)

    def distinct(self, key=lambda x: x):
        """
        Returns enumerable containing elements that are distinct based on
        given key selector
        :param key: key selector as lambda expression
        :return: new Enumerable object
        """
        return GroupedEnumerable(
            Enumerable(iter(self)), key, ["distinct"], lambda g: g.first()
        )

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
        return JoinEnumerable(
            Enumerable(iter(self)), inner_enumerable, outer_key, inner_key, result_func
        )

    def default_if_empty(self, value=None):
        """
        Returns an enumerable containing a single None element if enumerable is
        empty, otherwise the enumerable itself
        :return: an Enumerable object
        """
        if not self.any():
            return Enumerable([value])
        return self

    def group_join(
        self,
        inner_enumerable,
        outer_key=lambda x: x,
        inner_key=lambda x: x,
        result_func=lambda x: x,
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
        group_joined = (
            Enumerable(iter(self))
            .join(
                inner_enumerable=inner_enumerable,
                outer_key=outer_key,
                inner_key=inner_key,
                result_func=lambda e: (e[0], e[1]),
            )
            .group_by(
                key_names=["id"],
                key=lambda t: outer_key(t[0]),
                result_func=lambda g: (
                    g.first()[0],
                    g.where(lambda i: inner_key(i[1]) == g.key.id).select(
                        lambda i: i[1]
                    ),
                ),
            )
            .select(lambda gj: result_func(gj))
        )
        return group_joined

    def any(self, predicate=None):
        """
        Returns true if any elements that satisfy predicate are found
        :param predicate: condition to satisfy as lambda expression
        :return: boolean True or False
        """
        return self.first_or_default(predicate) is not None

    def intersect(self, enumerable, key=lambda x: x):
        """
        Returns enumerable that is the intersection between given enumerable
        and self
        :param enumerable: enumerable object
        :param key: key selector as lambda expression
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable parameter must be an instance of Enumerable")
        return IntersectEnumerable(Enumerable(iter(self)), enumerable, key)

    def aggregate(self, func, seed=None):
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

    def union(self, enumerable, key=lambda x: x):
        """
        Returns enumerable that is a union of elements between self and given
        enumerable
        :param enumerable: enumerable to union self to
        :param key: key selector used to determine uniqueness
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable parameter must be an instance of Enumerable")
        return UnionEnumerable(Enumerable(iter(self)), enumerable, key)

    def except_(self, enumerable, key=lambda x: x):
        """
        Returns enumerable that subtracts given enumerable elements from self
        :param enumerable: enumerable object
        :param key: key selector as lambda expression
        :return: new Enumerable object
        """
        if not isinstance(enumerable, Enumerable):
            raise TypeError(u"enumerable parameter must be an instance of Enumerable")
        return ExceptEnumerable(Enumerable(iter(self)), enumerable, key)

    def contains(self, element, key=lambda x: x):
        """
        Returns True if element is found in enumerable, otherwise False
        :param element: the element being tested for membership in enumerable
        :param key: key selector to use for membership comparison
        :return: boolean True or False
        """
        return self.select(key).any(lambda x: x == key(element))

    def all(self, predicate):
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
        return RepeatEnumerable(element, length)

    def reverse(self):
        """
        Inverts the order of the elements in a sequence
        :return: Enumerable with elements in reversed order
        """
        return ReversedEnumerable(Enumerable(iter(self)))

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


class SelectEnumerable(Enumerable):
    """
    Class to hold state for projection of elements in a collection
    """

    def __init__(self, enumerable, func):
        super(SelectEnumerable, self).__init__(enumerable)
        self.func = func

    def __iter__(self):
        for e in iter(self._iterable):
            yield self.func(e)


class WhereEnumerable(Enumerable):
    """
    Class to hold state for filtering elements in a collection
    """

    def __init__(self, enumerable, predicate):
        super(WhereEnumerable, self).__init__(enumerable)
        self.predicate = predicate

    def __iter__(self):
        for e in iter(self._iterable):
            if self.predicate(e):
                yield e

    def __getitem__(self, n):
        for i, e in enumerate(filter(self.predicate, self)):
            if i == n:
                return e


class SelectManyEnumerable(Enumerable):
    """
    Class to hold state for flattening nested collections within a collection
    """

    def __init__(self, enumerable, selector):
        super(SelectManyEnumerable, self).__init__(enumerable)
        self.selector = selector

    def __iter__(self):
        for element in iter(self._iterable):
            collection = self.selector(element)
            for subelement in collection:
                yield subelement


class SkipEnumerable(Enumerable):
    """
    Class to hold state for skipping elements in a collection
    """

    def __init__(self, enumerable, n):
        super(SkipEnumerable, self).__init__(enumerable)
        self.n = n

    def __iter__(self):
        for index, element in enumerate(self._iterable):
            if index >= self.n:
                yield element


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


class ReversedEnumerable(Enumerable):
    """
    Class to hold state for reversing elements in a collection
    """

    def __init__(self, enumerable):
        super(ReversedEnumerable, self).__init__(enumerable)

    def __iter__(self):
        stack = LifoQueue()
        for element in self._iterable:
            stack.put(element)
        while not stack.empty():
            yield stack.get()


class ConcatenateEnumerable(Enumerable):
    """
    Class to hold state for concatenating Enumerable collections
    """

    def __init__(self, enumerable1, enumerable2):
        super(ConcatenateEnumerable, self).__init__(enumerable1)
        self.enumerable = enumerable2

    def __iter__(self):
        for i in iter(self._iterable):
            yield i
        for j in iter(self.enumerable):
            yield j

    def __getitem__(self, n):
        if n < 0:
            raise IndexError
        if n == len(self) + len(self.enumerable):
            return None
        i = 0
        it = self._iterable if n < len(self._iterable) else self.enumerable._iterable
        while i < n:
            next(it)
            i += 1
        return next(it)


class IntersectEnumerable(Enumerable):
    """
    Class to hold state for determining the intersection between two sets
    """

    def __init__(self, enumerable1, enumerable2, key):
        super(IntersectEnumerable, self).__init__(enumerable1)
        self.enumerable = enumerable2
        self.key = key

    def __iter__(self):
        for i in iter(self._iterable):
            k1 = self.key(i)
            if any(self.key(i2) == k1 for i2 in self.enumerable):
                yield i


class ExceptEnumerable(IntersectEnumerable):
    """
    Class to hold state for determining the set minus of collection given another collection
    """

    def __init__(self, enumerable1, enumerable2, key):
        super(ExceptEnumerable, self).__init__(enumerable1, enumerable2, key)

    def __iter__(self):
        for i in iter(self._iterable):
            k1 = self.key(i)
            if not any(self.key(i2) == k1 for i2 in self.enumerable):
                yield i


class UnionEnumerable(Enumerable):
    """
    Class to hold state for determining the set union of a collection with another collection
    """

    def __init__(self, enumerable1, enumerable2, key):
        super(UnionEnumerable, self).__init__(enumerable1)
        self.enumerable = enumerable2
        self.key = key

    def __iter__(self):
        union = dict()
        for e in itertools.chain(iter(self._iterable), self.enumerable):
            key = self.key(e)
            key_hash = hash(json.dumps(key, default=str))
            if key_hash not in union:
                yield e
                union[key_hash] = e


class GroupedEnumerable(Enumerable):
    def __init__(self, enumerable, key, key_names, func=lambda x: x):
        """
        Constructor for GroupedEnumerable class
        :param grouped_data: Iterable of grouped data
        """
        super(GroupedEnumerable, self).__init__(enumerable)
        self.key = key
        self.key_names = key_names
        self.func = func
        self.grouping = dict()
        self._load_data()

    def _load_data(self):
        for d in iter(self._iterable):
            key_value = self.key(d)
            kv_hash = hash(json.dumps(key_value))
            if kv_hash not in self.grouping:
                key_prop = {}
                for i, prop in enumerate(self.key_names):
                    key_prop[prop] = (
                        key_value[i] if self._can_enumerate(key_value) else key_value
                    )
                self.grouping[kv_hash] = Grouping(Key(key_prop), [d])
            else:
                self.grouping[kv_hash].add(d)

    def _can_enumerate(self, key_value):
        return (
            hasattr(key_value, "__len__")
            and len(key_value) > 0
            and not isinstance(key_value, string_types)
        )

    def __iter__(self):
        for k in self.grouping:
            yield self.func(self.grouping[k])


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

    def add(self, item):
        self._iterable._data.append(item)


class SortedEnumerable(Enumerable):
    def __init__(self, enumerable, key_funcs):
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
        data = enumerable
        for o in reversed(self._key_funcs):
            data = sorted(iter(data), key=o.key, reverse=o.descending)
        super(SortedEnumerable, self).__init__(data)

    def __getitem__(self, n):
        result = None
        for i, e in enumerate(self):
            if i == n:
                result = e
        return result

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


class RepeatEnumerable(Enumerable):
    """
    Class to hold state for creating an Enumerable of a repeated element
    """

    def __init__(self, element, length):
        self.element = element
        self.length = length

    def __iter__(self):
        return itertools.repeat(self.element, self.length)


class JoinEnumerable(Enumerable):
    """
    Class to hold state for performing inner join of 2 enumerables
    """

    def __init__(
        self, outer_enumerable, inner_enumerable, outer_key, inner_key, result_func
    ):
        """
        Constructor
        :param outer_enumerable -> the outer collection to join against
        :param inner_enumerable -> the inner collection to join to outer enumerable
        :param outer_key -> lambda function for selecting the outer enumerable key
        :param inner_key -> lambda function for selecting the inner enumerable key
        :param result_func -> lambda function for transforming the result
        """
        super(JoinEnumerable, self).__init__(outer_enumerable)
        self.inner_enumerable = inner_enumerable
        self.outer_key = outer_key
        self.inner_key = inner_key
        self.result_func = result_func

    def __iter__(self):
        for outer in iter(self._iterable):
            ok = self.outer_key(outer)
            for inner in iter(self.inner_enumerable):
                ik = self.inner_key(inner)
                if ok == ik:
                    yield self.result_func((outer, inner))
