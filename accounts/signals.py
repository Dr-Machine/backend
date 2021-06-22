from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from accounts.utils import create_user_media_directory


@receiver(post_save, sender=CustomUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            create_user_media_directory(
                user_media_directory_path=instance.media_path)
