from django.db.models import QuerySet
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Item


class TestNewCatalog(TestCase):
    # fixtures = ["fixtures/data.json"]

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
        published_items = Item.objects.new_items()
        self.assertEqual(len(self.items), len(published_items))


class TestFridayCatalog(TestCase):
    # fixtures = ["fixtures/data.json"]

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
        published_items = Item.objects.friday_items()
        self.assertEqual(len(self.items), len(published_items))


class TestUnverifiedCatalog(TestCase):
    # fixtures = ["fixtures/data.json"]

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
        published_items = Item.objects.unverified_items()
        self.assertEqual(len(self.items), len(published_items))


__all__ = []
