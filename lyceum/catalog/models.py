from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from tinymce.models import HTMLField

from catalog.normalization import normalize_name
from catalog.validators import (
    validate_slug,
    ValidateMustContain,
)
from core.models import BaseModel


class Tag(BaseModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="слаг",
        help_text=(
            "Введите уникальный слаг. Допустимы "
            "латинские буквы, цифры, '-' и '_'."
        ),
    )
    normalized_name = models.CharField(
        max_length=200,
        unique=False,
        editable=False,
        verbose_name="нормализованное имя",
        help_text="Автоматически нормализованное имя для уникальности.",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]

    def save(self, *args, **kwargs):
        if not self.normalized_name or self.name != self.normalized_name:
            self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk:
            normalized = normalize_name(self.name)
            if Tag.objects.filter(normalized_name=normalized).exists():
                raise ValidationError(
                    {
                        "name": (
                            f"Тег с нормализованным именем '{normalized}'"
                            " уже существует."
                        ),
                    },
                )
        super().clean()


class Category(BaseModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="слаг",
        help_text=(
            "Введите уникальный слаг. Допустимы "
            "латинские буквы, цифры, '-' и '_'."
        ),
    )
    weight = models.PositiveIntegerField(
        default=100,
        verbose_name="вес",
        validators=[
            MinValueValidator(1, message="Вес должен быть не менее 1."),
            MaxValueValidator(
                32767,
                message="Вес должен быть не более 32767.",
            ),
        ],
        help_text=("Вес категории от 1 до 32767 (по умолчанию 100)."),
    )
    normalized_name = models.CharField(
        max_length=150,
        unique=False,
        editable=False,
        verbose_name="нормализованное имя",
        help_text="Автоматически нормализованное имя для уникальности.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]

    def save(self, *args, **kwargs):
        if not self.normalized_name or self.name != self.normalized_name:
            self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk:
            normalized = normalize_name(self.name)
            if Category.objects.filter(normalized_name=normalized).exists():
                raise ValidationError(
                    {
                        "name": (
                            "Категория с нормализованным "
                            f"именем '{normalized}' уже существует."
                        ),
                    },
                )
        super().clean()


class ItemMainImage(models.Model):
    item = models.OneToOneField(
        "Item",
        on_delete=models.CASCADE,
        related_name="main_image",
        verbose_name="товар",
    )

    image = models.ImageField(
        upload_to="catalog/%Y/%m/%d/",
        verbose_name="главное изображение",
        help_text="Будет приведено к размерам 300x300",
    )

    def get_image_300x300(self):
        return get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=100,
        )

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.get_image_300x300().url}" width="50">',
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"

    def __str__(self):
        return f"Главное изображение для {self.item}"

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class ItemImages(models.Model):
    item = models.ForeignKey(
        "Item",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="товар",
    )
    image = models.ImageField(
        upload_to="catalog/%Y/%m/%d/",
        verbose_name="изображение",
        help_text="Будет приведено к размерам 300x300",
    )

    def get_image_300x300(self):
        return get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" width="50">',
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    def __str__(self):
        return f"Изображение для {self.item}"

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"


class ItemManager(models.Manager):
    def get_published_base(self, with_images=False):
        queryset = (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category", "main_image")
        )

        prefetch_list = [
            models.Prefetch(
                "tags",
                queryset=Tag.objects.filter(is_published=True).only("name"),
            ),
        ]

        if with_images:
            prefetch_list.append(
                models.Prefetch(
                    "images",
                    queryset=ItemImages.objects.only("image"),
                ),
            )

        return queryset.prefetch_related(*prefetch_list).only(
            "name",
            "text",
            "category__name",
            "main_image__image",
        )

    def published(self):
        return self.get_published_base()

    def on_main(self):
        return self.get_published_base().filter(is_on_main=True)


class Item(BaseModel):
    objects = ItemManager()

    text = HTMLField(
        validators=[
            ValidateMustContain("Превосходно", "Роскошно"),
        ],
        verbose_name="текст",
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
        verbose_name="категория",
        help_text="Выберите категорию для этого товара.",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="items",
        related_query_name="item",
        verbose_name="теги",
        help_text="Выберите один или несколько тегов для этого товара.",
    )

    is_on_main = models.BooleanField(
        default=False,
        verbose_name="на главной странице",
        help_text="Если True, то товар отображается на главной странице",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]


__all__ = []
