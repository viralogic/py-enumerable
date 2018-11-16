## union

`union(enumerable, key=lambda x: x)`

Returns `Enumerable` that is a union between two `Enumerable` collections. Note that the key selector `lambda` function needs to map to comparable values in both `Enumerable` collections. This is an executing function.

**Parameters**

__enumerable__ : The second `Enumerable` collection to union with.
__key__: function to extract the key used to determine uniqueness

**Returns**

An `Enumerable` collection that only contains elements that are distinct by the given key

**Examples**

<pre><code>
from py_linq import Enumerable

Enumerable([1, 2, 3]).union(Enumerable([1, 4, 5]), lambda x: x).to_list()
# [1, 2, 3, 4, 5]
</code></pre>