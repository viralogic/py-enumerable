## to_dictionary

`to_dictionary()`

Creates a `dict` from an `Enumerable`. This is not an executing function.

**Parameters**

__key__ : `lambda` function used for selecting the key for each item in a collection

__value__: optional `lambda` function used for selecting the value for each item in a collection. Defaults to the item in the collection. 

**Returns**

A Python `dict` instance

**Example**

<pre><code>
from py_linq import Enumerable

collection = Enumerable([
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
])

collection.to_dictionary(lambda t: t[0], lambda t: t[1:])
"""
{
    0: [1, 2],
    3: [4, 5],
    6: [7, 8]
}
"""

collection.to_dictionary(lambda t: t[-1])
"""
{
    2: [0, 1, 2],
    5: [3, 4, 5],
    8: [6, 7, 8]
}
"""
</code></pre>