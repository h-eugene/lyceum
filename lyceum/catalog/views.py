from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Item, ItemImages, Tag


def item_list(request):
    template = "catalog/catalog.html"
    items = (
        Item.objects.filter(is_published=True)
        .select_related("category", "main_image")
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.filter(is_published=True).only("name"),
            )
        )
        .only("name", "text", "category", "main_image")
        .order_by("category__name")
    )

    context = {
        "items": items,
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
    )
    context = {
        "item": item,
    }
    return render(request, template, context)


def reg_expression(request, pk):
    return HttpResponse(pk)


__all__ = []
