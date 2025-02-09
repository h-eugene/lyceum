import catalog.views

import django.urls

urlpatterns = [
    django.urls.path("", catalog.views.item_list),
    django.urls.path("<int:pk>/", catalog.views.item_detail),
]
