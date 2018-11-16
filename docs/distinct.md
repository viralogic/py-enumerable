## distinct

`distinct(key=lambda x: x)`

Returns an `Enumerable` containing elements that are distinct based on a given key selector. This is an executing function.

**Parameters**

__key__ : `lambda` function used for selecting the key to compare.

**Returns**

An `Enumerable` object that contains only distinct elements based on the given key selector. If an element is not considered unique based on the given key selector, then the first match is returned in the new Enumerable. This is an executing function.

**Examples**

<pre><code>
from py_linq import Enumerable
locations = [
    ('Scotland', 'Edinburgh', 'Branch1', 20000),
    ('Scotland', 'Glasgow', 'Branch1', 12500),
    ('Scotland', 'Glasgow', 'Branch2', 12000),
    ('Wales', 'Cardiff', 'Branch1', 29700),
    ('Wales', 'Cardiff', 'Branch2', 30000),
    ('Wales', 'Bangor', 'Branch1', 12800),
    ('England', 'London', 'Branch1', 90000),
    ('England', 'London', 'Branch2', 80000),
    ('England', 'London', 'Branch3', 70000),
    ('England', 'Manchester', 'Branch1', 45600),
    ('England', 'Manchester', 'Branch2', 50000),
    ('England', 'Liverpool', 'Branch1', 29700),
    ('England', 'Liverpool', 'Branch2', 25000)
]

# Find distinct based on country. Will grab the first match.
Enumerable(locations).distinct(lambda x: x[0]).to_list()

"""
[
    ('England', 'London', 'Branch1', 90000),
    ('Scotland', 'Edinburgh', 'Branch1', 20000),
    ('Wales', 'Cardiff', 'Branch1', 29700)
]
"""

</code></pre>