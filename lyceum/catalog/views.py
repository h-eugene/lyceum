from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from catalog.models import Item


def item_list(request):
    template = "catalog/item_list.html"

    items = Item.objects.published()

    context = {
        "items": items,
    }
    return render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = get_object_or_404(
        Item.objects.get_published_base(with_images=True),
        pk=pk,
    )
    context = {
        "item": item,
        "page_title": _("Item List"),
    }
    return render(request, template, context)


def reg_expression(request, pk):
    return HttpResponse(pk)


def new_items(request):
    items = Item.objects.new_items()
    template = "catalog/special.html"
    context = {
        "items": items,
        "page_title": _("New Items"),
    }
    return render(request, template, context)


def friday_items(request):
    items = Item.objects.friday_items()
    template = "catalog/special.html"
    context = {
        "items": items,
        "page_title": _("Friday Items"),
    }
    return render(request, template, context)


def unverified_items(request):
    items = Item.objects.unverified_items()
    template = "catalog/special.html"
    context = {
        "items": items,
        "page_title": _("Unverified Items"),
    }
    return render(request, template, context)


__all__ = []
