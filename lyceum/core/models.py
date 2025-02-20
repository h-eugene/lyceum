from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    is_published = models.BooleanField(
        default=True, verbose_name="Опубликовано"
    )

    class Meta:
        abstract = True
