## default_if_empty

`default_if_empty(value=None)`

Returns the elements of the specified sequence or the specified value in a singleton collection if the sequence is empty.

**Parameters**

__value__: the default value to return if the collection is empty

**Returns**

An `Enumerable` object that contains `value` if the input `Enumerable` is empty, otherwise returns the input `Enumerable`

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable([]).default_if_empty()
# [None]

test = Enumerable([]).default_if_empty(value=u"I am empty!")
# ["I am empty!"]
</code></pre>