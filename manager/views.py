from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from gatekeeper.decorators import is_logged_in
from .models import Manager
from reception.models import Visitor
from datetime import datetime
from django.utils import timezone
import pusher


def login(request):
    if 'manager_id' in request.session:
        return redirect('manager-dashboard')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            manager = Manager.objects.get(email=email, password=password)
            request.session['manager_id'] = manager.id
            return redirect('manager-dashboard')
        except Manager.DoesNotExist:
            try:
                Manager.objects.get(email=email)
            except Manager.DoesNotExist:
                error = 'Your email does not belong to an account'
                messages.add_message(request, messages.ERROR, error)
                return render(request, 'manager/login.html')
            else:
                error = 'You entered an incorrect password'
                messages.add_message(request, messages.ERROR, error)
                return render(request, 'manager/login.html', {'email': email})
    else:
        return render(request, 'manager/login.html')


@is_logged_in('manager')
def dashboard(request):
    manager_id = request.session.get('manager_id')
    manager = Manager.objects.get(id=manager_id)

    visitors = Visitor.objects.filter(company_to_visit=manager)

    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    visitors_today = visitors.filter(in_time__range=(today_min, today_max)).order_by('-in_time')

    return render(request, 'manager/dashboard.html',
                  {
                      'manager': manager,
                      'all_visitors': visitors,
                      'visitors_today': visitors_today,
                  })


@is_logged_in('manager')
def logout(request):
    if request.method == 'POST':
        del request.session['manager_id']
        return redirect('manager-login')
    else:
        raise Http404


@is_logged_in('manager')
def all_visitors(request):
    manager_id = request.session.get('manager_id')
    manager = Manager.objects.get(id=manager_id)

    visitors = Visitor.objects.all()
    return render(request, 'manager/all-visitors.html',
                  {
                      'manager': manager,
                      'visitors': visitors,
                  })
# TODO: get visitors on
