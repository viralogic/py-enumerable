## sum

`sum(func=lambda x: x)`

Sums the elements in `Enumerable`. This is an executing function.

**Parameters**

__func__ : `lambda` function used as a key selector to sum over

**Returns**

The sum of the elements in `Enumerable`.

**Examples**

<pre><code>
from py_linq import Enumerable

collection = Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).sum()
# 6
</code></pre>