import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        _('id'), 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    email = models.CharField(_('Email'), max_length=255, unique=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    required_fields = []

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})


class CustomUserManager(models.Model):
    def get_all(self):
        qs = CustomUser.objects.all()
        return qs