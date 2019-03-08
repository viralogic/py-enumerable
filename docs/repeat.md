## repeat

`repeat(element, n)`

Generates a repeating sequence of an element `n` times.

**Parameters**

__element__ : the element to repeat<br>
__n__ : the number of times to repeat the element

**Returns**

An `Enumerable` collection of `n` repeated elements.

**Example**

<pre><code>
from py_linq import Enumerable

test = u"".join(Enumerable.repeat(u'Z', 10).to_list())
# ZZZZZZZZZZ
</code></pre>