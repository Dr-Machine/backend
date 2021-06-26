import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import BaseCase

from backend.settings import MEDIA_ROOT

from CT_LIS.validators import validate_file_size, validate_involvement

SERVICE_NICKNAME = 'CT_LIS'


def get_file_path(instance, filename):
    files_directory = os.path.join(instance.prescriber.media_path,
                                   SERVICE_NICKNAME, 'cases')
    file_path = os.path.join(files_directory, filename)
    return file_path


class CTLungInfectionSegmentation(BaseCase):
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
    upper_left = models.FloatField(blank=True,
                                   null=True,
                                   validators=[validate_involvement])
    upper_right = models.FloatField(blank=True,
                                    null=True,
                                    validators=[validate_involvement])
    lower_left = models.FloatField(blank=True,
                                   null=True,
                                   validators=[validate_involvement])
    lower_middle = models.FloatField(blank=True,
                                     null=True,
                                     validators=[validate_involvement])
    lower_right = models.FloatField(blank=True,
                                    null=True,
                                    validators=[validate_involvement])
    report = models.TextField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def service_directory_path(self):
        directory_path = os.path.join(self.prescriber.media_path,
                                      SERVICE_NICKNAME)
        directory_path = f'{MEDIA_ROOT}/{directory_path}'
        return directory_path

    @property
    def cases_directory_path(self):
        cases_path = os.path.join(self.service_directory_path, 'cases')
        if not os.path.isdir(cases_path):
            os.makedirs(cases_path)
        return cases_path

    @property
    def results_directory_path(self):
        results_path = os.path.join(self.service_directory_path, 'results')
        if not os.path.isdir(results_path):
            os.makedirs(results_path)
        return results_path
