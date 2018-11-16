## Select

`select(func=lambda x: x)`

The select method applies the _func_ lambda expression to each element in the `Enumerable` collection. This method is not an executing function.

**Parameters:**

_func_: lambda expression that is applies to each element in the `Enumerable` collection.

**Returns:**

An `Enumerable` object whose elements are the result of invoking the _func_ on each element.

**Example**

<pre><code>
from py_linq import Enumerable

students = Enumerable([{ 'name': 'Joe Smith', 'mark': 80}, { 'name': 'Joanne Smith', 'mark': 90}])
names = students.select(lambda x: x['name']) # results in ['Joe Smith', 'Joanne Smith']
</code></pre>

