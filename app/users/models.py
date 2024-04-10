import uuid

from django.db import models
from django.core import serializers
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

    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_superuser = models.BooleanField(default=False, verbose_name='Админ')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    required_fields = []

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})

    def toJSON(self):
        serialized_obj = serializers.serialize(
            'json', [self,], fields=['id', 'email', 'is_staff', 'is_superuser'])
        return serialized_obj

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('special_status', _("Can change event performer"))
        ]


class CustomUserManager(models.Model):
    def get_all(self):
        qs = CustomUser.objects.all()
        return qs
