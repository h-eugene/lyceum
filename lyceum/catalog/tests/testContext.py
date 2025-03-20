from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, Item, Tag


class TestContext(TestCase):
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

    def test_home_page_show_correct_context(self):
        response = Client().get(reverse("homepage:main"))
        self.assertIn("items", response.context)

    def test_home_count_item(self):
        response = Client().get(reverse("homepage:main"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)


__all__ = []
