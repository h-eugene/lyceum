from http import HTTPStatus

import django.http
import django.shortcuts
from django.db.models import Prefetch

from catalog.models import Item, Tag


def home(request):
    template = "homepage/main.html"
    items = (
        Item.objects.filter(
            is_published=True,
            is_on_main=True,
        )
        .select_related("category", "main_image")
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.filter(is_published=True).only("name"),
            )
        )
        .only("name", "text", "category", "main_image")
    )

    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = []
