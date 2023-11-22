from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from eventrequests.models import Event, AvWindow

from .forms import WindowForm


CustomUser = get_user_model()


@login_required
def user_page(request):
    template_name = 'account/account.html'
    current_user = request.user
    if current_user.is_staff or current_user.is_superuser:
        events = Event.objects.filter()

    else:
        events = Event.objects.filter(user=current_user)
    windows = AvWindow.objects.filter(event__isnull=True)
    if request.method == 'GET':
        form = WindowForm(request.GET)
    elif request.method == 'POST':
        form = WindowForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, template_name, {'user': current_user, 'events': events, 'form': form, 'windows': windows})
