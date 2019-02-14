## append

`append(element)`

Appends an element to the end of an `Enumerable`. This is not an executing function.

**Parameters**

__element__ : the element to append.

**Returns**

An `Enumerable` object with the element appended to the end.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable([1, 2, 3]).append(4)
# [1, 2, 3, 4]
</code></pre>