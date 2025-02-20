import django.contrib.admin

import catalog.models

django.contrib.admin.site.register(catalog.models.Category)
django.contrib.admin.site.register(catalog.models.Tag)


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)
