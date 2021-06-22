import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def nickname(self):
        return f'{self.first_name}_{self.last_name}'.lower()

    @property
    def media_path(self):
        directory_name = str(self.id)
        return directory_name


# todo: move BaseCase somewhere else
class BaseCase(models.Model):
    class PatientSex(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        UNKNOWN = 'U', _('Unknown')

    prescriber = models.ForeignKey(CustomUser,
                                   on_delete=models.SET_NULL,
                                   null=True)
    patient_id = models.CharField(max_length=64, blank=True, null=True)
    patient_sex = models.CharField(max_length=1,
                                   choices=PatientSex.choices,
                                   default=PatientSex.UNKNOWN)
    patient_age = models.PositiveSmallIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
