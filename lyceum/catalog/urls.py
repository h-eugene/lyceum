import django.urls

import catalog.views
from catalog.converters import PositiveIntConverter

django.urls.register_converter(PositiveIntConverter, "posint")

urlpatterns = [
    django.urls.path("", catalog.views.item_list),
    django.urls.path("<int:pk>/", catalog.views.item_detail, name="Item"),
    django.urls.re_path(
        r"^re/(?P<pk>0*[1-9]\d*)/$", catalog.views.re_expression, name="Item"
    ),
    django.urls.path(
        "converter/<posint:pk>/", catalog.views.re_expression, name="Item"
    ),
]
