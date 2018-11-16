## skip

`skip(n)`

The skip method skips the first _n_ elements in a collection and returns the remaining elements. This method is not an executing function.

**Parameters:**

_n_: The number of elements to skip before returning the remaining elements.

**Returns:**

An `Enumerable` object whose elements are the ones remaining after skipping the first _n_ elements.

**Example**

<pre><code>
from py_linq import Enumerable

students = Enumerable([{ 'name': 'Joe Smith', 'mark': 80}, { 'name': 'Joanne Smith', 'mark': 90}])
joanne = students.skip(1).to_list() # results in { 'name': 'Joanne Smith', 'mark': 90}
</code></pre>