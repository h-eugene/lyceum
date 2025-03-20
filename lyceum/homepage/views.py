from http import HTTPStatus

import django.http
import django.shortcuts

from catalog.models import Item


def home(request):
    template = "homepage/main.html"
    items = Item.objects.all()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = []
