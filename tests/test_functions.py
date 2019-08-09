from unittest import TestCase
from py_linq import Enumerable
from tests import _empty, _simple, _complex, _locations
from py_linq.exceptions import NoElementsError, NullArgumentError, \
    NoMatchingElement, MoreThanOneMatchingElement


class TestFunctions(TestCase):
    def setUp(self):
        self.empty = Enumerable(_empty)
        self.simple = Enumerable(_simple)
        self.complex = Enumerable(_complex)

    def test_to_list(self):
        self.assertListEqual(
            self.empty.to_list(),
            _empty,
            u"Empty to_list not correct")
        self.assertListEqual(
            self.simple.to_list(),
            _simple,
            u"Simple to_list not correct")
        self.assertListEqual(
            self.complex.to_list(),
            _complex,
            u"Complex to_list not correct")

    def test_sum(self):
        self.assertEqual(
            self.empty.sum(),
            0,
            u"Sum of empty enumerable should be 0")
        self.assertEqual(
            self.simple.sum(),
            6,
            u"Sum of simple enumerable should be 6")
        self.assertEqual(
            self.complex.sum(lambda x: x['value']),
            6,
            u"Sum of complex enumerable should be 6")

    def test_count(self):
        self.assertEqual(self.empty.count(), 0)
        self.assertEqual(self.empty.count(lambda x: x == 1), 0)

        self.assertEqual(self.simple.count(), 3)
        self.assertEqual(self.simple.count(lambda x: x == 1), 1)

        self.assertEqual(self.complex.count(), 3)
        self.assertEqual(self.complex.count(lambda x: x["value"] > 1), 2)

    def test_select(self):
        self.assertEqual(
            self.empty.select(lambda x: x['value']).count(),
            0,
            u"Empty enumerable should still have 0 elements")

        simple_select = self.simple.select(lambda x: {'value': x})
        self.assertDictEqual(
            simple_select.first(),
            {'value': 1},
            u"Transformed simple enumerable element is dictionary")
        self.assertEqual(
            simple_select.count(),
            3,
            u"Transformed simple enumerable has 3 elements")

        complex_select = self.complex.select(lambda x: x['value'])
        self.assertEqual(
            complex_select.count(),
            3, u"Transformed complex enumerable has 3 elements")
        self.assertIsInstance(
            complex_select.first(),
            int,
            u"Transformed complex enumerable element is integer"
        )

    def test_max_min(self):
        self.assertRaises(NoElementsError, self.empty.min)
        self.assertEqual(
            self.simple.min(),
            1,
            u"Minimum value of simple enumerable is 1")
        self.assertEqual(
            self.complex.min(lambda x: x['value']),
            1,
            u"Min value of complex enumerable is 1"
        )

        self.assertRaises(NoElementsError, self.empty.max)
        self.assertEqual(
            self.simple.max(),
            3,
            u"Max value of simple enumerable is 3")
        self.assertEqual(
            self.complex.max(lambda x: x['value']),
            3,
            u"Max value of complex enumerable is 3")

    def test_avg(self):
        avg = float(2)
        self.assertRaises(NoElementsError, self.empty.avg)
        self.assertEqual(
            self.simple.avg(),
            avg,
            u"Avg value of simple enumerable is {0:.5f}".format(avg))
        self.assertEqual(
            self.complex.avg(lambda x: x['value']),
            avg,
            u"Avg value of complex enumerable is {0:.5f}".format(avg))

    def test_first_last(self):
        self.assertRaises(NoElementsError, self.empty.first)
        self.assertEqual(
            self.empty.first_or_default(),
            None,
            u"First or default should be None")
        self.assertIsInstance(
            self.simple.first(),
            int,
            u"First element in simple enumerable is int")
        self.assertEqual(
            self.simple.first(),
            1,
            u"First element in simple enumerable is 1")
        self.assertEqual(
            self.simple.first(),
            self.simple.first_or_default(),
            u"First and first or default should equal")
        self.assertIsInstance(
            self.complex.first(),
            dict,
            u"First element in complex enumerable is dict")
        self.assertDictEqual(
            self.complex.first(),
            {'value': 1},
            u"First element in complex enumerable is not correct dict")
        self.assertDictEqual(
            self.complex.first(),
            self.complex.first_or_default(),
            u"First and first or default should equal")
        self.assertEqual(
            self.simple.first(),
            self.complex.select(lambda x: x['value']).first(),
            u"First values in simple and complex should equal")

        self.assertRaises(NoElementsError, self.empty.last)
        self.assertEqual(
            self.empty.last_or_default(),
            None,
            u"Last or default should be None")
        self.assertIsInstance(
            self.simple.last(),
            int,
            u"Last element in simple enumerable is int")
        self.assertEqual(
            self.simple.last(),
            3,
            u"Last element in simple enumerable is 3")
        self.assertEqual(
            self.simple.last(),
            self.simple.last_or_default(),
            u"Last and last or default should equal")
        self.assertIsInstance(
            self.complex.last(),
            dict,
            u"Last element in complex enumerable is dict")
        self.assertDictEqual(
            self.complex.last(),
            {'value': 3},
            u"Last element in complex enumerable is not correct dict")
        self.assertDictEqual(
            self.complex.last(),
            self.complex.last_or_default(),
            u"Last and last or default should equal")
        self.assertEqual(
            self.simple.last(),
            self.complex.select(lambda x: x['value']).last(),
            u"Last values in simple and complex should equal")

    def test_sort(self):
        self.assertRaises(NullArgumentError, self.simple.order_by, None)
        self.assertRaises(
            NullArgumentError,
            self.simple.order_by_descending,
            None)

        self.assertListEqual(
            self.simple.order_by(lambda x: x).to_list(),
            self.simple.to_list(),
            u"Simple enumerable sort ascending should yield same list")
        self.assertListEqual(
            self.simple.order_by_descending(lambda x: x).to_list(),
            sorted(self.simple, key=lambda x: x, reverse=True),
            u"Simple enumerable sort descending should yield reverse list")

        self.assertListEqual(
            self.complex.order_by(lambda x: x['value']).to_list(),
            self.complex.to_list(),
            u"Complex enumerable sort ascending should yield same list")
        self.assertListEqual(
            self.complex.order_by_descending(lambda x: x['value']).to_list(),
            sorted(self.complex, key=lambda x: x['value'], reverse=True),
            u"Complex enumerable sort descending should yield reverse list")

        self.assertListEqual(
            self.simple.order_by(lambda x: x).to_list(),
            self.complex.select(
                lambda x: x['value']
            ).order_by(lambda x: x).to_list(),
            u"Projection and sort ascending of complex should yield simple")

    def test_median(self):
        self.assertRaises(NoElementsError, self.empty.median)

        median = float(2)
        self.assertEqual(
            self.simple.median(),
            median,
            u"Median of simple enumerable should be {0:.5f}".format(median))
        self.assertEqual(
            self.complex.median(lambda x: x['value']),
            median,
            u"Median of complex enumerable should be {0:.5f}".format(median))

    def test_skip_take(self):
        self.assertListEqual(
            self.empty.skip(2).to_list(),
            [],
            u"Skip 2 of empty list should yield empty list")
        self.assertListEqual(
            self.empty.take(2).to_list(),
            [],
            u"Take 2 of empty list should yield empty list")
        self.assertListEqual(
            self.simple.skip(3).to_list(),
            [],
            u"Skip 3 of simple enumerable should yield empty list")
        self.assertListEqual(
            self.simple.take(4).to_list(),
            _simple,
            u"Take 4 of simple enumerable should yield simple list")

        self.assertEqual(
            self.simple.skip(1).take(1).first(),
            2,
            u"Skip 1 and take 1 of simple should yield 2")
        self.assertEqual(
            self.complex.select(lambda x: x['value']).skip(1).take(1).first(),
            2,
            u"Skip 1 and take 1 of complex with projection should yield 2")

    def test_filter(self):
        self.assertListEqual(
            self.empty.where(lambda x: x == 0).to_list(),
            [],
            u"Filter on empty list should yield empty list")
        self.assertListEqual(
            self.simple.where(lambda x: x == 2).to_list(),
            [2],
            u"Filter where element equals 2 should yield list with 1 element")
        self.assertListEqual(
            self.complex.where(lambda x: x['value'] == 2).to_list(),
            [{'value': 2}],
            u"Filter where element value is 2 should give list with 1 element")
        self.assertListEqual(
            self.complex.where(lambda x: x['value'] == 2)
                .select(lambda x: x['value'])
                .to_list(),
            self.simple.where(lambda x: x == 2).to_list(),
            u"Should equal filter of simple enumerable")
        self.assertListEqual(
            self.simple.where(lambda x: x == 0).to_list(),
            self.empty.to_list(),
            u"Should yield an empty list")

    def test_single_single_or_default(self):
        self.assertRaises(NoMatchingElement, self.empty.single, lambda x: x == 0)
        self.assertRaises(NoMatchingElement, self.empty.single, None)

        self.assertRaises(NoMatchingElement, self.simple.single, lambda x: x == 0)
        self.assertRaises(MoreThanOneMatchingElement, self.simple.single, None)

        self.assertRaises(NoMatchingElement, self.complex.single, lambda x: x['value'] == 0)
        self.assertRaises(MoreThanOneMatchingElement, self.complex.single, None)

        self.assertRaises(MoreThanOneMatchingElement, self.simple.single, lambda x: x > 0)
        self.assertRaises(MoreThanOneMatchingElement, self.complex.single, lambda x: x['value'] > 0)

        self.assertRaises(MoreThanOneMatchingElement, self.simple.single_or_default, lambda x: x > 0)
        self.assertIsNone(self.simple.single_or_default(lambda x: x > 3))

        self.assertRaises(MoreThanOneMatchingElement, self.complex.single_or_default, lambda x: x['value'] > 0)

        simple_single = self.simple.single(lambda x: x == 2)
        self.assertIsInstance(simple_single, int)
        self.assertEqual(simple_single, 2)

        complex_single = self.complex.single(lambda x: x['value'] == 2)
        self.assertIsInstance(complex_single, dict)
        self.assertDictEqual(complex_single, {'value': 2})
        self.assertEqual(simple_single, self.complex.select(lambda x: x['value']).single(lambda x: x == 2))

    def test_select_many(self):
        empty = Enumerable([[], [], []])
        simple = Enumerable([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        __complex = Enumerable(
            [
                {'key': 1, 'values': [1, 2, 3]},
                {'key': 2, 'values': [4, 5, 6]},
                {'key': 3, 'values': [7, 8, 9]}
            ]
        )

        self.assertListEqual(
            empty.select_many().to_list(),
            [],
            u"Should yield empty list")
        self.assertListEqual(
            simple.select_many().to_list(),
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            u"Should yield simple enumerable with single list")
        self.assertListEqual(
            __complex.select_many(lambda x: x['values']).to_list(),
            simple.select_many().to_list(),
            u"Should yield simple enumerable with single list")

    def test_concat(self):
        self.assertListEqual(
            self.empty.concat(self.empty).to_list(),
            [],
            u"Concatenation of 2 empty lists gives empty list")
        self.assertListEqual(
            self.empty.concat(self.simple).to_list(),
            _simple,
            u"Concatenation of empty to simple yields simple")
        self.assertListEqual(
            self.simple.concat(self.empty).to_list(),
            _simple,
            u"Concatenation of simple to empty yields simple")

    def test_group_by(self):
        simple_grouped = self.simple.group_by(key_names=['id'])
        self.assertEqual(
            simple_grouped.count(),
            3,
            u"Three grouped elements in simple grouped")
        for g in simple_grouped:
            self.assertEqual(
                g.key.id,
                g.first(),
                u"Each id in simple grouped should match first value")

        complex_grouped = self.complex.group_by(
            key_names=['value'],
            key=lambda x: x['value'])
        self.assertEqual(
            complex_grouped.count(),
            3,
            u"Three grouped elements in complex grouped")
        for g in complex_grouped:
            self.assertEqual(
                g.key.value,
                g.select(lambda x: x['value']).first(),
                u"Each value in complex grouped should mach first value")

        locations_grouped = Enumerable(_locations) \
            .group_by(
            key_names=['country', 'city'],
            key=lambda x: [x[0], x[1]])
        self.assertEqual(
            locations_grouped.count(),
            7,
            u"Seven grouped elements in locations grouped")

        london = locations_grouped \
            .single(
                lambda c: c.key.city == 'London' and c.key.country == 'England'
            )
        self.assertEqual(
            london.sum(lambda c: c[3]),
            240000,
            u"Sum of London, England location does not equal")

    def test_distinct(self):
        self.assertListEqual(
            self.empty.distinct().to_list(),
            [],
            u"Distinct empty enumerable yields empty list")
        self.assertListEqual(
            self.simple.concat(self.simple).distinct().to_list(),
            _simple,
            u"Distinct yields simple list")
        locations = Enumerable(_locations).distinct(lambda x: x[0])
        self.assertEqual(
            locations.count(),
            3,
            u"Three distinct countries in locations enumerable")
        self.assertListEqual(
            locations.to_list(),
            [
                ('England', 'London', 'Branch1', 90000),
                ('Scotland', 'Edinburgh', 'Branch1', 20000),
                ('Wales', 'Cardiff', 'Branch1', 29700)
            ],
            u"Distinct locations do not match")

    def test_default_if_empty(self):
        self.assertListEqual(
            self.empty.default_if_empty().to_list(),
            [None],
            u"Should yield None singleton")
        self.assertListEqual(
            self.simple.default_if_empty().to_list(),
            _simple,
            u"Default if empty of simple enumerable should yield simple list")
        self.assertListEqual(
            self.complex.default_if_empty().to_list(),
            _complex,
            u"Should yield complex list")

    def test_any(self):
        self.assertFalse(self.empty.any(lambda x: x == 1))
        self.assertFalse(self.empty.any())

        self.assertTrue(self.simple.any(lambda x: x == 1))
        self.assertTrue(self.simple.any())

        self.assertTrue(self.complex.any())
        self.assertFalse(self.complex.any(lambda x: x['value'] < 1))
        self.assertTrue(self.complex.any(lambda x: x['value'] >= 1))

    def test_contains(self):
        self.assertFalse(
            self.empty.contains(1),
            u"Empty enumerable should not contain 1 as element")
        self.assertTrue(
            self.simple.contains(1),
            u"Simple enumerable should contain 1 as element")
        self.assertTrue(
            self.complex.select(lambda x: x['value']).contains(1),
            u"Complex enumerable should contain 1 as an element value")

    def test_intersect(self):
        self.assertRaises(TypeError, self.empty.intersect, [])
        self.assertListEqual(
            self.empty.intersect(self.empty).to_list(),
            [],
            u"Intersect of two empty enumerables yield empty list")
        self.assertListEqual(
            self.empty.intersect(self.simple).to_list(),
            [],
            u"Intersect of empty and simple enumerables yields empty list")
        self.assertListEqual(
            self.simple.intersect(self.simple).to_list(),
            _simple,
            u"Intersect of two simple enumerables yields simple list")
        self.assertListEqual(
            self.simple.intersect(Enumerable([2])).to_list(),
            [2],
            u"Intersect of simple enumerable and [2] yields [2]")
        self.assertListEqual(
            self.simple.intersect(self.complex).to_list(),
            [],
            u"Intersect of simple and complex enumerable yields empty list")
        self.assertListEqual(
            self.complex.intersect(self.complex).to_list(),
            _complex,
            u"Intersect of two complex enumeraable yields complex list")
        self.assertListEqual(
            self.complex.intersect(Enumerable([{'value': 1}])).to_list(),
            [{'value': 1}],
            "Should yield {'value': 1}")

    def test_except(self):
        self.assertRaises(TypeError, self.empty.except_, [])
        self.assertListEqual(
            self.empty.except_(self.empty).to_list(),
            [],
            u"Complement of two empty enumerables yields empty list")
        self.assertListEqual(
            self.empty.except_(self.simple).to_list(),
            [],
            u"Complement of empty and simple enumerables yields empty list")
        self.assertListEqual(
            self.simple.except_(self.empty).to_list(),
            _simple,
            u"Complement of simple and empty enumerables yields simple list")
        self.assertListEqual(
            self.simple.except_(self.simple).to_list(),
            [],
            u"Complement of simple and simple enumerables yields empty list")
        self.assertListEqual(
            self.simple.except_(Enumerable([2])).to_list(),
            [1, 3],
            u"Complement of simple and [2] yields [1,3]")
        self.assertListEqual(
            self.simple.except_(self.complex).to_list(),
            _simple,
            u"Complement of simple and complex yields simple")
        self.assertListEqual(
            self.complex.except_(self.simple).to_list(),
            _complex,
            u"Complement of complex and simple yields complex")
        self.assertListEqual(
            self.complex.except_(self.complex).to_list(),
            [],
            u"Complement of complex and complex yields empty")
        self.assertListEqual(
            self.complex.except_(Enumerable([{'value': 1}])).to_list(),
            [{'value': 2}, {'value': 3}],
            "Should yield [{'value': 2}, 'value': 3]")

    def test_marks_intersect(self):
        marks1 = Enumerable([{'course': 'Chemistry', 'mark': 90}, {'course': 'Biology', 'mark': 85}])
        marks2 = Enumerable([{'course': 'Chemistry', 'mark': 65}, {'course': 'Computer Science', 'mark': 96}])
        self.assertListEqual(
            marks1.intersect(marks2, lambda c: c['course']).to_list(),
            [{'course': 'Chemistry', 'mark': 90}]
        )

    def test_marks_except(self):
        marks1 = Enumerable([{'course': 'Chemistry', 'mark': 90}, {'course': 'Biology', 'mark': 85}])
        marks2 = Enumerable([{'course': 'Chemistry', 'mark': 65}, {'course': 'Computer Science', 'mark': 96}])
        self.assertListEqual(
            marks1.except_(marks2, lambda c: c['course']).to_list(),
            [{'course': 'Biology', 'mark': 85}]
        )

    def test_union(self):
        self.assertListEqual(
            self.empty.union(self.empty).to_list(),
            [],
            u"Union of two empty enumerables yields empty list")
        self.assertListEqual(
            self.empty.union(self.simple).to_list(),
            _simple,
            u"Union of empty and simple yield simple")
        self.assertListEqual(
            self.simple.union(self.empty).to_list(),
            _simple,
            u"Union of simple and empty yield simple")
        self.assertListEqual(
            self.empty.union(self.complex).to_list(),
            _complex,
            u"Union of empty and complex yield complex")
        self.assertListEqual(
            self.complex.union(self.empty).to_list(),
            _complex,
            u"Union of complex and empty yield complex")

        simple_extended = _simple + [4, 5]
        self.assertListEqual(
            self.simple.union(Enumerable([4, 5])).to_list(),
            simple_extended,
            u"Union of simple and [4,5] yield simple + [4,5]")
        self.assertListEqual(
            self.simple.union(Enumerable([1, 4, 5]))
                .order_by(lambda x: x).to_list(),
            simple_extended,
            u"Union of simple and [1,4,5] yield simple + [4,5]")

        complex_extended = _complex + [{'value': 4}, {'value': 5}]
        self.assertListEqual(
            self.complex.union(
                Enumerable([{'value': 4}, {'value': 5}]),
                lambda x: x['value']).to_list(),
            complex_extended,
            u"Should yield complex + [{'value': 4}, {'value': 5}]")
        self.assertListEqual(
            self.complex.union(
                Enumerable([{'value': 1}, {'value': 4}, {'value': 5}]),
                lambda x: x['value']).order_by(lambda x: x['value']).to_list(),
            complex_extended,
            u"Should yield complex + [{'value': 4}, {'value': 5}]")

    def test_join(self):
        self.assertRaises(TypeError, self.empty.join, [])
        self.assertListEqual(
            self.empty.join(self.empty).to_list(),
            [],
            u"Joining 2 empty lists should yield empty list")
        self.assertListEqual(
            self.empty.join(self.simple).to_list(),
            [],
            u"Joining empty to simple yields empty list")
        self.assertListEqual(
            self.empty.join(self.complex).to_list(),
            [],
            u"Joining complex to simple yields empty list")

        self.assertListEqual(
            self.simple.join(self.empty).to_list(),
            [],
            u"Joining simple to empty yields empty list")
        self.assertListEqual(
            self.simple.join(self.simple)
                .order_by(lambda x: (x[0], x[1])).to_list(),
            [(1, 1), (2, 2), (3, 3)],
            u"Joining simple to simple yields [(1,1), (2,2), (3,3)]")
        self.assertListEqual(
            self.simple.join(
                self.complex,
                inner_key=lambda x: x['value'],
                result_func=lambda x: (x[0], x[1]['value'])).order_by(
                lambda x: (x[0], x[1])
            ).to_list(),
            [(1, 1), (2, 2), (3, 3)],
            u"Should yield [(1,1), (2,2), (3,3)]")

        self.assertListEqual(
            self.complex.join(
                self.complex,
                result_func=lambda x: (x[0]['value'], x[1]['value'])).order_by(
                    lambda x: (x[0], x[1])).to_list(),
            [(1, 1), (2, 2), (3, 3)],
            u"Should yield [(1,1), (2,2), (3,3)]")

    def test_group_join(self):
        self.assertRaises(TypeError, self.empty.group_join, [])
        self.assertListEqual(
            self.empty.group_join(self.empty).to_list(),
            [],
            u"Group join 2 empty yields empty")

        simple_empty_gj = self.simple.group_join(self.empty)
        self.assertEqual(
            simple_empty_gj.count(),
            3,
            u"Should have 3 elements")
        for i, e in enumerate(simple_empty_gj):
            self.assertEqual(
                e[0],
                i + 1,
                u"number property should be {0}".format(i + 1))
            self.assertEqual(
                e[1].count(),
                0,
                u"Should have 0 elements")
            self.assertEqual(
                e[1].first_or_default(),
                None,
                u"Value of first element should be None")

        simple_gj = self.simple.group_join(
            self.simple,
            result_func=lambda x: {
                'number': x[0],
                'collection': x[1]
            })
        for i, e in enumerate(simple_gj):
            self.assertEqual(
                e['number'],
                i + 1,
                u"number property should be {0}".format(i + 1))
            self.assertEqual(
                e['collection'].count(),
                1,
                u"Should only have one element")
            self.assertEqual(
                e['collection'].first(),
                i + 1,
                u"Value of first element should equal {0}".format(i + 1))

        complex_simple_gj = self.complex.group_join(
            self.simple,
            outer_key=lambda x: x['value'])
        for i, e in enumerate(complex_simple_gj):
            self.assertEqual(
                e[0]['value'],
                i + 1,
                u"value property of each element should be {0}".format(i + 1))
            self.assertEqual(
                e[1].count(),
                1,
                u"Should only have one element")
            self.assertEqual(
                e[1].first(),
                i + 1,
                u"Value of first element should equal {0}".format(i + 1))

        simple_gj = self.simple.group_join(
            Enumerable([2, 3]),
            result_func=lambda x: {
                'number': x[0],
                'collection': x[1]
            }).to_list()
        self.assertEqual(
            len(simple_gj),
            3,
            u"Should be 3 elements")
        for i, e in enumerate(simple_gj):
            self.assertEqual(
                e['number'],
                i + 1,
                u"number property should be {0}".format(i + 1))
            self.assertEqual(
                e['collection'].count(),
                0 if i == 0 else 1,
                u"should have {0} element(s)".format(0 if i == 0 else 1))
            self.assertListEqual(
                e['collection'].to_list(),
                [] if i == 0 else [i + 1],
                u"Collection should equal {0}".format(
                    [] if i == 0 else [i + 1])
            )

    def test_then_by(self):
        locations = Enumerable(_locations)
        self.assertListEqual(
            locations.order_by(lambda l: l[0])
            .then_by(lambda l: l[1])
            .select(lambda l: u"{0}, {1}".format(l[1], l[0]))
            .to_list(),
            [
                u'Liverpool, England',
                u'Liverpool, England',
                u'London, England',
                u'London, England',
                u'London, England',
                u'Manchester, England',
                u'Manchester, England',
                u'Edinburgh, Scotland',
                u'Glasgow, Scotland',
                u'Glasgow, Scotland',
                u'Bangor, Wales',
                u'Cardiff, Wales',
                u'Cardiff, Wales'
            ],
            u"then_by locations ordering is not correct")
        self.assertRaises(
            NullArgumentError,
            locations.order_by(lambda l: l[0]).then_by,
            None)

    def test_then_by_descending(self):
        locations = Enumerable(_locations)
        self.assertListEqual(
            locations.order_by(lambda l: l[0])
            .then_by(lambda l: l[1])
            .then_by_descending(lambda l: l[3])
            .select(lambda l: u"{0}, {1}: {2}".format(
                l[1], l[0], l[3]
            ))
            .to_list(),
            [
                u'Liverpool, England: 29700',
                u'Liverpool, England: 25000',
                u'London, England: 90000',
                u'London, England: 80000',
                u'London, England: 70000',
                u'Manchester, England: 50000',
                u'Manchester, England: 45600',
                u'Edinburgh, Scotland: 20000',
                u'Glasgow, Scotland: 12500',
                u'Glasgow, Scotland: 12000',
                u'Bangor, Wales: 12800',
                u'Cardiff, Wales: 30000',
                u'Cardiff, Wales: 29700'
            ],
            u"then_by_descending ordering is not correct"
        )

    def reverse(self, result, element):
        return element + " " + result

    def sum(self, result, element):
        return result + element

    def test_aggregate(self):
        words = u"the quick brown fox jumps over the lazy dog".split(" ")
        self.assertListEqual(words, ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"])
        test = Enumerable(words).aggregate(self.reverse)
        self.assertEqual(test, "dog lazy the over jumps fox brown quick the")

        self.assertRaises(NoElementsError, Enumerable().aggregate, [lambda x: x[0] + x[1], 0])

        test = self.simple.aggregate(self.sum, seed=0)
        self.assertEqual(test, 6)

    def test_all(self):
        test = Enumerable([1, 1, 1]).all(lambda x: x == 1)
        self.assertTrue(test)

        test = Enumerable([]).all(lambda x: x == 1)
        self.assertTrue(test)

        test = self.simple.all(lambda x: x == 1)
        self.assertFalse(test)

    def test_append(self):
        test = self.simple.append(4)
        self.assertEqual(test.count(), 4)
        self.assertEqual(test.element_at(3), 4)

    def test_prepend(self):
        test = self.simple.prepend(4)
        self.assertEqual(test.count(), 4)
        self.assertEqual(test.element_at(0), 4)

    def test_empty(self):
        test = Enumerable.empty()
        self.assertIsInstance(test, Enumerable)
        self.assertEqual(test.count(), 0)

    def test_range(self):
        test = Enumerable.range(1, 3)
        self.assertEqual(test.count(), 3)
        self.assertListEqual(self.simple.to_list(), test.to_list())

    def test_repeat(self):
        test = Enumerable.repeat(u'Z', 10)
        self.assertEqual(test.count(), 10)
        self.assertEqual(u"".join(test.to_list()), u'ZZZZZZZZZZ')

    def test_reverse(self):
        test = self.empty.reverse()
        self.assertListEqual(test.to_list(), [])

        test = self.simple.reverse()
        self.assertListEqual(test.to_list(), [3, 2, 1])

        words = u"the quick brown fox jumps over the lazy dog".split(" ")
        self.assertListEqual(words, ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"])
        test = Enumerable(words).reverse()
        self.assertEqual(u" ".join(test.to_list()), u"dog lazy the over jumps fox brown quick the")

    def test_skip_last(self):
        test = Enumerable([1, 2, 3, 4, 5]).skip_last(2)
        self.assertListEqual(test.to_list(), [1, 2, 3])

        test = Enumerable(["one", "two", "three", "four", "five"]).skip(1).skip_last(1)
        self.assertListEqual(test.to_list(), ["two", "three", "four"])

    def test_skip_while(self):
        test = Enumerable([1, 4, 6, 4, 1]).skip_while(lambda x: x < 5)
        self.assertListEqual(test.to_list(), [6, 4, 1])

        test = Enumerable([]).skip_while(lambda x: x < 5)
        self.assertListEqual(test.to_list(), [])

    def test_take_last(self):
        test = Enumerable([1, 2, 3, 4, 5]).take_last(2)
        self.assertListEqual(test.to_list(), [4, 5])

        test = Enumerable(["one", "two", "three", "four", "five"]).take(3).take_last(1)
        self.assertListEqual(test.to_list(), ["three"])

    def test_take_while(self):
        test = Enumerable([1, 4, 6, 4, 1]).take_while(lambda x: x < 5)
        self.assertListEqual(test.to_list(), [1, 4])

        test = Enumerable([]).skip_while(lambda x: x < 5)
        self.assertListEqual(test.to_list(), [])

    def test_zip(self):
        test = Enumerable(["A", "B", "C", "D"]).zip(Enumerable(["x", "y"]), lambda t: "{0}{1}".format(t[0], t[1]))
        self.assertListEqual(test.to_list(), ["Ax", "By"])
