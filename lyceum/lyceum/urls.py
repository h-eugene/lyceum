from django.contrib import admin
from django.urls import re_path, path, include
from django.conf import settings

app_name = "lyceum"

urlpatterns = [
    re_path(r"^(?:.*/)?coffee/", include("core.urls")),
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("catalog/", include("catalog.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar as toolbar
    from django.conf.urls.static import static

    path = (path("__debug__/", include(toolbar.urls)),)
    urlpatterns += path

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
