## group_join

`group_by(self, inner_enumerable, outer_key=lambda x: x, inner_key=lambda x: x, result_func=lambda x: x)`

Correlates the elements of two `Enumerable` collections based on key equality and groups the results. This is not an executing function.

**Parameters**

__inner_enumerable__ : the `Enumerable` to join to the first collection
__outer_key__ : a `lambda` function to extract the join key from each element of the first collection
__inner_key__ : a `lambda` function to extract the join key from each element of the __inner_enumerable__.
__result_func__ : a `lambda` function to create a result element from an element of the first collection and a collection of matching elements from __inner_enumerable__

**Returns**

An `Enumerable` of elements of structure obtained by __result_func__.

**Examples**

<pre><code>
from py_linq import Enumerable

Enumerable([
    {'value': 1},
    {'value': 2},
    {'value': 3}
]).group_join(
    Enumerable([1, 2, 3]),
    outer_key=lambda x: x['value'],
    inner_key=lambda x: x,
    result_func=lambda (x, y): {
        'inner': x,
        'outer': y.to_list()
    }
).to_list()
# [{'outer': [1], 'inner': {'value': 1}}, {'outer': [2], 'inner': {'value': 2}}, {'outer': [3], 'inner': {'value': 3}}]
</code></pre>