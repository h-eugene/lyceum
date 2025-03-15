from django.shortcuts import render
from django.http import (
    Http404,
    HttpResponse,
)
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


def get_item_data(pk):
    try:
        return ITEMS[int(pk)]
    except (KeyError, ValueError):
        raise Http404("Товар не найден")


def get_item_view(request, pk, template_name):
    try:
        item_data = get_item_data(pk)
        return render(request, template_name, item_data)
    except Http404:
        return render(
            request,
            "404.html",
            {"message": "Товар не найден"},
            status=HTTPStatus.NOT_FOUND,
        )


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
