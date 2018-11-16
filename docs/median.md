## median

`median(func=lambda x: x)`

Finds the median of an `Enumerable` collection. Used for computing the average of a collection of numbers. This is an executing function.

**Parameters**

__func__ : a `lambda` function used as a key selector to find the median over.

**Returns**

The median value of the collection

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).median(lambda x: x['value'])
# 2

# Works for collections of strings as well
Enumerable([
    'Alice',
    'Bob',
    'Zeke'
]).median()
# 'Bob'
</code></pre>