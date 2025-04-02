from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from catalog.managers import ItemManager
from catalog.validators import ValidateMustContain
from core.models import BaseImage, BaseItemAttribute, BaseModel


class Tag(BaseItemAttribute):
    class Meta:
        ordering = ("slug",)
        verbose_name = _("admin tag")
        verbose_name_plural = _("admin tags")
        default_related_name = "tags"


class Category(BaseItemAttribute):
    weight = models.PositiveIntegerField(
        default=100,
        verbose_name=_("weight"),
        validators=[
            MinValueValidator(1, message="Вес должен быть не менее 1."),
            MaxValueValidator(
                32767, message="Вес должен быть не более 32767."
            ),
        ],
        help_text="Вес категории от 1 до 32767 (по умолчанию 100).",
    )

    class Meta:
        ordering = ("weight",)
        verbose_name = _("admin category")
        verbose_name_plural = _("admin categories")


class ItemMainImage(BaseImage):
    item = models.OneToOneField(
        "Item",
        on_delete=models.CASCADE,
        related_name="main_image",
        verbose_name=_("admin item"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("image").verbose_name = _("admin main image")

    def __str__(self):
        return f"Главное изображение для {self.item}"

    class Meta:
        verbose_name = _("admin main image")
        verbose_name_plural = _("admin main images")


class ItemImages(BaseImage):
    item = models.ForeignKey(
        "Item",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("admin item"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("image").verbose_name = _("admin image")

    def __str__(self):
        return f"Изображение для {self.item}"

    class Meta:
        verbose_name = _("admin image")
        verbose_name_plural = _("admin images")


class Item(BaseModel):
    objects = ItemManager()

    text = HTMLField(
        validators=[
            ValidateMustContain("Превосходно", "Роскошно"),
        ],
        verbose_name=_("admin text"),
        help_text=(
            "Введите текст товара, "
            "который обязательно должен содержать "
            "слово 'превосходно' или 'роскошно'."
        ),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
        verbose_name=_("admin category"),
        help_text="Выберите категорию для этого товара.",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="items",
        related_query_name="item",
        verbose_name=_("admin tags"),
        help_text="Выберите один или несколько тегов для этого товара.",
    )

    is_on_main = models.BooleanField(
        default=False,
        verbose_name=_("is_on_main"),
        help_text="Если True, то товар отображается на главной странице",
    )

    created_at = models.DateTimeField(
        verbose_name=_("admin created at"),
        auto_now_add=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("admin updated at"),
        auto_now=True,
        null=True,
    )

    class Meta:
        ordering = ("category__name",)
        verbose_name = _("admin item")
        verbose_name_plural = _("admin items")

    def __str__(self):
        return self.name[:15]


__all__ = []
