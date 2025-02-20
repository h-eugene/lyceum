import django.urls

from catalog.converters import PositiveIntConverter
import catalog.views

django.urls.register_converter(PositiveIntConverter, "posint")

urlpatterns = [
    django.urls.path("", catalog.views.item_list),
    django.urls.path(
        "<int:pk>/",
        catalog.views.item_detail,
        name="item",
    ),
    django.urls.re_path(
        r"^re/(?P<pk>0*[1-9]\d*)/$",
        catalog.views.reg_expression,
        name="item",
    ),
    django.urls.path(
        "converter/<posint:pk>/",
        catalog.views.reg_expression,
        name="item",
    ),
]
