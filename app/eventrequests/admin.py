from django.utils.encoding import force_str
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.forms.formsets import all_valid
from django import forms
from django.db.models import Q

import nested_admin

from .models import Event, Signatory, HonoredGuest, AvWindow, Subceremony, Speaker


class SpeakerInline(nested_admin.NestedTabularInline):
    model = Speaker
    min_num = 0

    extra = 1


class HonoredGuestInline(nested_admin.NestedTabularInline):
    model = HonoredGuest
    min_num = 0
    extra = 1


class SignatoryInline(nested_admin.NestedTabularInline):
    model = Signatory
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})}
    }
    min_num = 2
    extra = 0


class SignatoryAdmin(nested_admin.NestedModelAdmin):
    list_display = ["id", ]
    fieldsets = (
        (None, {
            'fields': (
                "__all__",
            ),
        }),
    )


class SubceremonyInline(nested_admin.NestedStackedInline):
    model = Subceremony
    min_num = 1
    extra = 0
    inlines = [SignatoryInline,]


class EventAdminForm(forms.ModelForm):
    CHOICES1 = [(1, 'Приглашаются вместе с подписантами. Во время церемонии стоят за спинами подписантов'),
                (2, 'Присутствуют в зале, представляются модератором, но не выходят на сцену'),
                (0, 'Не присутствуют')]
    CHOICES2 = [(1, 'В начале церемонии'),
                (2, 'В конце церемонии'),
                (0, 'Не предоставляется')]

    honored_guests_format = forms.ChoiceField(
        required=True,
        label="Формат участия почетных гостей",
        widget=forms.RadioSelect,
        choices=CHOICES1
    )
    time_for_speakers = forms.ChoiceField(
        required=True,
        label=" Слово предоставляется",
        widget=forms.RadioSelect,
        choices=CHOICES2
    )
    performer = forms.ModelChoiceField(required=False, label="Исполнитель", queryset=get_user_model(
    ).objects.filter(Q(is_superuser=True) | Q(is_staff=True)))


class EventAdmin(nested_admin.NestedModelAdmin):
    list_display = ['number', 'doc_name', 'window']
    inlines = [
        SpeakerInline,
        HonoredGuestInline,
        SubceremonyInline,
    ]
    form = EventAdminForm
    fieldsets = (

        (_("Вводные данные о церемонии"), {
         "fields": ('customer_name', 'doc_name', 'window')}),
        (
            _("Дополнительные опции"),
            {
                "fields": (
                    "presents", 'press_briefing', 'is_online',
                ),
            },
        ),
        (_("Контактные данные лица, ответственного за заявку"), {
         "fields": ("name", 'org_name', 'position', 'phone_number', "email")}),

        (_("Контактные данные представителя, присутствующего на площадке Форума "), {
         "fields": ('resp_is_repr', "repr_name", 'repr_org_name', 'repr_position', 'repr_phone_number', "repr_email",)}),

        (_("Исполнитель"), {
            "fields": ('performer',),
        }),
        (_("Кому принадлежит заявка"), {
            "fields": ('user',),
        }),
        (_("Спикеры"), {
            "fields": ("time_for_speakers",
                       "speakers_inline"
                       ),
        }),
        (_("Формат почётных гостей"), {
            "fields": ("honored_guests_format",
                       "honored_guests_inline"
                       )}),
    )
    readonly_fields = "speakers_inline", "honored_guests_inline",

    def speakers_inline(self, *args, **kwargs):
        context = getattr(self.response, 'context_data', None) or {
        }  # somtimes context.copy() is better
        inline = context['inline_admin_formset'] = context['inline_admin_formsets'].pop(
            0)
        return get_template(inline.opts.template).render(context, self.request)

    def honored_guests_inline(self, *args, **kwargs):
        context = getattr(self.response, 'context_data', None) or {
        }  # somtimes context.copy() is better
        inline = context['inline_admin_formset'] = context['inline_admin_formsets'].pop(
            0)
        return get_template(inline.opts.template).render(context, self.request)

    def render_change_form(self, request, *args, **kwargs):
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response

    class Meta:
        model = Event

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '/static/admin/js/hide_responsible.js',
        )


class AvWindowAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'time', 'place']

    class Meta:
        model = AvWindow


admin.site.register(AvWindow, AvWindowAdmin)
admin.site.register(Event, EventAdmin)
