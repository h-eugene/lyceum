from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from itertools import groupby
from operator import attrgetter

from catalog.models import Item, ItemImages, Tag


def item_list(request):
    template = "catalog/catalog.html"

    items = (
        Item.objects.filter(is_published=True, category__is_published=True)
        .select_related("category", "main_image")
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.filter(is_published=True).only("name"),
            ),
        )
        .only(
            "name",
            "text",
            "category__name",
            "main_image__image",
        )
        .order_by("category__name")
    )

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
        Item.objects.select_related(
            "category",
            "main_image",
        )
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.filter(is_published=True).only("name"),
            ),
            Prefetch(
                "images",
                queryset=ItemImages.objects.only("image"),
            ),
        )
        .only("name", "text", "main_image", "category"),
        pk=pk,
        is_published=True,
        category__is_published=True,
    )
    context = {
        "item": item,
    }
    return render(request, template, context)


def reg_expression(request, pk):
    return HttpResponse(pk)


__all__ = []
