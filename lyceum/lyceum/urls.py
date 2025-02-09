from django.contrib import admin

import django.urls


urlpatterns = [
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("admin/", admin.site.urls),
    django.urls.path("catalog/", django.urls.include("catalog.urls")),
    django.urls.path("about/", django.urls.include("about.urls"))
]
