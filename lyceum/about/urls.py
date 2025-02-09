import django.urls

import about.views


urlpatterns = [
    django.urls.path("", about.views.description),
]
