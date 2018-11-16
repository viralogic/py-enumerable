## add

`add(element)`

Adds an element to the `Enumerable` collection. This is not an executing function.

**Parameters**

__element__ - The element to add to the `Enumerable` collection.

**Returns**

An `Enumerable` instance with the added element.

**Note**

Please note that this method uses the [concat](https://github.com/viralogic/py-enumerable/wiki/Concat) method to add the element to the `Enumerable`. The `concat` method tries to enforce some crude type checking to ensure that the same type of elements are added to the `Enumerable` that could lead to linear time performance whenever `add` is called. For example,

<pre><code>

var students = Enumerable([21234, 76543]).add(23456).add(7893)

</code></pre>

would give O(2n) where n = 2 performance.

I am currently rethinking this strategy because of the performance hit and because type checking is not a necessity in Python.

**Example**

<pre><code>
from py_linq import Enumerable

students = Enumerable([{ 'name': 'Joe Smith', 'marks': [80, 90, 75]}, { 'name': 'Joanne Smith', 'marks': [67, 89, 91]}])
students.add({'name': 'John Deere', 'marks': [55, 56, 57]}) 
# students is now:
[
 { 'name': 'Joe Smith', 'marks': [80, 90, 75]},
 { 'name': 'Joanne Smith', 'marks': [67, 89, 91]},
 {'name': 'John Deere', 'marks': [55, 56, 57]}
]
</code></pre>