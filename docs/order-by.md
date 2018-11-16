## order_by

`order_by(key)`

The order_by method order the collection in _ascending_ order using the _key_ lambda expression. This method is not an executing function.

**Parameters:**

_key_: lambda expression that extracts a key from an element in the collection.

**Returns:**

A `SortedEnumerable` object whose elements are ordered by the _key_ in ascending order. A `SortedEnumerable` will allow access to the `then_by` and `then_by_descending` methods.

**Example**

<pre><code>
from py_linq import Enumerable

numbers = Enumerable([80, 90, 25, 65])
ascending_numbers = numbers.order_by(lambda x: x).to_list() # results [25, 65, 80, 90]
</code></pre>