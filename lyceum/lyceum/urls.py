from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.i18n import set_language

app_name = "lyceum"

urlpatterns = [
    re_path(r"^(?:.*/)?coffee/", include("core.urls")),
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("catalog/", include("catalog.urls")),
    path("download/", include("download.urls")),
    path('i18n/', set_language, name='set_language'),
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
