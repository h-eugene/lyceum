import django.urls

import core.views

app_name = "core"

urlpatterns = [
    django.urls.re_path("", core.views.coffee),
]
