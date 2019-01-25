## concat

`concat(enumerable)`

Concatenates two `Enumerable` instances together. Concat not an executing function.

**Parameters**

__enumerable__ - A second `Enumerable` to add to an `Enumerable` collection.

**Returns**

An `Enumerable` instance with the concatenated collections.

**Example**

<pre><code>
from py_linq import Enumerable

students = Enumerable([{ 'name': 'Joe Smith', 'marks': [80, 90, 75]}, { 'name': 'Joanne Smith', 'marks': [67, 89, 91]}])
marks = students.select_many(lambda x: x['marks])
marks.concat(Enumerable([55, 56, 57])) # marks is [80, 90, 75, 67, 89, 91, 55, 56, 57]

</code></pre>