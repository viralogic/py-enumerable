## reverse

`reverse()`

Inverts the order of the elements in an `Enumerable`. This is a non-executing function.

**Parameters**

**Returns**

An `Enumerable` with the element order reversed.

**Example**

<pre><code>
from py_linq import Enumerable

words = u"the quick brown fox jumps over the lazy dog".split(" ")
self.assertListEqual(words, ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"])
test = Enumerable(words).reverse()
self.assertEqual(u" ".join(test.to_list()), u"dog lazy the over jumps fox brown quick the")
</code></pre>