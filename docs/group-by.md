## group_by

`group_by(key_names=[], key=lambda x: x, result_func=lambda x: x)`

Groups an enumerable on given key selector and transforms the result. This is an executing function because it uses [itertools.groupby](https://docs.python.org/2/library/itertools.html#itertools.groupby) and the result of this function call is required to be saved to a `list` object for before being processed by the __result_func__ function.

**Parameters**

__key_names__ : list of key names
__key__ : key selector as a `lambda` function
__result_func__ : transformation function as a `lambda` function

**Returns**

An `Enumerable` of [`Grouping`](/py-enumerable/api/grouping) instances.

**Usage**

<pre><code>
Enumerable([1,2,3]).group_by(key_names=['id'], key=lambda x: x).to_list()
# [{'enumerable': '[1]', 'key': "{'id': 1}"}, {'enumerable': '[2]', 'key': "{'id': 2}"}, {'enumerable': '[3]', 'key': "{'id': 3}"}]
</code></pre>

Thus the key names for each grouping object can be referenced through the key property. Using the above example:

<pre><code>
Enumerable([1,2,3]).group_by(key_names=['id'], key=lambda x: x).select(lambda g: { 'key': g.key.id, 'count': g.count() }).to_list()
# [{'count': 1, 'key': 1}, {'count': 1, 'key': 2}, {'count': 1, 'key': 3}]
</code></pre>

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

Enumerable(locations).group_by(key_names=['country', 'city'], key=lambda x: [x[0], x[1]]).to_list()
"""
[
    {
        'enumerable': "[
            ('England', 'Liverpool', 'Branch1', 29700), 
            ('England', 'Liverpool', 'Branch2', 25000)
        ]", 
        'key': "{'country': 'England', 'city': 'Liverpool'}"
    }, 
    {
        'enumerable': "[
            ('England', 'London', 'Branch1', 90000), 
            ('England', 'London', 'Branch2', 80000), 
            ('England', 'London', 'Branch3', 70000)
        ]", 
        'key': "{'country': 'England', 'city': 'London'}"
    },
    {
        'enumerable': "[
            ('England', 'Manchester', 'Branch1', 45600),
            ('England', 'Manchester', 'Branch2', 50000)
        ]",
        'key': "{'country': 'England', 'city': 'Manchester'}"
    }, 
    {
        'enumerable': "[
            ('Scotland', 'Edinburgh', 'Branch1', 20000)
        ]", 
        'key': "{'country': 'Scotland', 'city': 'Edinburgh'}"
    }, 
    {
        'enumerable': "[
            ('Scotland', 'Glasgow', 'Branch1', 12500), 
            ('Scotland', 'Glasgow', 'Branch2', 12000)
        ]",
        'key': "{'country': 'Scotland', 'city': 'Glasgow'}"
    },
    {
        'enumerable': "[
            ('Wales', 'Bangor', 'Branch1', 12800)
        ]",
        'key': "{'country': 'Wales', 'city': 'Bangor'}"
    }, 
    {
        'enumerable': "[
            ('Wales', 'Cardiff', 'Branch1', 29700),
            ('Wales', 'Cardiff', 'Branch2', 30000)
        ]", 
        'key': "{'country': 'Wales', 'city': 'Cardiff'}"
    }
]
"""
</code></pre>