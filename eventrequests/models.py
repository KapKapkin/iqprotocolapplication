import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Event(models.Model):
    id = models.UUIDField(_('id'),
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          db_index=True,
                          unique=True,)
    
    customer_name = models.CharField(max_length=255, blank=False)
    doc_name = models.CharField(max_length=255, blank=False)
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=255, blank=False)

    presents = models.BooleanField(default=False)
    press_briefing = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    resp_is_repr = models.BooleanField(default=True)

    name = models.CharField(max_length=255, blank=False)
    org_name = models.CharField(max_length=255, blank=False)
    position = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    email = models.EmailField(max_length=255, blank=False)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    

class Signatory(models.Model):
    id = models.UUIDField(_('id'),
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          db_index=True,
                          unique=True,)
    
    org_name = models.CharField(max_length=255, blank=False)
    position = models.CharField(max_length=255, blank=False)
    is_man = models.BooleanField(default=True)
    signatory_name = models.CharField(max_length=255, blank=False)
    signatory_name_translate = models.CharField(max_length=255, blank=False)
    
    is_speaker = models.BooleanField(default=False)
    is_additional_speaker = models.BooleanField(default=False)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="signatories")
    

    
