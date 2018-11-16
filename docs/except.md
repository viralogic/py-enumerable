## except

`except_(enumerable, key=lambda x: x)`

Returns an `Enumerable` that contains elements not found in the given `enumerable` argument. This is also known as a set difference. This is not an executing function.

**Parameters**

__enumerable__ : an `Enumerable` instance to perform set difference against<br>
__key__ : `lambda` function used as a key selector for both sets

**Returns**

An `Enumerable` object that is the result of a set difference.

**Examples**

<pre><code>
from py_linq import Enumerable

e1 = Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
])
diff = e1.except_(Enumerable([{'value': 1}])
# [{'value': 2}, {'value': 3}]
</code></pre>