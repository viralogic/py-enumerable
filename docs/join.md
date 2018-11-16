## join

`join(inner_enumerable, outer_key=lambda x: x, inner_key=lambda x: x, result_func=lambda x: x)`

Returns an `Enumerable` that is the result of the inner equi-join between two `Enumerable` instances. This is not an executing function.

**Parameters**

__inner_enumerable__ : the inner `Enumerable` to join.<br>
__outer_key__ : lambda expression used to select the key of the outer `Enumerable` that will be used for the join<br>
__inner_key__ : lambda expression used to select the key of the inner `Enumerable` that will be used for the join<br>
__result_func__ : lambda expression used to create a result element from two matching elements.

**Returns**

An `Enumerable` that has elements transformed by __result_func__ that are obtained by performing an inner join on two sequences.

**Examples**

<pre><code>

from py_linq import Enumerable

marks1 = Enumerable([{ 'course' : 'Chemistry', 'mark': 90 }, {'course': 'Biology', 'mark': 85 }])
marks2 = Enumerable([{ 'course': 'Chemistry', 'mark': 65}, {'course': 'Computer Science', 'mark': 96 }])
chem_marks = marks1.join(marks2, lambda s1: s1['course'], lambda s2: s2['course'], lambda result: result) # [({ 'course' : 'Chemistry', 'mark': 90 }, { 'course': 'Chemistry', 'mark': 65})]
</code></pre>