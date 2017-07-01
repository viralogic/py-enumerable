.. image:: https://travis-ci.org/scls19fr/py-enumerable.svg?branch=master
    :target: https://travis-ci.org/scls19fr/py-enumerable

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
Similar to LINQ in C#, there are certain functions in py-linq that cause the query expression to be evaluated.

The following functions will execute an Enumerable query expression:

1. to_list
2. count
3. sum
4. min
5. max
6. avg
7. median
8. any -- uses count in algorithm
9. elementAt -- has to store data in list to allow resetting of iterator
10. elemantAtOrDefault --uses elementAt
11. first --uses elementAt
12. first_or_default --uses first
13. last --uses first after sorting
14. last_or_default --uses last
15. contains --uses any
16. group_by -- due to grouped iterables having to be saved to memory when iterating through itertools.groupby result
17. distinct -- uses group by in algorithm
18. group_join -- uses group by in algorithm
19. union -- uses distinct in algorithm



Available Functions
-------------------
Similar to LINQ, py-linq makes extensive use of Python lambda expressions as function parameters.

Most of the standard LINQ functions are available from the Enumerable class:

**Non excecuting functions**

1. select
2. order_by
3. order_by_descending
4. skip
5. take
6. where
7. select_many
8. add
9. concat
10. join
11. intersect
12. except_

**Executing functions**

13. to_list
14. count
15. sum
16. min
17. max
18. avg
19. median
20. any -- uses count in algorithm
21. elementAt -- has to store data in list to allow resetting of iterator
22. elemantAtOrDefault --uses elementAt
23. first --uses elementAt
24. first_or_default --uses first
25. last --uses first after sorting
26. last_or_default --uses last
27. contains --uses any
28. group_by -- due to grouped iterables having to be saved to memory when iterating through itertools.groupby result
29. distinct -- uses group by in algorithm
30. group_join -- uses group by in algorithm
31. union -- uses distinct in algorithm

Please refer to the MSDN `Enumerable <http://msdn.microsoft.com/en-us/library/system.linq.enumerable_methods(v=vs.100).aspx>`_
class for more information on how to use each function or view the Enumerable class `source <https://github.com/viralogic/py-enumerable/blob/master/py_linq/py_linq.py>`_ code.
