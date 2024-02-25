from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from datetime import datetime

from eventrequests.models import Event, AvWindow

from .forms import WindowForm


CustomUser = get_user_model()


def get_all_windows():
    return sorted(AvWindow.objects.filter(event__isnull=True), key=lambda x: [x.date, x.time])


def to_datetime(date, time):
    str_time = time.strftime('%H:%M:%S')
    str_date = date.strftime('%Y-%m-%d')
    dt = datetime.strptime(
        str_date + " " + str_time, '%Y-%m-%d %H:%M:%S')
    return dt


@login_required
def user_page(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:

        if not (request.user.is_staff or request.user.is_superuser):
            return Http404

        try:
            id = request.POST.get('id')
            event = Event.objects.get(id=id)
            event.status = True
            return JsonResponse()
        except Exception:
            return HttpResponseBadRequest({'message': "Произошла ошибка."}, status=400)
    else:
        template_name = 'account/account.html'
        current_user = request.user

        if current_user.is_staff or current_user.is_superuser:
            events = Event.objects.filter()

        else:
            events = Event.objects.filter(user=current_user)
        places = set()
        for event in events:
            places.add(event.window.place)
        if request.method == 'GET':
            form = WindowForm(request.GET)

        elif request.method == 'POST' and request.user.is_staff:

            if not (request.user.is_staff or request.user.is_superuser):
                return Http404

            form = WindowForm(request.POST)

            if form.is_valid():
                time = form.cleaned_data['time']
                date = form.cleaned_data['date']
                dt = to_datetime(date, time)
                place = form.cleaned_data['place']

                windows = AvWindow.objects.filter(place=place)
                for i in windows:
                    i_dt = to_datetime(i.date, i.time)
                    if (i.date == date):
                        if (dt - i_dt).total_seconds() / 60 < 20:
                            message = "На данное время невозможно создать таймслот: слишком маленький интервал между событиями."
                            return render(request, template_name, {'user': current_user, 'events': events, 'form': form, 'windows': get_all_windows(), "message": message, })
                form.save()

            form.clean()
        return render(request, template_name, {'user': current_user, 'events': events, 'form': form, 'places': places, 'windows': get_all_windows()})
