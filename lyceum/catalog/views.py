from itertools import groupby

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from operator import attrgetter

from catalog.models import Item


def item_list(request):
    template = "catalog/item_list.html"

    items = Item.objects.published().order_by("category__name")

    grouped_items = []
    for category_name, group in groupby(
        items,
        key=attrgetter("category.name"),
    ):
        group_list = list(group)
        if group_list:
            grouped_items.append((category_name, group_list))

    context = {
        "grouped_items": grouped_items,
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
    }
    return render(request, template, context)


def reg_expression(request, pk):
    return HttpResponse(pk)


__all__ = []
