## contains

`contains(element, key=lambda x: x)`

Determines if the given element is found in the `Enumerable`. Uses a `lambda` function as a key selector for membership comparison with the element. This is an executing function.

**Parameters**

__element__ : the object to test for membership in the collection.
__key__ : `lambda` function used as a selector for testing the element for membership in the `Enumerable` collection.

**Returns**

Boolean result if at least 1 element matches the given __element__ based on the __key__.

**Example**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).contains({'value' : 2}, lambda x: x['value'])
# True

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).contains({'value' : 0}, lambda x: x['value'])
# False
</code></pre>