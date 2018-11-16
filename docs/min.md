## min

`min(func=lambda x: x)`

Finds the minimum in an `Enumerable` collection. This is an executing function.

**Parameters**

__func__ : a `lambda` function used as a key selector to find the minimum over.

**Returns**

The minimum of the collection

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).min(lambda x: x['value'])
# 1

# For a string
Enumerable([
    'Alice',
    'Bob',
    'Zeke'
]).min()
# 'Alice'
</code></pre>