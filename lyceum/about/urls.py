import about.views

import django.urls

urlpatterns = [
    django.urls.path("", about.views.description),
]
