=============
py-linq
=============
LINQ (Language Integrated Query) is a popular querying language available in .NET. This library ports the language so
that developers can query collections of objects using the same syntax. This library would be useful for Python developers
with experience using the expressiveness and power of LINQ.

Install
-------
Available as a package from PyPI.
::
    pip install py-linq

Usage
-----
To access the LINQ functions an iterable needs to be wrapped by the Enumerable class.
::
    from py_linq import Enumerable
    my_collection = Enumerable([1,2,3])

Executing Functions
-------------------
Similar to LINQ in C#, there are certain functions in py-linq that cause the query expression to be evaluated. Because
py-linq uses iterables as its underlying data source, once an expression is evaluated, the iterable is exhausted. Thus,
the following statement would give erroneous results:
::

    my_collection = Enumerable([1,2,3])
    count = my_collection.count() **gives 3**
    sum = my_collection.sum() **iterable exhausted - gives 0, but should give 6**

If you need to perform multiple "executing" functions on the same Enumerable, first save it to memory using the to_list()
function and re-wrap the list as an Enumerable.
::
    my_collection = Enumerable([1,2,3]).where(lambda x: x==1).to_list() **Save to memory**
    count = len(my_collection) **gives 1**
    sum = Enumerable(my_collection).sum() **gives 1**

The following functions will execute an Enumerable query expression:

1. to_list
2. count
3. sum
4. min
5. max
6. avg
7. median


Available Functions
-------------------
Similar to LINQ, py-linq makes extensive use of Python lambda expressions as function parameters.

Most of the standard LINQ functions are available from the Enumerable class:

**Non excecuting functions**

1. select
2. elementAt
3. elementAtOrDefault
4. first
5. first_or_default
6. last
7. last_or_default
8. order_by
9. order_by_descending
10. skip
11. take
12. where
13. single
14. single_or_default
15. select_many
16. add
17. concat
18. group_by
19. distinct
20. join
21. default_if_empty
22. group_join
23. any
24. intersect
25. except_
26. union
27. contains

**Executing functions**

28. to_list
29. count
30. sum
31. min
32. max
33. avg
34. median

Please refer to the MSDN `Enumerable <http://msdn.microsoft.com/en-us/library/system.linq.enumerable_methods(v=vs.100).aspx>`_
class for more information on how to use each function.

Enumerable class source
-----------------------
.. literalinclude:: py_linq/py_linq.py
    :start-after: 5
    :end-before: 445
