## last_index_of

`last_index_of(n)`

Returns the index of the last occurrence of a given element in an `Enumerable` collection. If no matching element is found, None is returned. This is an executing function.

**Parameters**

__element__ : the element to search for and return the last index of within the collection

**Returns**

The last index of the given element, or None.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3},
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).last_index_of({'value': 2})
# 4

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).last_index_of({'value': 4})
# None
</code></pre>