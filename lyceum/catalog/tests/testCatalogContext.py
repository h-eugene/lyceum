from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog.models import Category, Item, Tag


class TestCatalogContext(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published_category",
            weight=100,
        )
        cls.unpublished_category = Category.objects.create(
            is_published=False,
            name="Тестовая неопубликованная категория",
            slug="unpublished_category",
            weight=100,
        )
        cls.published_tag = Tag.objects.create(
            is_published=True,
            name="Опубликованный тэг",
            slug="published_tag",
        )
        cls.unpublished_tag = Tag.objects.create(
            is_published=False,
            name="Непубликованный тэг",
            slug="unpublished_tag",
        )
        cls.published_item = Item(
            is_on_main=True,
            is_published=True,
            name="Опубликованный товар",
            category=cls.published_category,
            text="превосходно",
        )
        cls.unpublished_item = Item(
            is_on_main=True,
            is_published=False,
            name="Непубликованный товар",
            category=cls.unpublished_category,
            text="превосходно",
        )
        cls.published_item.save()
        cls.unpublished_item.save()
        cls.published_item.tags.add(cls.published_tag.pk)
        cls.published_item.tags.add(cls.unpublished_tag.pk)

    def setUp(self):
        super().setUp()

        self.response = Client().get(reverse("catalog:item_list"))
        self.grouped_items = self.response.context["grouped_items"]

    def test_catalog_page_show_correct_context(self):
        self.assertIn("grouped_items", self.response.context)
        for _, items in self.grouped_items:
            for item in items:
                self.assertIsInstance(item, Item)

    def test_catalog_page_items_count_and_content(self):
        _, items = self.grouped_items[0]
        self.assertEqual(len(items), 1)
        self.assertQuerysetEqual(
            items,
            [self.published_item],
            ordered=False,
        )

    @parameterized.expand(
        [
            ("Опубликованный товар", True),
            ("Тестовая опубликованная категория", True),
            ("Опубликованный тэг", True),
            ("Непубликованный товар", False),
            ("Тестовая неопубликованная категория", False),
            ("Непубликованный тэг", False),
        ],
    )
    def test_catalog_page_content(self, text, should_contain):
        if should_contain:
            self.assertContains(self.response, text)
        else:
            self.assertNotContains(self.response, text)


__all__ = []
