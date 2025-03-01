import django.http
import django.shortcuts

from catalog.views import ITEMS


def home(request):
    template = "homepage/main.html"
    items = list(ITEMS.values())
    return django.shortcuts.render(request, template, {"items": items})
