from http import HTTPStatus

from django.db.models import QuerySet
from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog.models import Category, Item, Tag



class TestStaticURL(TestCase):


    def test_homepage_endpoint_status(self):
        client = Client()

        response = client.get("/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_coffee_endpoint_status(self):
        client = Client()
        url = reverse("homepage:coffee")
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)



class TestHomepageContext(TestCase):
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

        self.response = Client().get(reverse("homepage:main"))
        self.items = self.response.context["items"]

    def test_home_page_show_correct_context(self):
        self.assertIn("items", self.response.context)
        self.assertIsInstance(self.response.context["items"], QuerySet)
        for item in self.response.context["items"]:
            self.assertIsInstance(item, Item)

    def test_home_page_items_count_and_content(self):
        self.assertEqual(len(self.items), 1)
        self.assertQuerysetEqual(
            self.items,
            [self.published_item],
            ordered=False,
        )

    @parameterized.expand(
        [
            ("Опубликованный товар", True),
            ("Тестовая опубликованная категория", True),
            ("Опубликованный тэг", True),
            ("Непубликованный тэг", False),
        ],
    )
    def test_home_page_content(self, text, should_contain):
        if should_contain:
            self.assertContains(self.response, text)
        else:
            self.assertNotContains(self.response, text)


__all__ = []
