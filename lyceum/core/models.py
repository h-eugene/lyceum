from django.db import models


class BaseModel(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название",
        unique=True,
        help_text="Название товара",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Опубликован ли товар",
    )

    class Meta:
        abstract = True
