from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from parameterized import parameterized

import catalog.models
from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def test_default_catalog_endpoint_status(self):
        client = Client()

        response = client.get("/catalog/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_default_catalog_endpoint_content(self):
        client = Client()

        response = client.get("/catalog/")
        text = "Список элементов"

        self.assertEqual(
            response.content.decode("utf-8"),
            "<body>" + text + "</body>",
        )


class TestDynamicURL(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.OK),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_with_index_endpoint_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()

        response = client.get(f"/catalog/{index}/")
        self.assertEqual(response.status_code, status)

    def test_catalog_with_index_endpoint_content(self):
        client = Client()

        response = client.get("/catalog/1/")
        text = "Подробно элемент"

        self.assertEqual(
            response.content.decode("utf-8"),
            "<body>" + text + "</body>",
        )

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.NOT_FOUND),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_with_positive_number_regex_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()

        response = client.get(f"/catalog/re/{index}/")
        self.assertEqual(response.status_code, status)

    def test_catalog_with_positive_number_regex_content(self):
        client = Client()

        response = client.get("/catalog/re/123/")
        self.assertEqual(response.content.decode("utf-8"), "123")

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.NOT_FOUND),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_with_converter_to_posint_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()

        response = client.get(f"/catalog/converter/{index}/")
        self.assertEqual(response.status_code, status)

    def test_catalog_with_converter_to_posint_content(self):
        client = Client()

        response = client.get("/catalog/converter/123/")
        self.assertEqual(response.content.decode("utf-8"), "123")


class CatalogModelTests(TestCase):
    def setUp(self):
        super().setUp()
        self.category = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            weight=200,
            is_published=True,
        )
        self.tag = catalog.models.Tag.objects.create(
            name="Тестовый тег",
            slug="test-tag",
            is_published=True,
        )

    def tearDown(self):
        self.category.delete()
        self.tag.delete()
        super().tearDown()

    def test_create_catalog_item_valid_text(self):
        item = catalog.models.Item(
            name="Тестовый товар",
            text="Этот товар превосходно работает!",
            is_published=True,
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(catalog.models.Item.objects.count(), 1)
        self.assertEqual(item.name, "Тестовый товар")
        self.assertTrue(item.is_published)
        self.assertEqual(item.category, self.category)
        self.assertIn(self.tag, item.tags.all())

    def test_create_catalog_item_invalid_text(self):
        item = catalog.models.Item(
            name="Тестовый товар",
            text="Этот товар просто хороший",
            is_published=True,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_catalog_item_text_with_luxury(self):
        item = catalog.models.Item(
            name="Роскошный товар",
            text="Этот товар выглядит роскошно!",
            is_published=True,
            category=self.category,
        )
        item.full_clean()
        item.save()
        self.assertEqual(catalog.models.Item.objects.count(), 1)

    def test_catalog_item_invalid_text_with_substring(self):
        item = catalog.models.Item(
            name="Недопустимый товар",
            text="Этот товар неПревосходно работает!",
            is_published=True,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_catalog_item_invalid_text_with_partial_word(self):
        item = catalog.models.Item(
            name="Недопустимый товар",
            text="Этот товар превосходный!",
            is_published=True,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_catalog_item_empty_text(self):
        item = catalog.models.Item(
            name="Пустой товар",
            text="",
            is_published=True,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_catalog_tag_creation(self):
        tag = catalog.models.Tag.objects.create(
            name="Новый тег",
            slug="new-tag",
            is_published=False,
        )
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            2,
        )
        self.assertEqual(tag.name, "Новый тег")
        self.assertFalse(tag.is_published)

    def test_catalog_tag_unique_slug(self):
        with self.assertRaises(ValidationError):
            tag = catalog.models.Tag(
                name="Дубликат тег",
                slug="test-tag",
                is_published=True,
            )
            tag.full_clean()

    def test_catalog_tag_invalid_slug(self):
        with self.assertRaises(ValidationError):
            tag = catalog.models.Tag(
                name="Недопустимый тег",
                slug="test@tag",
                is_published=True,
            )
            tag.full_clean()

    def test_catalog_category_weight_validation(self):
        with self.assertRaises(ValidationError):
            category = catalog.models.Category(
                name="Недопустимая категория",
                slug="invalid-category",
                weight=0,
            )
            category.full_clean()

    def test_catalog_category_weight_max(self):
        category = catalog.models.Category(
            name="Категория с максимальным весом",
            slug="max-weight",
            weight=32767,
        )
        category.full_clean()
        category.save()
        self.assertEqual(category.weight, 32767)

    def test_catalog_category_default_weight(self):
        category = catalog.models.Category(
            name="Категория по умолчанию",
            slug="default-category",
        )
        category.full_clean()
        category.save()
        self.assertEqual(category.weight, 100)

    def test_catalog_category_unique_slug(self):
        with self.assertRaises(ValidationError):
            category = catalog.models.Category(
                name="Дубликат категория",
                slug="test-category",
                weight=100,
                is_published=True,
            )
            category.full_clean()

    def test_item_category_relationship(self):
        item = catalog.models.Item(
            name="Товар с категорией",
            text="Этот товар превосходно работает!",
            is_published=True,
            category=self.category,
        )
        item.full_clean()
        item.save()
        self.assertEqual(item.category, self.category)

    def test_item_tags_relationship(self):
        item = catalog.models.Item(
            name="Товар с тегом",
            text="Этот товар роскошно работает!",
            is_published=True,
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)
        self.assertIn(self.tag, item.tags.all())
        self.assertEqual(item.tags.count(), 1)

    def test_item_name_max_length(self):
        long_name = "a" * 201
        with self.assertRaises(ValidationError):
            item = catalog.models.Item(
                name=long_name,
                text="Этот товар превосходно работает!",
                is_published=True,
                category=self.category,
            )
            item.full_clean()

    def test_tag_normalized_name_russian_english(self):
        tag1 = catalog.models.Tag.objects.create(
            name="Привет",
            slug="privet",
            is_published=True,
        )
        self.assertEqual(tag1.normalized_name, "privet")

        with self.assertRaises(ValidationError):
            tag2 = catalog.models.Tag(
                name="привет!",
                slug="privet2",
                is_published=True,
            )
            tag2.full_clean()
