## any

`any(predicate=None)`

Determines if any elements in the `Enumerable` collection match the given predicate. This is an executing function.

**Parameters**

__predicate__ : condition to satisfy as a `lambda` function. Optional.

**Returns**

Boolean result if at least 1 element matches the given predicate. If no predicate is given, then the boolean result after checking if the collection is empty.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).any(lambda x: x['value'] == 3)
# True
</code></pre>