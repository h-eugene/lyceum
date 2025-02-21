import django.contrib.admin

import catalog.models

django.contrib.admin.site.register(catalog.models.Category)
django.contrib.admin.site.register(catalog.models.Tag)


NAME_FIELD = catalog.models.Item.name.field.name
IS_PUBLISHED_FIELD = catalog.models.Item.is_published.field.name
TAGS_FIELD = catalog.models.Item.tags.field.name


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = [NAME_FIELD, IS_PUBLISHED_FIELD]
    list_editable = [IS_PUBLISHED_FIELD]
    list_display_links = [NAME_FIELD]
    filter_horizontal = [TAGS_FIELD]
