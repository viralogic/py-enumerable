## element_at_or_default

`element_at_or_default(n)`

Returns the element in an `Enumerable` collection at the given index. If no element is found at the given index then `None` is returned. This is an executing function.

**Parameters**

__n__ : zero-based index of the element to return

**Returns**

The element at the given index or `None` if no element exists at the given index.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).element_at_or_default(2)
# {'value': 3}

result = Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).element_at_or_default(3)

result is None
# True

</code></pre>