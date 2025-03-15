from django.shortcuts import render
from django.http import HttpResponse
from http import HTTPStatus

ITEMS = {
    1: {
        "pk": 1,
        "name": "Котик",
        "description": (
            "Милый котик для вашего дома. Идеальный компаньон для любого любителя животных!"
        ),
        "image": "images/cat.jpg",
    },
    2: {
        "pk": 2,
        "name": "Енотик",
        "description": (
            "Игривый енот для радости. Отличный друг для весёлых моментов!"
        ),
        "image": "images/raccoon.jpg",
    },
}


def get_item_view(request, pk, template_name):
    if int(pk) in ITEMS:
        item_data = ITEMS[pk]
        return render(request, template_name, item_data)
    return HttpResponse("Товар не найден", status=HTTPStatus.NOT_FOUND)


def item_list(request):
    template = "catalog/catalog.html"
    items = list(ITEMS.values())
    return render(request, template, {"items": items})


def item_card(request, pk):
    return get_item_view(request, pk, "catalog/item_card.html")


def item_detail(request, pk):
    return get_item_view(request, pk, "catalog/item.html")


def reg_expression(request, pk):
    return HttpResponse(pk)
