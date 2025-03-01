from django.urls import path, re_path, register_converter

from catalog.converters import PositiveIntConverter
import catalog.views

register_converter(PositiveIntConverter, "posint")

urlpatterns = [
    path("", catalog.views.item_list, name="catalog"),
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
]
