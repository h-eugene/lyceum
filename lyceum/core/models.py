from django.db import models
from django.utils.translation import gettext_lazy as _


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


__all__ = []
