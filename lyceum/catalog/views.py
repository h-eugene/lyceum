from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Item


def item_list(request):
    template = "catalog/item_list.html"

    items = Item.objects.published().order_by(Item.category.field.name)

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
    }
    return render(request, template, context)


def reg_expression(request, pk):
    return HttpResponse(pk)


__all__ = []
