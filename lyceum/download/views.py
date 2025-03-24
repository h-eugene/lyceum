from django.conf import settings
from django.http import FileResponse


def download_image(request, path):
    return FileResponse(
        open(settings.MEDIA_ROOT / path, "rb"),
        as_attachment=True,
    )


__all__ = []
