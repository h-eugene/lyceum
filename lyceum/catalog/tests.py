from http import HTTPStatus

from django.test import Client, TestCase

import catalog.models

from django.core.exceptions import ValidationError

from parameterized import parameterized

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
        ]
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
        ]
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
        ]
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
        self.category = catalog.models.category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            weight=200,
            is_published=True,
        )
        self.tag = catalog.models.tag.objects.create(
            name="Тестовый тег",
            slug="test-tag",
            is_published=True,
        )

    def test_create_catalog_item_valid_text(self):
        item = catalog.models.item(
            name="Тестовый товар",
            text="Этот товар превосходно работает!",
            is_published=True,
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(catalog.models.item.objects.count(), 1)
        self.assertEqual(item.name, "Тестовый товар")
        self.assertTrue(item.is_published)
        self.assertEqual(item.category, self.category)
        self.assertIn(self.tag, item.tags.all())

    def test_create_catalog_item_invalid_text(self):
        # Негативный тест: текст без слов "превосходно" или "роскошно"
        item = catalog.models.item(
            name="Тестовый товар",
            text="Этот товар просто хороший",
            is_published=True,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()  # Должен выбросить исключение из-за валидатора
            item.save()

    def test_catalog_item_text_with_luxury(self):
        # Позитивный тест: текст с "роскошно"
        item = catalog.models.item(
            name="Роскошный товар",
            text="Этот товар выглядит роскошно!",
            is_published=True,
            category=self.category,
        )
        item.full_clean()
        item.save()
        self.assertEqual(catalog.models.item.objects.count(), 1)

    def test_catalog_tag_creation(self):
        # Тест создания тега
        tag = catalog.models.tag.objects.create(
            name="Новый тег",
            slug="new-tag",
            is_published=False,
        )
        self.assertEqual(
            catalog.models.tag.objects.count(), 2
        )  # 1 из setUp + новый
        self.assertEqual(tag.name, "Новый тег")
        self.assertFalse(tag.is_published)

    def test_catalog_category_weight_validation(self):
        # Тест ограничения веса (0 не входит, минимум 1)
        with self.assertRaises(ValidationError):
            category = catalog.models.category(
                name="Недопустимая категория",
                slug="invalid-category",
                weight=0,
            )
            category.full_clean()
            category.save()

    def test_catalog_category_default_weight(self):
        # Тест значения веса по умолчанию
        category = catalog.models.category(
            name="Категория по умолчанию",
            slug="default-category",
        )
        category.full_clean()
        category.save()
        self.assertEqual(category.weight, 100)
