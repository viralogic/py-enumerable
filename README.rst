=============
py-linq
=============
LINQ (Language Integrated Query) is a popular querying language available in .NET. This library ports the language so
that developers can query collections of objects using the same syntax. This library would be useful for Python developers
with experience using the expressiveness and power of LINQ.

Install
-------
Available as a package from PyPI.

'pip install py-linq'

Usage
-----
To access the LINQ functions an iterable needs to be wrapped by the Enumerable class.::

from py_linq import Enumerable
my_collection = Enumerable([1,2,3])

Executing Functions
-------------------
Similar to LINQ in C#, there are certain functions in py-linq that cause the query expression to be evaluated. Because
py-linq uses iterables as its underlying data source, once an expression is evaluated, the iterable is exhausted. Thus,
the following statement would give erroneous results::

my_collection = Enumerable([1,2,3])
count = my_collection.count() **gives 3**
sum = my_collection.sum() **iterable exhausted - gives 0, but should give 6**

If you need to perform multiple "executing" functions on the same Enumerable, first save it to memory using the to_list()
function and re-wrap the list as an Enumerable.::

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
3. first
4. first_or_default
5. last
6. last_or_default
7. order_by
8. order_by_descending
9. skip
10. take
11. where
12. single
13. single_or_default
14. select_many
15. add
16. concat
17. group_by
18. distinct
19. join
20. default_if_empty
21. group_join
22. any
23. intersect
24. except_
25. union
26. contains

**Executing functions**
27. to_list
28. count
29. sum
30. min
31. max
32. avg
33. median

Please refer to the .. Enumerable class MSDN page:http://msdn.microsoft.com/en-us/library/system.linq.enumerable_methods(v=vs.100).aspx
for more information on how to use each function.




