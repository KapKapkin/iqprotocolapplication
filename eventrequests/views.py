from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives

from django.utils.html import strip_tags
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import Http404

import os

from .models import Signatory, Event, AvWindow, HonoredGuest
from .forms import EventForm, SignatoryFormset, HonoredGuestFormset
from iqprotocolapplication.settings import TEMPLATES_DIR


@login_required
def delete_window(request, *args, **kwargs):
    object = AvWindow.objects.get(id=kwargs['pk'])
    object.delete()
    return HttpResponseRedirect(reverse('account'))


@login_required
def create_event(request):
    template_name = 'form.html'
    if request.method == 'GET':
        eventform = EventForm()
        guests_formset = HonoredGuestFormset(
            request.GET or None, queryset=Event.objects.none(), prefix="guests")
        formset = SignatoryFormset(
            request.GET or None, queryset=Event.objects.none(), prefix="sig")

    elif request.method == 'POST':

        eventform = EventForm(request.POST)
        formset = SignatoryFormset(request.POST, prefix="sig")
        guests_formset = HonoredGuestFormset(request.POST, prefix="guests")
        if eventform.is_valid() and formset.is_valid() and guests_formset.is_valid():
            save_stack = []
            event = eventform.save(commit=False)

            event.user = request.user
            save_stack.append(event)

            num = 0
            for form in guests_formset:
                guest = form.save(commit=False)
                guest.event = event
                save_stack.append(guest)
            for form in formset:
                signatory = form.save(commit=False)
                if request.POST.get(f'participant{num + 1}', 1):
                    signatory.is_speaker = True
                    signatory.event = event
                    save_stack.append(signatory)
                    num += 1
            for element in save_stack:
                element.save()
            if request.POST.get('participant1-name', 1):

                name = request.POST.get('participant1-name')
                surname = request.POST.get('participant1-surname')
                middlename = request.POST.get('participant1-middlename')
                if name:
                    guest = Signatory.objects.create(signatory_surname=surname,
                                                     signatory_name=name,
                                                     signatory_middlename=middlename, position=request.POST['participant1-position'], is_speaker=True, is_additional_speaker=True, event=event)

            content = render_to_string(os.path.join(str(TEMPLATES_DIR), 'account/email/event_created.txt'), context={
                'event_id': event.id, 'request': RequestContext(request)})
            subject = render_to_string(os.path.join(
                str(TEMPLATES_DIR), 'account/email/event_created_subject.txt'))

            message = EmailMultiAlternatives(
                subject=subject,
                body=strip_tags(content),
                from_email=None,
                to=(request.user.email,)
            )
            message.attach_alternative(content, "text/html")
            message.send()

            return HttpResponseRedirect(reverse("account"))

    return render(request, template_name, {
        'guests_formset': guests_formset,
        'sig_formset': formset,
        'form': eventform,
    })


def show_event(request, *args, **kwargs):
    template_name = "event_view.html"
    try:
        event = Event.objects.get(id=kwargs['pk'])
        signatories = Signatory.objects.filter(event=event)
        honored_guests = HonoredGuest.objects.filter(event=event)
        speakers = Signatory.objects.filter(
            event=event).filter(is_speaker=True)
        if event.user == request.user or request.user.is_super or request.user.is_employee:
            return render(request, template_name=template_name, context={'event': event, 'signatories': signatories, 'honored_guests': honored_guests, 'speakers': speakers})
        else:
            return Http404
    except KeyError:
        return Http404
