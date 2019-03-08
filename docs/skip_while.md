## skip_while

`skip_while(predicate)`

Bypasses elements in an input `Enumerable` as long as a specified condition is true and then returns the remaining elements.

**Parameters**

__predicate__: a function to test each element for a condition

**Returns**

An `Enumerable` that contains the elements from the input sequence starting at the first element in the linear series that does not pass the test specified by the given predicate.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable([1, 4, 6, 4, 1]).skip_while(lambda x: x < 5)
# [6, 4, 1]
</code></pre>