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
12. except_
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