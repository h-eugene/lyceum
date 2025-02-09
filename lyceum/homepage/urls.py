import django.urls

import homepage.views


urlpatterns = [
    django.urls.path("", homepage.views.home),
]
