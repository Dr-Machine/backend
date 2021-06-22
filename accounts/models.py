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
        timestamp = str(self.date_joined).split(' ')[0]
        directory_name = f'{timestamp}_{self.nickname}'
        return directory_name


# class Profile(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)
#     mobile = models.CharField(max_length=11,
#                               default=None,
#                               null=True,
#                               blank=True,
#                               validators=[mobile_regex])
#     mobile_confirmed = models.BooleanField(default=False)
#     national_id = models.CharField(max_length=10,
#                                    default=None,
#                                    null=True,
#                                    blank=True,
#                                    validators=[validate_national_ID])
#     national_id_confirmed = models.BooleanField(default=False)
#     medical_id = models.CharField(
#         max_length=15,  # todo: R&D on real length
#         default=None,
#         null=True,
#         blank=True)
#     medical_id_confirmed = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.user)


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
