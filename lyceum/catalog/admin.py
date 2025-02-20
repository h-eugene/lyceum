import django.contrib.admin

import catalog.models

django.contrib.admin.site.register(catalog.models.category)
django.contrib.admin.site.register(catalog.models.tag)


@django.contrib.admin.register(catalog.models.item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)
