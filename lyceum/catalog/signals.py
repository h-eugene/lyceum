from django.db.models.signals import post_delete
from django.dispatch import receiver
from sorl.thumbnail import delete

from catalog.models import ItemImages, ItemMainImage


@receiver(post_delete, sender=ItemMainImage)
def delete_thumbnail_main_image(sender, instance, **kwargs):
    if instance.image:
        delete(instance.image)


@receiver(post_delete, sender=ItemImages)
def delete_thumbnail_item_images(sender, instance, **kwargs):
    if instance.image:
        delete(instance.image)
