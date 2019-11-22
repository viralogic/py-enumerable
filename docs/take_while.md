## take_while

`take_while(predicate)`

Returns elements from an `Enumerable` as long as a specified condition is true, and then skips the remaining elements. This is not an executing function.

**Parameters**

__predicate__: a function to test each element for a condition

**Returns**

An `Enumerable` that contains the elements from the input sequence that occur before the element at which the test no longer passes.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable([1, 4, 6, 4, 1]).take_while(lambda x: x < 5)
# [1, 4]
</code></pre>