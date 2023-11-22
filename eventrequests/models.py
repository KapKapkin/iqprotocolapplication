import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class AvWindow(models.Model):
    id = models.AutoField(primary_key=True)

    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return str(self.date) + " " + str(self.time) + " " + str(self.place)

    class Meta:
        verbose_name = 'Окна (дата, время, место)'


class Event(models.Model):
    id = models.UUIDField(_('id'),
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          db_index=True,
                          unique=True,)
    number = models.IntegerField()

    customer_name = models.CharField(
        max_length=255, blank=False, verbose_name="Название организации-заказчика")
    doc_name = models.CharField(max_length=255, blank=False,
                                verbose_name="Полное наименование подписываемого документа")
    window = models.OneToOneField(
        AvWindow, on_delete=models.CASCADE, related_name='event', verbose_name="Дата, время, место (из доступных)")

    presents = models.BooleanField(
        default=False, verbose_name="Обмен подарками во время церемонии")
    press_briefing = models.BooleanField(
        default=False, verbose_name="Предоставить возможность прессе задавать вопросы после церемонии")
    is_online = models.BooleanField(
        default=False, verbose_name="Одна из сторон подписывает соглашение онлайн")
    resp_is_repr = models.BooleanField(
        default=True, verbose_name="Представитель на площадке Форума совпадает с лицом, ответственным за заявку")

    name = models.CharField(max_length=255, blank=False,
                            verbose_name="Фамилия, имя, отчество (полностью)")
    org_name = models.CharField(
        max_length=255, blank=False, verbose_name=" Организация")
    position = models.CharField(
        max_length=255, blank=False, verbose_name="Должность")
    phone_number = models.CharField(
        max_length=20, blank=False, verbose_name="Мобильный телефон")
    email = models.EmailField(
        max_length=255, blank=False, verbose_name='Email')

    time_for_speakers = models.CharField(
        max_length=255, blank=True, default='', verbose_name='Слово предоставляется')

    repr_name = models.CharField(
        max_length=255, blank=True, default='', verbose_name="Фамилия, имя, отчество (полностью)")
    repr_org_name = models.CharField(
        max_length=255, blank=True, default='', verbose_name=" Организация")
    repr_position = models.CharField(
        max_length=255, blank=True, default='', verbose_name="Должность")
    repr_phone_number = models.CharField(
        max_length=20, blank=True, default='', verbose_name="Мобильный телефон")
    repr_email = models.EmailField(
        max_length=255, blank=True, default='', verbose_name="Email")

    honored_guests_format = models.BooleanField(default=False)

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="events")

    def save(self, *args, **kwargs):
        self.object_list = self.objects.order_by('number')
        if len(self.object_list) == 0:  # if there are no objects
            self.number = 1
        else:
            self.number = self.object_list.last().number + 1
        if self.resp_is_repr:
            self.repr_name = self.name
            self.repr_org_name = self.org_name
            self.repr_position = self.position
            self.repr_phone_number = self.phone_number
            self.repr_email = self.email
        super(Event, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Форумы"


class Signatory(models.Model):
    id = models.UUIDField(_('id'),
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          db_index=True,
                          unique=True,)

    org_name = models.CharField(max_length=255, blank=True,
                                verbose_name="Наименование стороны – участника подписания соглашения", default='')
    position = models.CharField(
        max_length=255, blank=False, verbose_name="Должность подписанта")
    is_man = models.BooleanField(
        default=True, verbose_name="Форма обращения (Если выбрать - Господин, иначе - Госпожа)")
    signatory_surname = models.CharField(
        max_length=255, default=None, verbose_name="Фамилия")
    signatory_name = models.CharField(
        max_length=255, default=None, verbose_name="Имя")
    signatory_middlename = models.CharField(
        max_length=255, default=None, verbose_name="Отчество")
    signatory_name_translate = models.CharField(
        max_length=255, blank=True, verbose_name="ФИО на англ", default='')

    is_speaker = models.BooleanField(
        default=False, verbose_name="Предоставить слово участнику")
    is_additional_speaker = models.BooleanField(
        default=False, verbose_name="Участнику предоставленно слово, но сам он не учавствует в конференции (достаточно указать ФИО и должность, остальные поля - прочерки)")

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="signatories")

    class Meta:
        verbose_name_plural = "Участники Форума"


class HonoredGuest(models.Model):
    id = models.UUIDField(_('id'),
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          db_index=True,
                          unique=True,)
    name = models.CharField(max_length=255, blank=False,
                            verbose_name="Фамилия, имя, отчество (полностью)")
    position = models.CharField(
        max_length=255, blank=False, verbose_name="Должность")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="honored_guests")

    class Meta:
        verbose_name_plural = "Почётные гости"
