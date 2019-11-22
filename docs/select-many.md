## select_many

`select_many(func=lambda x: x)`

Projects each element of a sequence to an IEnumerable<T> and flattens the resulting sequences into one sequence. This is not an executing function.

**Parameters:**

_func_: lambda expression that is the transform function to apply to each element.

**Returns:**

An `Enumerable` object whose elements whose elements are the result of invoking the one-to-many transform function on each element of the input sequence.

**Example**

<pre><code>
from py_linq import Enumerable

students = Enumerable([{ 'name': 'Joe Smith', 'marks': [80, 90, 75]}, { 'name': 'Joanne Smith', 'marks': [67, 89, 91]}])
marks = students.select_many(lambda x: x['marks']) # results in [80, 90, 75, 67, 89, 91]
</code></pre>

