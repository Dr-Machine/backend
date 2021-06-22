import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import CustomUser

from profiles.validators import mobile_regex, validate_national_ID


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11,
                              default=None,
                              null=True,
                              blank=True,
                              validators=[mobile_regex])
    mobile_confirmed = models.BooleanField(default=False)
    national_id = models.CharField(max_length=10,
                                   default=None,
                                   null=True,
                                   blank=True,
                                   validators=[validate_national_ID])
    national_id_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
