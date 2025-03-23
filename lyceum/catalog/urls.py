from django.urls import path, re_path, register_converter

from catalog.converters import PositiveIntConverter
import catalog.views

register_converter(PositiveIntConverter, "posint")

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<int:pk>/", catalog.views.item_detail, name="item_detail"),
    re_path(
        r"^re/(?P<pk>0*[1-9]\d*)/$",
        catalog.views.reg_expression,
        name="item_detail_re",
    ),
    path(
        "converter/<posint:pk>/",
        catalog.views.reg_expression,
        name="item_detail_converter",
    ),
    path("new/", catalog.views.new_items, name="new_items"),
    path("friday/", catalog.views.friday_items, name="friday_items"),
    path(
        "unverified/",
        catalog.views.unverified_items,
        name="unverified_items",
    ),
]
