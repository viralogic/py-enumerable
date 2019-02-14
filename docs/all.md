## all

`all(predicate)`

Determines if all elements in the `Enumerable` collection match the given predicate. This is an executing function.

**Parameters**

__predicate__ : condition to satisfy as a `lambda` function.

**Returns**

Boolean result if at all elements match the given predicate

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).all(lambda x: x['value'] <= 3)
# True
</code></pre>