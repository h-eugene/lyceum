import django.urls

import homepage.views

app_name = "homepage"

urlpatterns = [
    django.urls.path("", homepage.views.home, name="main"),
    django.urls.path("coffee/", homepage.views.coffee, name="coffee"),
]
