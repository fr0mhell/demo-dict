from unittest import TestCase
from demo_dict import DemoDict


class DemoDictTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.a = 1
        cls.b = 2

    def test_create_with_values(self):
        to_test = DemoDict(a=self.a, b=self.b)

        self.assertEqual(len(to_test), 2)
        self.assertEqual(to_test['a'], self.a)
        self.assertEqual(to_test['b'], self.b)

    def test_create_empty(self):
        to_test = DemoDict()
        self.assertEqual(len(to_test), 0)

    def test_set_item(self):
        to_test = DemoDict()
        to_test['a'] = self.a
        to_test['b'] = self.b

        self.assertEqual(len(to_test), 2)
        self.assertEqual(to_test['a'], self.a)
        self.assertEqual(to_test['b'], self.b)

