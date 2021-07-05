import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.models import BaseCase

from backend.settings import MEDIA_ROOT

from utils.validators import validate_file_size, validate_involvement

SERVICE_NICKNAME = 'ai_corona'


def get_file_path(instance, filename):
    files_directory = os.path.join(instance.prescriber.media_path,
                                   SERVICE_NICKNAME, 'cases')
    file_path = os.path.join(files_directory, filename)
    return file_path


class COVID19Diagnosis(BaseCase):
    ALLOWED_EXTENSIONS = ['zip']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(
        upload_to=get_file_path,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
            validate_file_size
        ],
        null=False,
        blank=False)
    normal = models.FloatField(blank=True,
                               null=True,
                               validators=[validate_involvement])
    pneumonia = models.FloatField(blank=True,
                                  null=True,
                                  validators=[validate_involvement])
    covid = models.FloatField(blank=True,
                              null=True,
                              validators=[validate_involvement])
    report = models.TextField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def service_directory_path(self):
        directory_path = os.path.join(self.prescriber.media_path,
                                      SERVICE_NICKNAME)
        # ! Why TF this did not work? :|
        # directory_path = f'{MEDIA_ROOT}/{directory_path}'

        directory_path = MEDIA_ROOT + directory_path
        return directory_path

    @property
    def cases_directory_path(self):
        cases_path = os.path.join(self.service_directory_path, 'cases')
        if not os.path.isdir(cases_path):
            os.makedirs(cases_path)
        return cases_path

    @property
    def case_directory_path(self):
        p = f'{self.cases_directory_path}/{self.id}/'
        print(f'{p = }')
        return p
