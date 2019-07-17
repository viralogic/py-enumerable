## last

`last(predicate)`

Returns the last element in an `Enumerable` collection. If a `predicate` is given, then it is the first element in the collection that satisfies the condition. If the collection contains no elements then a _NoElementsError_ is raised. This is an executing function.

**Parameters**

__predicate__ : condition to satisfy as a `lambda` function. Optional.

**Returns**

The last element in the `Enumerable` collection

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).last()
# {'value': 3}

Enumerable([]).last()
# raises NoElementsError
</code></pre>