import django.contrib.admin

import catalog.models

django.contrib.admin.site.register(catalog.models.Category)
django.contrib.admin.site.register(catalog.models.Tag)


NAME_FIELD = "name"
IS_PUBLISHED_FIELD = "is_published"
TAGS_FIELD = "tags"


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = [NAME_FIELD, IS_PUBLISHED_FIELD]
    list_editable = [IS_PUBLISHED_FIELD]
    list_display_links = [NAME_FIELD]
    filter_horizontal = [TAGS_FIELD]
