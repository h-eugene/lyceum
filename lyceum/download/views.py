import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


def download_image(request, path):
    file_path = Path(settings.MEDIA_ROOT) / path

    if not file_path.exists():
        raise Http404("Файл не найден")

    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = "application/octet-stream"

    file = file_path.open("rb")
    file_name = file_path.name

    response = FileResponse(
        file,
        content_type=content_type,
        as_attachment=True,
        filename=file_name,
    )
    response["Content-Length"] = file_path.stat().st_size
    return response
