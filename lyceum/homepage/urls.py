import django.urls

import homepage.views

urlpatterns = [
    django.urls.path("", homepage.views.home),
    django.urls.path("coffee/", homepage.views.coffee, name="Coffee"),
]
