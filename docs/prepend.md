## prepend

`prepend(element)`

Prepends an element to the beginning of an `Enumerable`. This is not an executing function.

**Parameters**

__element__ : the element to prepend.

**Returns**

An `Enumerable` object with the element prepended to the beginning.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable([1, 2, 3]).prepend(4)
# [4, 1, 2, 3]
</code></pre>