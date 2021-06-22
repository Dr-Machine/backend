import os

from backend.settings.base import MEDIA_ROOT


def create_user_media_directory(user_media_directory_path: str) -> None:
    path = os.path.join(MEDIA_ROOT, user_media_directory_path)
    os.makedirs(path)
