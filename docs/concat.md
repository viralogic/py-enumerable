## concat

`concat(enumerable)`

Concatenates two `Enumerable` instances together. Concat not an executing function.

**Parameters**

__enumerable__ - A second `Enumerable` to add to an `Enumerable` collection.

**Returns**

An `Enumerable` instance with the concatenated collections.

**Note**

The `concat` method tries to enforce some crude type checking to ensure that the same type of elements are added to the `Enumerable` that could lead to linear time performance for every element added to the collection. For example,

<pre><code>
var students = Enumerable([21234, 76543]).concat(Enumerable([23456, 7893])
</code></pre>

would give O(2n) where n = 2 performance once `concat` is called.

I am currently rethinking this strategy because of the performance hit and because type checking is not a necessity in Python.

**Example**

<pre><code>
from py_linq import Enumerable

students = Enumerable([{ 'name': 'Joe Smith', 'marks': [80, 90, 75]}, { 'name': 'Joanne Smith', 'marks': [67, 89, 91]}])
marks = students.select_many(lambda x: x['marks])
marks.concat(Enumerable([55, 56, 57])) # marks is [80, 90, 75, 67, 89, 91, 55, 56, 57]

</code></pre>