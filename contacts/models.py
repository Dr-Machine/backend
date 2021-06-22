import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=1024)

    def __str__(self):
        return self.email
