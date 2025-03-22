from django.test import TestCase

from catalog.models import Category, Item, ItemImages, ItemMainImage, Tag


class ItemManagerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Test Category",
            slug="test",
        )
        cls.tag = Tag.objects.create(name="Тестовый тег", slug="test")

        cls.item1 = Item.objects.create(
            name="Item 1",
            category=cls.category,
            is_on_main=True,
            text="Описание товара превосходно",
        )
        cls.item2 = Item.objects.create(
            name="Item 2",
            category=cls.category,
            is_on_main=False,
            text="Описание товара превосходно",
        )
        cls.item1.tags.add(cls.tag)
        cls.item2.tags.add(cls.tag)

        cls.main_image = ItemMainImage.objects.create(
            item=cls.item1,
            image="test.jpg",
        )

        cls.itemimage = ItemImages.objects.create(
            item=cls.item1,
            image="test.jpg",
        )

        cls.item1.main_image = cls.main_image
        cls.item1.save()
        cls.item1.images.add(cls.itemimage)

        cls.item2.main_image = cls.main_image
        cls.item2.save()
        cls.item1.images.add(cls.itemimage)

    def test_on_main_filter(self):
        items = Item.objects.on_main()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first().name, "Item 1")

    def test_published_filter(self):
        items = Item.objects.published()
        self.assertEqual(items.count(), 2)
        self.assertEqual(items.first().name, "Item 1")

    def test_on_main_fields_not_loaded(self):
        item = Item.objects.on_main().first()
        self.assertEqual(item.name, "Item 1")
        self.assertEqual(item.main_image.image, "test.jpg")
        self.assertNotIn("text", item._state.fields_cache)
        self.assertNotIn("images", item._state.fields_cache)

    def test_published_fields_not_loaded(self):
        item = Item.objects.published().first()
        self.assertEqual(item.name, "Item 1")
        self.assertEqual(item.text, "Описание товара превосходно")
        self.assertEqual(item.main_image.image, "test.jpg")
        self.assertNotIn("images", item._state.fields_cache)

    def test_on_main_prefetched_objects(self):
        item = Item.objects.on_main().first()
        self.assertEqual(item.category.name, "Test Category")
        self.assertEqual(item.tags.first().name, "Тестовый тег")
        self.assertIn("tags", item._prefetched_objects_cache)

    def test_published_prefetched_objects(self):
        item = Item.objects.published().first()
        self.assertEqual(item.category.name, "Test Category")
        self.assertEqual(item.tags.first().name, "Тестовый тег")
        self.assertIn("tags", item._prefetched_objects_cache)


__all__ = []
