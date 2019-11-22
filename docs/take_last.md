## take_last

`take_last(n)`

Takes the last `n` elements in an `Enumerable` collection. This is not an executing function.

**Parameters**

__n__: the number of elements at the end of the sequence to take

**Returns**

An `Enumerable` containing the last `n` elements of an input collection.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable([1, 2, 3, 4, 5]).take_last(2)
# [4, 5]
</code></pre>