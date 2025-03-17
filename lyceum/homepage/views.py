from http import HTTPStatus

import django.http
import django.shortcuts

from catalog.views import ITEMS


def home(request):
    template = "homepage/main.html"
    items = list(ITEMS.values())
    return django.shortcuts.render(request, template, {"items": items})


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = ["home", "coffee"]
