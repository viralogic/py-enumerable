## count

`count()`

Returns the number of elements in the `Enumerable` instance. This is an executing function.

**Parameters**

None

**Returns**

The number of elements in the `Enumerable` instance as an integer.

**Example**

<pre><code>
from py_linq import Enumerable

collection = Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).count()
# 3
</code></pre>