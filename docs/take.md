## take

`take(n)`

The take method returns a specified number of contiguous elements from the start of a sequence. This method is not an executing function.

**Parameters:**

_n_: The number of contiguous elements to return.

**Returns:**

An `Enumerable` object that contains the specified number of elements from the start of the input sequence.

**Example**

<pre><code>
from py_linq import Enumerable

students = Enumerable([{ 'name': 'Joe Smith', 'mark': 80}, { 'name': 'Joanne Smith', 'mark': 90}])
joe = students.take(1).to_list() # results in { 'name': 'Joe Smith', 'mark': 80}
</code></pre>