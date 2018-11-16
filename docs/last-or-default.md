## last_or_default

`last_or_default()`

Returns the last element in an `Enumerable` collection. If the collection contains no elements then returns `None`. This is an executing function.

**Parameters**

None

**Returns**

The last element in the `Enumerable` collection or `None` if the collection contains no elements.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).last_or_default()
# {'value': 3}

result = Enumerable([]).last_or_default()
result is None
# True
</code></pre>