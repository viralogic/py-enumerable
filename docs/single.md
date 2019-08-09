## single

`single(predicate=None)`

Returns the only element in an `Enumerable` collection.

If a `predicate` is given, then it must be the only element in the collection that satisfies the condition. If the collection contains no elements that satisfy the given `predicate` then a _NoElementsError_ is raised. If the collections contains 2 or more matching elements then a _MoreThanOneMatchingElementError_ is raised.

This is an executing function.

**Parameters**

__predicate__ : condition to satisfy as a `lambda` function. Optional.

**Returns**

The only element in the `Enumerable` collection that matches the given `predicate`.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).single(lambda x: x['value'] == 1)
# {'value': 1}

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).single()
# MoreThanOneMatchingElementError

Enumerable([]).single()
# raises NoElementsError
</code></pre>