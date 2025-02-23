from django.core.exceptions import ValidationError
from django.db import models

from catalog.normalization import normalize_name
from catalog.validators import (
    validate_slug,
    validate_weight,
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
        unique=True,
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
        validators=[validate_weight],
        help_text=("Вес категории от 1 до 32767 (по умолчанию 100)."),
    )
    normalized_name = models.CharField(
        max_length=150,
        unique=True,
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


class Item(BaseModel):
    text = models.TextField(
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
        verbose_name="категория",
        help_text="Выберите категорию для этого товара.",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="items",
        verbose_name="теги",
        help_text="Выберите один или несколько тегов для этого товара.",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]
