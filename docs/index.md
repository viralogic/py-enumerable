# py-linq #

py-linq is a little wrapper package that I wrote a few years ago for querying and transforming collections of Python objects. I found that the built-in Python querying and transforming tools were lacking. Specifically, the Python API made the code unreadable and difficult to understand. It made me long for the LINQ API's available in .NET. So I decided to sit down and try to write it.

## Getting started ##

To get started using py-linq, you will need to install it from PyPI.

`pip install py-linq`

To start querying and transforming your Python collection you will need to import `Enumerable`.

`from py_linq import Enumerable`

### Enumerable ###

`Enumerable` is just the access point for the py-linq API. There are 2 ways to instantiate an `Enumerable` object.

<pre>
<code>my_collection = Enumerable()<br>
my_collection = Enumerable(<i>collection</i>)
</code></pre>

The _collection_ class has to implement the `__iter__` dunder. The default constructor `Enumerable()` is just `Enumerable(collection)` where _collection_ is `[]`. `Enumerable` itself is an iterable.

### LINQ methods ###

The methods encapsulated by the `Enumerable` class can be either _executing_ functions or _non-executing_. Executing functions will iterate over the collection when it is called. Non-executing functions will not iterate over the collections. These functions will be executed **only** when the collection does get iterated over.

Once you have created an `Enumerable` instance, the LINQ methods will become available to you. The methods implemented at this point are:

1. [select](/py-enumerable/select)
2. [order_by](/py-enumerable/order-by)
3. [order_by_descending](/py-enumerable/order-by-descending)
4. [skip](/py-enumerable/skip)
5. [take](/py-enumerable/take)
6. [where](/py-enumerable/where)
7. [select_many](/py-enumerable/select-many)
8. [add](/py-enumerable/add)
9. [concat](/py-enumerable/concat)
10. [join](/py-enumerable/join)
11. [intersect](/py-enumerable/intersect)
12. [except_](/py-enumerable/except)
13. [to_list](/py-enumerable/to-list)
14. [count](/py-enumerable/count)
15. [sum](/py-enumerable/sum)
16. [min](/py-enumerable/min)
17. [max](/py-enumerable/max)
18. [avg](/py-enumerable/avg)
19. [median](/py-enumerable/median)
20. [any](/py-enumerable/any)
21. [element_at](/py-enumerable/element-at)
22. [element_at_or_default](/py-enumerable/element-at-or-default)
23. [first](/py-enumerable/first)
24. [first_or_default](/py-enumerable/first-or-default)
25. [last](/py-enumerable/last)
26. [last_or_default](/py-enumerable/last-or-default)
27. [contains](/py-enumerable/contains)
28. [group_by](/py-enumerable/group-by)
29. [distinct](/py-enumerable/distinct)
30. [group_join](/py-enumerable/group-join)
31. [union](/py-enumerable/union)