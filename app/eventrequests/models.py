import uuid
import datetime

from django.db import models
from django.core import serializers
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class AvWindow(models.Model):
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=255, blank=True, default='')

    objects = models.Manager()

    def __str__(self):
        res = str(self.date) + " " + str(self.time) + " " + str(self.place)
        events = Event.objects.all()
        for event in events:
            if (event.window == self):
                res += " - Занято"
                break
        else:
            res += " - Свободно"
        return res

    def toJSON(self):
        serialized_obj = serializers.serialize(
            'json', [self,], fields=['id', 'date', 'time', 'place'])
        return serialized_obj

    class Meta:
        verbose_name = 'Окна (дата, время, место)'


class Event(models.Model):

    number = models.IntegerField()

    customer_name = models.CharField(
        max_length=255, blank=False, verbose_name="Название организации-заказчика")
    doc_name = models.CharField(max_length=255, blank=False,
                                verbose_name="Полное наименование подписываемого документа")
    window = models.OneToOneField(
        AvWindow, on_delete=models.CASCADE, related_name='event', verbose_name="Дата, время, место")

    presents = models.BooleanField(
        default=False, verbose_name="Обмен подарками во время церемонии")
    press_briefing = models.BooleanField(
        default=False, verbose_name="Пресс-подход (наличие прессы обеспечивает заказчик)")
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

    time_for_speakers = models.IntegerField(
        blank=True, null=True, default=0, verbose_name='Слово предоставляется')

    repr_name = models.CharField(
        max_length=255, blank=True, default='', verbose_name="Фамилия, имя, отчество (полностью)")
    repr_org_name = models.CharField(
        max_length=255, blank=True, default='', verbose_name="Организация")
    repr_position = models.CharField(
        max_length=255, blank=True, default='', verbose_name="Должность")
    repr_phone_number = models.CharField(
        max_length=20, blank=True, default='', verbose_name="Мобильный телефон")
    repr_email = models.EmailField(
        max_length=255, blank=True, default='', verbose_name="Email")

    honored_guests_format = models.IntegerField(
        default=0, verbose_name="Формат почётных гостей")

    performer = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name="Исполнитель")

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="events")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.object_list = Event.objects.order_by('number')
        if not self.number:
            if len(self.object_list) == 0:
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

    def get_absolute_url(self):
        return reverse('event', kwargs={'pk': self.pk})

    def toJSON(self):
        serialized_obj = serializers.serialize(
            'json', [self,], fields=['id', 'window', 'user', 'performer'])
        return serialized_obj

    class Meta:
        verbose_name = _("Событие")
        verbose_name_plural = _("События")


class Subceremony(models.Model):
    discription = models.CharField(
        max_length=255, default='-', verbose_name="Описание")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name="Событие")

    objects = models.Manager()

    class Meta:
        verbose_name = _("Вагон")
        verbose_name_plural = _("Вагоны")


class Speaker(models.Model):
    name = models.CharField(
        max_length=255, default=None, verbose_name="ФИО")
    position = models.CharField(
        max_length=255, blank=False, verbose_name="Должность с указанием организации.")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="speakers")

    objects = models.Manager()

    class Meta:
        verbose_name = _("Спикер")
        verbose_name_plural = _("Спикеры")


class Signatory(models.Model):
    org_name = models.CharField(max_length=255,
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

    subceremony = models.ForeignKey(
        Subceremony, on_delete=models.CASCADE, related_name="signatories")

    objects = models.Manager()

    class Meta:
        verbose_name = _('Участник форума')
        verbose_name_plural = _("Участники форума")


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

    objects = models.Manager()

    class Meta:
        verbose_name = _("Почётный гость")
        verbose_name_plural = "Почётные гости"
