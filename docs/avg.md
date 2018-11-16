## avg

`max(func=lambda x: x)`

Finds the average of an `Enumerable` collection. Used for computing the average of a collection of numbers. This is an executing function.

**Parameters**

__func__ : a `lambda` function used as a key selector to find the average over.

**Returns**

The average of the collection

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).avg(lambda x: x['value'])
# 2.0
</code></pre>