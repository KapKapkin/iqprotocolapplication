from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Event, Signatory, HonoredGuest, AvWindow


class HonoredGuestInline(admin.TabularInline):
    model = HonoredGuest


class SignatoryInline(admin.TabularInline):
    model = Signatory
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})}
    }
    min_num = 2


class EventAdmin(admin.ModelAdmin):
    list_display = ['number', 'doc_name', 'window']
    inlines = [
        SignatoryInline,
        HonoredGuestInline,
    ]
    fieldsets = (

        (_("Вводные данные о церемонии"), {
         "fields": ('customer_name', 'doc_name', 'window')}),
        (
            _("Дополнительные опции (при наличии)"),
            {
                "fields": (
                    "presents", 'press_briefing', 'is_online', 'resp_is_repr', 'time_for_speakers'
                ),
            },
        ),
        (_("Контактные данные лица, ответственного за заявку"), {
         "fields": ("name", 'org_name', 'position', 'phone_number', "email",)}),
        (_("Контактные данные представителя, присутствующего на площадке Форума (ВНИМАНИЕ! если вы поставили галочку 'Представитель на площадке Форума совпадает с лицом, ответственным за заявку', то следующие поля будут заполненны автоматически значениями из предыдущего блока)"), {
         "fields": ("repr_name", 'repr_org_name', 'repr_position', 'repr_phone_number', "repr_email",)}),
        (_("Формат почётных гостей (не играет роли, если нет добавленных почётных гостей)"), {
            "fields": ("honored_guests_format",)}),

    )

    class Meta:
        model = Event

    def render_change_form(self, request, context, *args, **kwargs):
        CHOICES1 = [(True, 'Приглашаются вместе с подписантами. Во время церемонии стоят за спинами подписантов'),
                    (False, 'Присутствуют в зале, представляются модератором, но не выходят на сцену')]
        CHOICES2 = [('В начале церемонии', 'В начале церемонии'),
                    ('В конце церемонии', 'В конце церемонии')]
        context['adminform'].form.fields['window'].queryset = AvWindow.objects.filter(
            event__isnull=True)
        context['adminform'].form.fields['honored_guests_format'] = forms.ChoiceField(
            required=False,
            label="Формат участия почетных гостей",
            widget=forms.RadioSelect,
            choices=CHOICES1
        )
        context['adminform'].form.fields['time_for_speakers'] = forms.ChoiceField(
            required=True,
            label=" Слово предоставляется",
            widget=forms.RadioSelect,
            choices=CHOICES2
        )
        return super(EventAdmin, self).render_change_form(
            request, context, *args, **kwargs)


class AvWindowAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'time', 'place']

    class Meta:
        model = AvWindow


admin.site.register(AvWindow, AvWindowAdmin)
admin.site.register(Event, EventAdmin)
