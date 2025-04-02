from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.normalization import normalize_name
from core.validators import validate_slug


class BaseModel(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name=_("admin name"),
        unique=True,
        help_text="Название товара",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("admin is published"),
        help_text="Опубликован ли товар",
    )

    class Meta:
        abstract = True


class ItemAttribute(BaseModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name=_("slug"),
        help_text="Введите уникальный слаг. Допустимы латинские буквы, цифры, '-' и '_'.",
    )
    normalized_name = models.CharField(
        max_length=200,
        unique=False,
        editable=False,
        verbose_name="нормализованное имя",
        help_text="Автоматически нормализованное имя для уникальности.",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.normalized_name or self.name != self.normalized_name:
            self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk:
            normalized = normalize_name(self.name)
            if self.__class__.objects.filter(
                normalized_name=normalized
            ).exists():
                raise ValidationError(
                    {
                        "name": (
                            f"{self._meta.verbose_name.title()} с нормализованным именем '{normalized}' уже существует."
                        )
                    }
                )
        super().clean()

    def __str__(self):
        return self.name[:15]


__all__ = []
