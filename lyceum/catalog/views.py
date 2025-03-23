import mimetypes
import os

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Item


def download_image(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.exists(file_path):
        raise Http404("Файл не найден")

    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = "application/octet-stream"

    file = open(file_path, "rb")

    file_name = os.path.basename(file_path)

    response = FileResponse(
        file,
        content_type=content_type,
        as_attachment=True,
        filename=file_name,
    )

    response["Content-Length"] = os.path.getsize(file_path)

    return response


def item_list(request):
    template = "catalog/item_list.html"

    items = Item.objects.published()

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
