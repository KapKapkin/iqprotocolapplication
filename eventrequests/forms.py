from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Event

CustomUser = get_user_model()

class EventForm():
    class Meta:
        model = Event
        fields = '__all__'