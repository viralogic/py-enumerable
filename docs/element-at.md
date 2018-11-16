## element_at

`element_at(n)`

Returns the element in an `Enumerable` collection at the given index. If no element is found at the given index a _NoElementsError_ is raised. This is an executing function.

**Parameters**

__n__ : zero-based index of the element to return

**Returns**

The element at the given index. 

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).element_at(2)
# {'value': 3}

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).element_at(3)
# raises NoElementsError
</code></pre>