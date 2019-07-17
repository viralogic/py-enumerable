## first_or_default

`first_or_default(predicate)`

Returns the first element in an `Enumerable` collection. If a `predicate` is given, then it is the first element in the collection that satisfies the condition. If the collection contains no elements then `None` is returned. This is an executing function.

**Parameters**

__predicate__ : condition to satisfy as a `lambda` function. Optional.

**Returns**

The first element in the `Enumerable` collection or `None` if the collection is empty.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).first_or_default()
# {'value': 1}

result = Enumerable([]).first_or_default()
result is None
# True
</code></pre>