import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .tasks import resize_image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".gif", ".png"}


@receiver(post_save, sender=Comment)
def handle_attachment_after_save(sender, instance, created, **kwargs):
    """
    If picture in comments run Celery.
    """

    if not instance.mediafile:
        return

    if created and instance.mediafile:
        file_path = instance.mediafile.path

        _, ext = os.path.splitext(file_path)

        if ext.lower() in IMAGE_EXTENSIONS:
            resize_image.delay(file_path)
