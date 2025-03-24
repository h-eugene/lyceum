from django.db.models import QuerySet
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import ITEMS_PER_IMAGE, Item


class TestNewCatalog(TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        super().setUp()

        self.response = Client().get(reverse("catalog:new_items"))
        self.items = self.response.context["items"]

    def test_catalog_page_show_correct_context(self):
        self.assertIn("items", self.response.context)
        self.assertIsInstance(self.items, QuerySet)
        for item in self.items:
            self.assertIsInstance(item, Item)

    def test_catalog_page_items_count(self):
        self.assertEqual(len(self.items), ITEMS_PER_IMAGE)


class TestFridayCatalog(TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        super().setUp()

        self.response = Client().get(reverse("catalog:friday_items"))
        self.items = self.response.context["items"]

    def test_catalog_page_show_correct_context(self):
        self.assertIn("items", self.response.context)
        self.assertIsInstance(self.items, QuerySet)
        for item in self.items:
            self.assertIsInstance(item, Item)

    def test_catalog_page_items_count(self):
        self.assertEqual(len(self.items), ITEMS_PER_IMAGE)


class TestUnverifiedCatalog(TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        super().setUp()

        self.response = Client().get(reverse("catalog:unverified_items"))
        self.items = self.response.context["items"]

    def test_catalog_page_show_correct_context(self):
        self.assertIn("items", self.response.context)
        self.assertIsInstance(self.items, QuerySet)
        for item in self.items:
            self.assertIsInstance(item, Item)

    def test_catalog_page_items_count(self):
        self.assertEqual(len(self.items), ITEMS_PER_IMAGE)
