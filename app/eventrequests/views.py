from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Signatory, Event, AvWindow, HonoredGuest, Subceremony, Speaker
from .forms import EventForm, HonoredGuestFormset, SubceremonyFormset, SpeakerFormset

from django.views.decorators.csrf import csrf_exempt


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
        print(event_form.is_valid(), subceremony_formset.is_valid(),
              honoredguests_formset.is_valid(), speakers_formset.is_valid())
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
                    raise Exception('')
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
