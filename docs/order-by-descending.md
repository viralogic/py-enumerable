## order_by_descending

`order_by_descending(key)`

The order_by_descending method orders the collection in _descending_ order using the _key_ lambda expression. This method is not an executing function.

**Parameters:**

_key_: lambda expression that extracts a key from an element in the collection.

**Returns:**

A `SortedEnumerable` object whose elements are ordered by the _key_ in descending order. A `SortedEnumerable` will allow access to the `then_by` and `then_by_descending` methods.

**Example**

<pre><code>
from py_linq import Enumerable

numbers = Enumerable([80, 90, 25, 65])
descending_numbers = numbers.order_by_descending(lambda x: x).to_list() # results [90, 80, 65, 25]
</code></pre>