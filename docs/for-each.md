## for_each

`for_each(n)`

Executes a given function per each element in an `Enumerable` collection. Syntactic sugar for a for loop. This is an executing function.

**Parameters**

__func__ : the function, lambda or otherwise, to execute per each element

**Returns**

None

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([1 ,2 ,3]).for_each(print)
# 1
# 2
# 3

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).for_each(lambda x: print(x['value']))
# 1
# 2
# 3

</code></pre>