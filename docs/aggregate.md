## aggregate

`aggregate(func, seed=None)`

Applies an accumulator function over an `Enumerable`. The specified seed value is used as the initial accumulator value, and the specified function is used to select the result value.

**Parameters**

__func__ : the accumulator function to be performed on each element

__seed__ : the initial accumulator value

**Returns**

The result of the accumulator function over the sequence

**Example**

<pre><code>
from py_linq import Enumerable
def reverse(self, result, element):
        return element + " " + result
words = u"the quick brown fox jumps over the lazy dog".split(" ")
test = Enumerable(words).aggregate(self.reverse)

# "dog lazy the over jumps fox brown quick the"
</code></pre>