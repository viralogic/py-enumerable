## range

`range(i, n)`

Generates a sequence of `n` integral numbers starting from `i`.

**Parameters**

__i__ : the value of the first number in the sequence<br>
__n__ : the number of sequential integers to generate

**Returns**

An `Enumerable` collection of `n` sequential integers that start from `i`.

**Example**

<pre><code>
from py_linq import Enumerable

test = Enumerable.range(1, 3)
# [1, 2, 3]
</code></pre>