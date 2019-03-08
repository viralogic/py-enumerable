## zip

`zip(enumerable)`

Merges elements from two `Enumerable` collections into a single collection

**Parameters**

__enumerable__: the second sequence to merge

**Returns**

An `Enumerable` that contains merged elements from two sequences.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable(["A", "B", "C", "D"]).zip(Enumerable(["x", "y"]), lambda t: "{0}{1}".format(t[0], t[1]))
# ["Ax", "By"]
</code></pre>