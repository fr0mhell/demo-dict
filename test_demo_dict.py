from unittest import TestCase
from demo_dict import DemoDict


class MyHashable:
    """Allows testing hash collisions by easy creation of values with same hash."""
    def __init__(self, hash_value):
        self.hash = hash_value

    def __hash__(self):
        return self.hash


class DemoDictTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.a_value = 1
        cls.b_value = 2
        cls.c_value = 3

    def setUp(self) -> None:
        self.empty = DemoDict()
        self.with_values = DemoDict(a=self.a_value, b=self.b_value)

    def test_create_with_values(self):
        self.assertEqual(len(self.with_values), 2)
        self.assertEqual(self.with_values['a'], self.a_value)
        self.assertEqual(self.with_values['b'], self.b_value)

    def test_create_empty(self):
        self.assertEqual(len(self.empty), 0)

    def test_set_item_empty_dict(self):
        self.empty['a'] = self.a_value
        self.empty['b'] = self.b_value

        self.assertEqual(len(self.empty), 2)
        self.assertEqual(self.empty['a'], self.a_value)
        self.assertEqual(self.empty['b'], self.b_value)

    def test_set_item_overwrites_value(self):
        self.with_values['a'] = self.c_value
        self.with_values['b'] = self.a_value

        self.assertEqual(len(self.with_values), 2)
        self.assertEqual(self.with_values['a'], self.c_value)
        self.assertEqual(self.with_values['b'], self.a_value)

    def test_get_item_raises_error_when_no_key(self):
        with self.assertRaises(KeyError):
            self.with_values['c']

    def test_hash_collision(self):
        # create two future keys with same hash
        # locator of a will be in _locators_list[-1]
        a = MyHashable(hash_value=DemoDict._initial_size-1)
        # locator of b will be in _locators_list[0] because _locators_list[-1] already points to a
        b = MyHashable(hash_value=DemoDict._initial_size-1)

        self.empty[a] = self.a_value
        self.empty[b] = self.b_value

        a_locator = self.empty._locators_list[-1]
        a_hash, a_key, a_value = self.empty._table[a_locator]
        self.assertEqual(a_key, a)
        self.assertEqual(a_value, self.a_value)

        b_locator = self.empty._locators_list[0]
        b_hash, b_key, b_value = self.empty._table[b_locator]
        self.assertEqual(b_key, b)
        self.assertEqual(b_value, self.b_value)

    def test_iter(self):
        expected_keys = ['a', 'b']
        result_keys = [key for key in self.with_values]

        self.assertListEqual(result_keys, expected_keys)

    def test_keys_method(self):
        expected_keys = ['a', 'b']
        self.assertListEqual(self.with_values.keys(), expected_keys)

    def test_values_method(self):
        expected_values = [self.a_value, self.b_value]
        self.assertListEqual(self.with_values.values(), expected_values)

    def test_items_method(self):
        expected_pairs = [('a', self.a_value), ('b', self.b_value)]
        self.assertListEqual(self.with_values.items(), expected_pairs)

    # TODO: add tests for update

    def test_deletion(self):
        a = MyHashable(hash_value=0)
        b = MyHashable(hash_value=1)

        self.empty[a] = self.a_value
        self.empty[b] = self.b_value

        # Check b deleted from all internals
        b_locator = self.empty._locators_list[1]
        del self.empty[b]
        self.assertEqual(len(self.empty), 1)
        self.assertIsNone(self.empty._locators_list[1])
        self.assertListEqual(self.empty._table[b_locator], [None, None, None])

        # Check c correctly added
        c = MyHashable(hash_value=2)
        self.empty[c] = self.c_value
        self.assertEqual(len(self.empty), 2)

    def test_deletion_raises_error(self):
        with self.assertRaises(KeyError):
            del self.with_values['c']
