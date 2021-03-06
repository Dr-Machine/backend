import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from accounts.utils import create_user_media_directory

logger = logging.getLogger('backend')


@receiver(post_save, sender=CustomUser)
def CustomUserSignla(sender, instance, created, **kwargs):
    if created:
        logger.info('Running functions at new Custom User creation...')

        if not instance.is_superuser:
            create_user_media_directory(
                user_media_directory_path=instance.media_path)

        logger.info('Functions at new Custom User creation done!')
