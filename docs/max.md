## max

`max(func=lambda x: x)`

Finds the maximum in an `Enumerable` collection. This is an executing function.

**Parameters**

__func__ : a `lambda` function used as a key selector to find the maximum over.

**Returns**

The maximum of the collection

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).max(lambda x: x['value'])
# 3

# For a string
Enumerable([
    'Alice',
    'Bob',
    'Zeke'
]).max()
# 'Zeke'
</code></pre>