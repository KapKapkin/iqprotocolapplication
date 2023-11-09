from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django import forms

from .models import Event, Signatory

class SignatoryAdminForm(forms.ModelForm):
    signatories = forms.ModelChoiceField(queryset=Signatory.objects.all())
    

class SignatoryInline(admin.TabularInline):
    model = Signatory
    form = SignatoryAdminForm
    formfield_overrides = {
        models.CharField: {'widget' : TextInput(attrs={'size':'10'})} 
    }  
    min_num = 2



class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.get_fields()]
    inlines = [
        SignatoryInline,
    ]
    

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin, )
