from django.contrib import admin

import catalog.models

admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.ItemMainImage)
admin.site.register(catalog.models.ItemImages)


NAME_FIELD = catalog.models.Item.name.field.name
IS_PUBLISHED_FIELD = catalog.models.Item.is_published.field.name
TAGS_FIELD = catalog.models.Item.tags.field.name
UPDATED_AT_FIELD = catalog.models.Item.updated_at.field.name
CREATED_AT_FIELD = catalog.models.Item.created_at.field.name


class ItemMainImageInline(admin.StackedInline):
    model = catalog.models.ItemMainImage
    extra = 1
    max_num = 1


class ItemImagesInline(admin.TabularInline):
    model = catalog.models.ItemImages
    extra = 1


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    def get_main_image_tmb(self, obj):
        if hasattr(obj, "main_image") and obj.main_image:
            return obj.main_image.image_tmb()

        return "Нет изображения"

    get_main_image_tmb.short_description = "Превью"

    list_display = [
        NAME_FIELD,
        IS_PUBLISHED_FIELD,
        get_main_image_tmb.__name__,
    ]
    list_editable = [IS_PUBLISHED_FIELD]
    list_display_links = [NAME_FIELD]
    filter_horizontal = [TAGS_FIELD]
    inlines = [ItemMainImageInline, ItemImagesInline]
    readonly_fields = [UPDATED_AT_FIELD, CREATED_AT_FIELD]


__all__ = []
