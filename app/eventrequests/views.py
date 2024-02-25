from django.http import FileResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.conf import settings

import os
from docxtpl import DocxTemplate

from .models import Event, AvWindow, HonoredGuest, Subceremony, Speaker
from .forms import EventForm, HonoredGuestFormset, SubceremonyFormset, SpeakerFormset


@login_required
def delete_window(request, *args, **kwargs):
    if request.user.is_staff or request.user.is_superuser:
        object = AvWindow.objects.get(id=kwargs['pk'])
        object.delete()
        return HttpResponseRedirect(reverse('account'))
    else:
        return Http404()


@login_required
def create_event(request):
    template_name = 'form.html'
    if request.method == 'GET':
        event_form = EventForm()
        honoredguests_formset = HonoredGuestFormset(
            request.GET or None, queryset=Event.objects.none(), prefix="guests")
        subceremony_formset = SubceremonyFormset(
            request.GET or None, queryset=Event.objects.none(), prefix="subceremony")
        speakers_formset = SpeakerFormset(
            request.GET or None, queryset=Event.objects.none(), prefix="speakers")
    else:
        event_form = EventForm(request.POST)
        honoredguests_formset = HonoredGuestFormset(
            request.POST, prefix="guests")
        subceremony_formset = SubceremonyFormset(
            request.POST, prefix="subceremony")
        speakers_formset = SpeakerFormset(request.POST, prefix="speakers")
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.user = request.user
            subceremony_formset = SubceremonyFormset(
                request.POST, prefix="subceremony", instance=event)

            if event_form.is_valid() and subceremony_formset.is_valid() and honoredguests_formset.is_valid() and speakers_formset.is_valid():
                try:
                    event.save()
                    subceremony_formset.save()

                    for instance in honoredguests_formset:
                        instance = instance.save(commit=False)
                        instance.event = event
                        instance.save()

                    for instance in speakers_formset:
                        instance = instance.save(commit=False)
                        instance.event = event
                        instance.save()
                except Exception:
                    if (Event.objects.filter(id=event.id).exists()):
                        Event.objects.filter(id=event.id).delete()
                    return render(request, template_name, {
                        'guests_formset': honoredguests_formset,
                        'subceremonies_formset': subceremony_formset,
                        'speakers_formset': speakers_formset,
                        'form': event_form,
                        'success': False,
                    })

                return HttpResponseRedirect(reverse("account"))

    return render(request, template_name, {
        'guests_formset': honoredguests_formset,
        'subceremonies_formset': subceremony_formset,
        'speakers_formset': speakers_formset,
        'form': event_form,
        'success': True,

    })


@login_required
def show_event(request, *args, **kwargs):
    template_name = "event_view.html"
    try:
        event = Event.objects.get(id=kwargs['pk'])

        subceremonies = Subceremony.objects.filter(event=event)
        honored_guests = HonoredGuest.objects.filter(event=event)
        speakers = Speaker.objects.filter(event=event)
        if event.user == request.user or request.user.is_superuser or request.user.is_staff:
            return render(request, template_name=template_name, context={'event': event, 'subceremonies': subceremonies, 'honored_guests': honored_guests, 'speakers': speakers})
        else:
            return Http404
    except KeyError:
        return Http404


@login_required
def download_event(request, *args, **kwargs):
    print(os.listdir())
    user = request.user
    if user.is_staff or user.is_superuser:
        event_id = kwargs['pk']
        event = Event.objects.get(id=event_id)
        try:
            path = os.path.join(settings.MEDIA_ROOT,
                                "events/event_%s.docx" % event_id)
            f = open(path)
            f.close()
        except FileNotFoundError:
            path = create_file(event)
        response = FileResponse(open(path, 'rb'))
        filename = "event_%s.docx" % event_id
        response['Content-Disposition'] = 'inline; filename=' + filename
        return response
    return Http404


def create_file(event):
    context = {}
    context['event'] = event

    context['subceremonies'] = Subceremony.objects.filter(event=event)
    context['honoredguests'] = HonoredGuest.objects.filter(event=event)
    context['speakers'] = Speaker.objects.filter(event=event)

    doc = DocxTemplate(os.path.join(settings.STATIC_ROOT,
                                    "textfiles/event_template.docx"))
    doc.render(context)
    path = os.path.join(settings.BASE_DIR,
                        'media/events/event_%s.docx' % event.id)
    print(path)
    doc.save(path)
    return path
