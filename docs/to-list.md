## to_list

`to_list()`

Converts an `Enumerable` instance to a `list`. This is an executing function.

**Parameters**

None

**Returns**

A Python `list` instance

**Example**

<pre><code>
from py_linq import Enumerable

collection = Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).to_list()
</code></pre>