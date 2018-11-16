## intersect

`intersect(enumerable, key=lambda x: x)`

Returns an `Enumerable` that is the result of an intersection between two `Enumerable` instance based on the value of the key given. This is not an executing function.

**Parameters**

__enumerable__ : an `Enumerable` instance to intersect with.
__key__ : `lambda` function used as the key selector for both sets

**Returns**

An `Enumerable` object that contains the common elements between the two `Enumerables` based on the given key.

**Examples**

<pre><code>
from py_linq import Enumerable

marks1 = Enumerable([{ 'course' : 'Chemistry', 'mark': 90 }, {'course': 'Biology', 'mark': 85 }])
marks2 = Enumerable([{ 'course': 'Chemistry', 'mark': 65}, {'course': 'Computer Science', 'mark': 96 }])
common_courses = marks1.intersect(marks2, lambda c: c['course'])

</code></pre>

