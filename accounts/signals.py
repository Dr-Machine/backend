import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser

from backend.settings.base import MEDIA_ROOT


@receiver(post_save, sender=CustomUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            user_media_path = os.path.join(MEDIA_ROOT, instance.media_path)
            os.makedirs(
                user_media_path)  # todo: convert to a separate utils function
