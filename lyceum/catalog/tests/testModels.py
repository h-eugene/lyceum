from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

import catalog.models


class TagTests(TestCase):
    def setUp(self):
        super().setUp()
        self.tag = catalog.models.Tag.objects.create(
            name="Тестовый тег",
            slug="test-tag",
            is_published=True,
        )

    def tearDown(self):
        if hasattr(self, "tag") and self.tag:
            self.tag.delete()
        super().tearDown()

    def _create_tag(self, name, slug, is_published=True):
        return catalog.models.Tag(
            name=name,
            slug=slug,
            is_published=is_published,
        )

    @parameterized.expand(
        [
            (
                "Дубликат тег",
                "test-tag",
                "Тест уникальности slug для существующего тега",
            ),
            (
                "Ещё один дубликат",
                "test-tag",
                "Повторная проверка уникальности slug",
            ),
        ],
    )
    def test_catalog_tag_unique_slug(self, name, slug, test_name):
        with self.subTest(msg=test_name):
            with self.assertRaises(ValidationError):
                tag = self._create_tag(name, slug, True)
                tag.full_clean()

    @parameterized.expand(
        [
            (
                "Недопустимый тег",
                "test@tag",
                "Тест недопустимых символов в slug (@)",
            ),
            (
                "Недопустимый тег с пробелом",
                "test tag",
                "Тест недопустимых пробелов в slug",
            ),
        ],
    )
    def test_catalog_tag_invalid_slug(self, name, slug, test_name):
        with self.subTest(msg=test_name):
            with self.assertRaises(ValidationError):
                tag = self._create_tag(name, slug, True)
                tag.full_clean()

    def test_tag_normalized_name_russian_english(self):
        tag1 = catalog.models.Tag.objects.create(
            name="Привет",
            slug="privet",
            is_published=True,
        )
        self.assertEqual(tag1.normalized_name, "privet")

        with self.assertRaises(ValidationError):
            tag2 = self._create_tag("привет!", "privet2", True)
            tag2.full_clean()
            tag2.save()


class CategoryTests(TestCase):
    def setUp(self):
        super().setUp()
        self.category = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            weight=200,
            is_published=True,
        )

    def tearDown(self):
        if hasattr(self, "category") and self.category:
            self.category.delete()
        super().tearDown()

    def _create_category(self, name, slug, weight=100, is_published=True):
        return catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
            is_published=is_published,
        )

    def test_catalog_category_weight_validation(self):
        with self.assertRaises(ValidationError):
            category = self._create_category(
                "Недопустимая категория",
                "invalid-category",
                0,
                True,
            )
            category.full_clean()

    def test_catalog_category_weight_max(self):
        category = self._create_category(
            "Категория с максимальным весом",
            "max-weight",
            32767,
            True,
        )
        category.full_clean()
        category.save()
        self.assertEqual(category.weight, 32767)

    def test_catalog_category_default_weight(self):
        category = self._create_category(
            "Категория по умолчанию",
            "default-category",
        )
        category.full_clean()
        category.save()
        self.assertEqual(category.weight, 100)

    @parameterized.expand(
        [
            (
                "Дубликат категория",
                "test-category",
                100,
                "Тест уникальности slug для существующей категории",
            ),
            (
                "Ещё один дубликат",
                "test-category",
                150,
                "Повторная проверка уникальности slug",
            ),
        ],
    )
    def test_catalog_category_unique_slug(self, name, slug, weight, test_name):
        with self.subTest(msg=test_name):
            with self.assertRaises(ValidationError):
                category = self._create_category(name, slug, weight, True)
                category.full_clean()


class ItemTests(TestCase):
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
        if hasattr(self, "category") and self.category:
            self.category.delete()
        if hasattr(self, "tag") and self.tag:
            self.tag.delete()
        catalog.models.Item.objects.all().delete()
        super().tearDown()

    def _create_item(self, name, text, category, is_published=True):
        return catalog.models.Item(
            name=name,
            text=text,
            category=category,
            is_published=is_published,
        )

    @parameterized.expand(
        [
            (
                "Тестовый товар",
                "Этот товар просто хороший",
                "Тест недопустимого текста без ключевых слов",
            ),
            (
                "Недопустимый товар",
                "Этот товар неПревосходно работает!",
                "Тест текста с подстрокой 'неПревосходно'",
            ),
            (
                "Недопустимый товар",
                "Этот товар превосходный!",
                "Тест текста с частичным словом 'превосходный'",
            ),
            ("Пустой товар", "", "Тест пустого текста"),
        ],
    )
    def test_create_catalog_item_invalid_text(self, name, text, test_name):
        with self.subTest(msg=test_name):
            item = self._create_item(name, text, self.category, True)
            with self.assertRaises(ValidationError):
                item.full_clean()

    def test_create_catalog_item_valid_text(self):
        item = self._create_item(
            "Тестовый товар",
            "Этот товар превосходно работает!",
            self.category,
            True,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(catalog.models.Item.objects.count(), 1)
        self.assertEqual(item.name, "Тестовый товар")
        self.assertTrue(item.is_published)
        self.assertEqual(item.category, self.category)
        self.assertIn(self.tag, item.tags.all())

    def test_catalog_item_text_with_luxury(self):
        item = self._create_item(
            "Роскошный товар",
            "Этот товар выглядит роскошно!",
            self.category,
            True,
        )
        item.full_clean()
        item.save()
        self.assertEqual(catalog.models.Item.objects.count(), 1)

    def test_item_name_max_length(self):
        long_name = "a" * 201
        with self.assertRaises(ValidationError):
            item = self._create_item(
                long_name,
                "Этот товар превосходно работает!",
                self.category,
                True,
            )
            item.full_clean()


class RelationshipTests(TestCase):
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
        if hasattr(self, "category") and self.category:
            self.category.delete()
        if hasattr(self, "tag") and self.tag:
            self.tag.delete()
        catalog.models.Item.objects.all().delete()
        super().tearDown()

    def _create_item(self, name, text, category, is_published=True):
        return catalog.models.Item(
            name=name,
            text=text,
            category=category,
            is_published=is_published,
        )

    def test_item_category_relationship(self):
        item = self._create_item(
            "Товар с категорией",
            "Этот товар превосходно работает!",
            self.category,
            True,
        )
        item.full_clean()
        item.save()
        self.assertEqual(item.category, self.category)

    def test_item_tags_relationship(self):
        item = self._create_item(
            "Товар с тегом",
            "Этот товар роскошно работает!",
            self.category,
            True,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)
        self.assertIn(self.tag, item.tags.all())
        self.assertEqual(item.tags.count(), 1)


__all__ = ["TagTests", "CategoryTests", "ItemTests", "RelationshipTests"]
