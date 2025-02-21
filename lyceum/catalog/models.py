from django.db import models

from catalog.validators import (
    validate_slug,
    validate_weight,
    ValidateMustContain,
)
from core.models import BaseModel


class Tag(BaseModel):
    slug = models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="Слаг",
        help_text=(
            "Введите уникальный слаг. Допустимы "
            "латинские буквы, цифры, '-' и '_'."
        ),
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class Category(BaseModel):
    slug = models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="Слаг",
        help_text=(
            "Введите уникальный слаг. Допустимы "
            "латинские буквы, цифры, '-' и '_'."
        ),
    )
    weight = models.PositiveIntegerField(
        default=100,
        verbose_name="Вес",
        validators=[validate_weight],
        help_text=(
            "Вес категории от 1 до 32767 (по умолчанию 100)."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]


class Item(BaseModel):
    text = models.TextField(
        validators=[
            ValidateMustContain("Превосходно", "Роскошно"),
        ],
        verbose_name="Текст",
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
        verbose_name="Категория",
        help_text="Выберите категорию для этого товара.",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="items",
        verbose_name="Теги",
        help_text="Выберите один или несколько тегов для этого товара.",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]
