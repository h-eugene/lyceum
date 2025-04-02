from datetime import timedelta
import random

from django.db import models
from django.utils import timezone

ITEMS_PER_IMAGE = 5


class ItemManager(models.Manager):
    def get_published_base(self, with_images=False):
        from catalog.models import Category, Item, ItemImages, Tag

        queryset = (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
        )

        prefetch_list = [
            models.Prefetch(
                Item.tags.field.name,
                queryset=Tag.objects.filter(is_published=True).only(
                    Tag.name.field.name,
                ),
            ),
        ]

        if with_images:
            prefetch_list.append(
                models.Prefetch(
                    Item.images.field.related_query_name(),
                    queryset=ItemImages.objects.only(
                        ItemImages.image.field.name,
                        ItemImages.item.field.name,
                    ),
                ),
            )

        return queryset.prefetch_related(*prefetch_list).only(
            Item.name.field.name,
            Item.text.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            Item.main_image.related.name,
        )

    def published(self):
        from catalog.models import Category, Item

        return self.get_published_base().order_by(
            f"{Item.category.field.name}__{Category.name.field.name}",
            f"{Item.name.field.name}",
        )

    def on_main(self):
        from catalog.models import Item

        return (
            self.get_published_base()
            .filter(is_on_main=True)
            .order_by(f"{Item.name.field.name}")
        )

    def new_items(self):
        from catalog.models import Item

        one_week_ago = timezone.now() - timedelta(days=7)
        items_ids = list(
            self.published()
            .filter(created_at__gte=one_week_ago)
            .values_list(Item.id.field.name, flat=True),
        )

        if len(items_ids) > ITEMS_PER_IMAGE:
            items_ids = random.sample(items_ids, ITEMS_PER_IMAGE)
        return self.published().filter(id__in=items_ids)

    def friday_items(self):
        from catalog.models import Item

        return (
            self.published()
            .filter(updated_at__week_day=6)
            .order_by(f"-{Item.updated_at.field.name}")
        )[:ITEMS_PER_IMAGE]

    def unverified_items(self):
        from catalog.models import Item

        lower = models.F(Item.updated_at.field.name) - timedelta(seconds=1)
        upper = models.F(Item.updated_at.field.name) + timedelta(seconds=1)
        return (
            self.on_main()
            .filter(
                created_at__gte=lower,
                created_at__lte=upper,
            )
            .order_by("?")
        )[:ITEMS_PER_IMAGE]
