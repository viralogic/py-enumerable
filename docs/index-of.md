## index_of

`index_of(n)`

Returns the index of a given element in an `Enumerable` collection. If no matching element is found, None is returned. This is an executing function.

**Parameters**

__element__ : the element to search for and return the index of within the collection

**Returns**

The index of the given element, or None.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).index_of({'value': 2})
# 1

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).index_of({'value': 4})
# None
</code></pre>