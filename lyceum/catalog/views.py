from django.shortcuts import render
from django.http import (
    Http404,
    HttpResponse,
)
from django.template.loader import render_to_string
from http import HTTPStatus

ITEMS = {
    1: {
        "name": "Котик",
        "description": "Милый котик для вашего дома. Идеальный компаньон для любого любителя животных!",
        "image": "images/cat.jpg",
    },
    2: {
        "name": "Енотик",
        "description": "Игривый енот для радости. Отличный друг для весёлых моментов!",
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
        return render(
            request,
            template_name,
            {
                "pk": pk,
                "name": item_data["name"],
                "description": item_data["description"],
                "image": item_data["image"],
            },
        )
    except Http404:
        return render(
            request,
            "404.html",
            {"message": "Товар не найден"},
            status=HTTPStatus.NOT_FOUND,
        )


def item_list(request):
    template = "catalog/item_list.html"
    pks = list(ITEMS.keys())  
    
    cards = []
    for pk in pks:
        card_html = render_to_string("catalog/item_card.html", {
            "pk": pk,
            "name": ITEMS[pk]["name"],
            "description": ITEMS[pk]["description"],
            "image": ITEMS[pk]["image"],
        })
        cards.append(card_html)
    
    return render(request, template, {"cards": cards})




def item_detail(request, pk):
    return get_item_view(request, pk, "catalog/item_detail.html")


def reg_expression(request, pk):
    return HttpResponse(pk)
