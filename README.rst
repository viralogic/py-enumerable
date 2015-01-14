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
8. any
9. elementAt
10. elemantAtOrDefault
11. first
12. first_or_default
13. last
14. last_or_default
15. contains



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
class for more information on how to use each function or view the Enumerable class `source <https://github.com/viralogic/py-enumerable/blob/master/py_linq/py_linq.py>`_ code.
