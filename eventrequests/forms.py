from django import forms
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Event, Signatory, HonoredGuest, AvWindow

CustomUser = get_user_model()


class EventForm(forms.ModelForm):
    presents = forms.ChoiceField(
        required=True,
        label="Обмен подарками во время церемонии",
        widget=forms.RadioSelect,
        choices=[
            (True, 'Да'),
            (False, 'Нет')
        ],
        initial=True,
    )
    press_briefing = forms.ChoiceField(
        required=True,
        label="Пресс-подход (наличие прессы обеспечивает заказчик)",
        widget=forms.RadioSelect,
        choices=[
            (True, 'Да'),
            (False, 'Нет')
        ],
        initial=False,
    )
    is_online = forms.ChoiceField(
        required=True,
        label="В каком формате будет проходить церемония",
        widget=forms.RadioSelect,
        choices=[
            (False, 'Церемония сполным присутствием (все стороны присутствуют взале)'),
            (True, 'Удаленная онлайн-церемония (одна из сторон подписывает соглашение онлайн)')
        ],
        initial=False,
    )
    time_for_speakers = forms.ChoiceField(
        required=False,
        label="Слово предоставляется:",
        widget=forms.RadioSelect,
        choices=[
            ('В конце церемонии', 'В конце церемонии'),
            ('В начале церемонии', 'В начале церемонии')
        ],
    )
    resp_is_repr = forms.ChoiceField(
        required=True,
        label="Представитель на площадке Форума совпадает с лицом, ответственным за заявку",
        widget=forms.RadioSelect(),
        choices=[
            (True, 'Да, это тот же человек'),
            (False, 'Нет, это другой человек')
        ],
    )

    honored_guests_format = forms.ChoiceField(
        required=False,
        label="Формат участия почетных гостей",
        widget=forms.RadioSelect,
        choices=[
            (True, 'Приглашаются вместе с подписантами. Во время церемонии стоят за спинами подписантов'),
            (False, 'Присутствуют в зале, представляются модератором, но не выходят на сцену')
        ],
        initial=True,
    )

    window = forms.ModelChoiceField(
        label="Дата, время, место (из доступных):",
        queryset=AvWindow.objects.filter(event__isnull=True),
        widget=forms.Select(attrs={'class': 'form-application',
                                   'rows': 1,
                                   'cols': 30,
                                   'placeholder': "Введите текст:", }))

    name = forms.CharField(
        label="Фамилия, имя, отчество (полностью):",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    org_name = forms.CharField(
        label="Организация:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:",

        }))
    position = forms.CharField(
        label="Должность:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    phone_number = forms.CharField(
        label="Мобильный телефон:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    email = forms.EmailField(
        label="Email:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    repr_name = forms.CharField(
        required=False,
        label="Фамилия, имя, отчество (полностью):",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    repr_org_name = forms.CharField(
        required=False,
        label="Организация:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:",

        }))
    repr_position = forms.CharField(
        required=False,
        label="Должность:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    repr_phone_number = forms.CharField(
        required=False,
        label="Мобильный телефон:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    repr_email = forms.EmailField(
        required=False,
        label="Email:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    class Meta:

        model = Event
        fields = ('customer_name',
                  'doc_name',
                  'window',
                  'presents',
                  'press_briefing',
                  'is_online',
                  'resp_is_repr',
                  'name',
                  'org_name',
                  'position',
                  'phone_number',
                  'email',
                  'honored_guests_format',)

        labels = {'customer_name': "Название организации-заказчика:",
                  'doc_name': "Полное наименование подписываемого документа:",

                  }

        widgets = {'customer_name': forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }),

            'doc_name': forms.Textarea(attrs={
                'class': 'form-application',
                'rows': 1,
                'cols': 30,
                'placeholder': "Введите текст:"
            }),

        }


class SignatoryForm(forms.ModelForm):
    org_name = forms.CharField(
        label="Полное наименование стороны (организации) – участника подписания соглашения:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    position = forms.CharField(
        label="Должность подписанта:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    is_man = forms.ChoiceField(
        label="Форма обращения:",
        widget=forms.RadioSelect(),
        choices=[
            (True, 'Господин'),
            (False, 'Госпожа')
        ]
    )

    signatory_surname = forms.CharField(
        label="Фамилия:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    signatory_name = forms.CharField(
        label="Имя:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))
    signatory_middlename = forms.CharField(
        label="Отчество:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    signatory_name_translate = forms.CharField(
        label="Написание имени и фамилии подписанта на английском языке:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    class Meta:
        model = Signatory
        fields = [
            'org_name',
            'position',
            'is_man',
            'signatory_surname',
            'signatory_name',
            'signatory_middlename',
            'signatory_name_translate',
        ]


class HonoredGuestForm(forms.ModelForm):
    name = forms.CharField(
        label="Фамилия, имя, отчество почетного гостя:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    position = forms.CharField(
        label="Должность почетного гостя с указанием организации:",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите текст:"
        }))

    class Meta:
        model = HonoredGuest
        fields = [
            'name',
            'position',
        ]


SignatoryFormset = modelformset_factory(
    model=Signatory,
    form=SignatoryForm,
    fields=[
        'org_name',
        'position',
        'is_man',
        'signatory_surname',
        'signatory_name',
        'signatory_middlename',
        'signatory_name_translate',
    ],
    extra=0,
    min_num=2,
    max_num=30,)

HonoredGuestFormset = modelformset_factory(
    model=HonoredGuest,
    form=HonoredGuestForm,
    fields=[
        'name',
        'position',
    ],
    max_num=10
)
