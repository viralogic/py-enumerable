## where

`where(predicate)`

The where method applies the _predicate_ lambda expression as a filter in the `Enumerable` collection. This method is not an executing function.

**Parameters:**

_predicate_: lambda expression that is used to test each element for a condition.

**Returns:**

An `Enumerable` object that contains elements from the input sequence that satisfy the condition.

**Example**

<pre><code>
from py_linq import Enumerable

marks = Enumerable([25, 49, 50, 80, 90])
passing = marks.where(lambda x: x >= 50) # results in [50, 80, 90]
</code></pre>