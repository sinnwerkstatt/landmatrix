import collections

from django.test import TestCase

from apps.api.utils import PropertyCounter


class PropertyCounterTestCase(TestCase):
    def setUp(self):
        self.counter = PropertyCounter()

    def test_init(self):
        for prop in self.counter.properties.keys():
            self.assertEqual(collections.defaultdict(int), getattr(self.counter, prop))
        self.assertEqual(set(), self.counter.activity_identifiers)

    def test_increment(self):
        self.counter.increment(
            activity_identifier=1,
            intention="test",
            implementation_status=["test1", "test2"],
            level_of_accuracy="test",
            test="test",
        )
        self.assertEqual({1}, self.counter.activity_identifiers)
        self.assertIsInstance(self.counter.intention, dict)
        self.assertEqual(1, self.counter.intention.get("test"))
        self.assertIsInstance(self.counter.implementation, dict)
        self.assertEqual(1, self.counter.implementation.get("test1"))
        self.assertEqual(1, self.counter.implementation.get("test2"))

    def test_get_properties(self):
        props = self.counter.get_properties()
        self.assertEqual({}, props.get("intention"))
        self.assertEqual({}, props.get("implementation"))
        self.assertEqual({}, props.get("level_of_accuracy"))
