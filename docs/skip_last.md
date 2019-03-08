## skip_last

`skip_last(n)`

Skips over the last `n` elements in an `Enumerable` collection

**Parameters**

__n__: the number of elements at the end of the sequence to skip

**Returns**

An `Enumerable` with the last `n` elements skipped over.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable(["one", "two", "three", "four", "five"]).skip(1).skip_last(1)
# ["two", "three", "four"]
</code></pre>