import django.urls

import core.views

urlpatterns = [
    django.urls.re_path("", core.views.coffee),
]
