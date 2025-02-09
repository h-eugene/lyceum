import django
import django.urls
from django.contrib import admin

urlpatterns = [
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("about/", django.urls.include("about.urls")),
    django.urls.path("admin/", admin.site.urls),
    django.urls.path("catalog/", django.urls.include("catalog.urls")),
]

if django.conf.settings.DEBUG:
    import debug_toolbar as toolbar

    path = (django.urls.path("__debug__/", django.urls.include(toolbar.urls)),)
    urlpatterns += path
