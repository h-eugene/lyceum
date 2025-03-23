from django.urls import re_path, register_converter

from catalog.converters import PositiveIntConverter
import download.views

register_converter(PositiveIntConverter, "posint")

app_name = "download"

urlpatterns = [
    re_path(
        r"^(?P<path>.*)$",
        download.views.download_image,
        name="download_image",
    ),
]
