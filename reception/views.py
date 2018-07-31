from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib import messages
from django.forms.models import model_to_dict
from django.utils import timezone
from django.http import JsonResponse

from .models import Receptionist, Visitor
from manager.models import Manager

from datetime import datetime
from collections import namedtuple
import pusher
import json

from gatekeeper.decorators import is_logged_in


pusher_client = pusher.Pusher(
        app_id='558783',
        key='42f9ee7dff98a91b754c',
        secret='8d636a26b6180cd288e1',
        cluster='ap2',
        ssl=True
    )


def login(request):
    if 'receptionist_id' in request.session:
        return redirect('reception-dashboard')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            receptionist = Receptionist.objects.get(email=email, password=password)
            request.session['reception_id'] = receptionist.id
            return redirect('reception-dashboard')
        except Receptionist.DoesNotExist:
            try:
                Receptionist.objects.get(email=email)
            except Receptionist.DoesNotExist:
                error = 'Your email does not belong to an account'
                messages.add_message(request, messages.INFO, error)
                return render(request, 'reception/login.html')
            else:
                error = 'You entered an incorrect password'
                messages.add_message(request, messages.ERROR, error)
                return render(request, 'reception/login.html', {'email': request.POST.get('email', None)})
    else:
        return render(request, 'reception/login.html')


@is_logged_in('reception')
def dashboard(request):
    reception_id = request.session.get('reception_id')
    receptionist = Receptionist.objects.get(id=reception_id)
    managers = Manager.objects.all()

    total_visitors = len(Visitor.objects.all())

    visitors = get_all_visitors_sorted(managers)

    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    visitors_today = Visitor.objects.filter(in_time__range=(today_min, today_max)).order_by('-in_time')

    return render(request, 'reception/dashboard.html',
                  {
                      'receptionist': receptionist,
                      'all_visitors': visitors,
                      'total_visitors': total_visitors,
                      'visitors_today': visitors_today,
                      'total_companies': len(managers)
                  })


def get_all_visitors_sorted(managers):
    max_visitors = max(len(Visitor.objects.filter(company_to_visit=manager)) for manager in managers)

    VisitorInfo = namedtuple('VisitorInfo', 'company visitors percentage')
    visitors = []
    for manager in managers:
        v = Visitor.objects.filter(company_to_visit=manager)  # get all visitors for one company/manager
        vp = round(100. * len(v) / max_visitors)
        visitors.append(VisitorInfo(company=manager.company_name, visitors=v, percentage=vp))

    return sorted(visitors, key=lambda x: x.percentage, reverse=True)


@is_logged_in('reception')
def logout(request):
    if request.method == 'POST':
        del request.session['reception_id']
        return redirect('reception-login')
    else:
        raise Http404


@is_logged_in('reception')
def add_visitor(request):
    if request.method == 'GET':
        reception_id = request.session.get('reception_id')
        receptionist = Receptionist.objects.get(id=reception_id)
        companies = Manager.objects.all()
        return render(request, 'reception/add-visitor.html', {
            'companies': companies,
            'receptionist': receptionist
        })
    else:
        first_name = request.POST.get('first_name', None)
        middle_name = request.POST.get('middle_name', None)
        last_name = request.POST.get('last_name', None)
        gender = request.POST.get('gender', None)
        dob = request.POST.get('dob', None)
        phone1 = request.POST.get('phone1', None)
        phone2 = request.POST.get('phone2', None)
        email = request.POST.get('email', None)
        #  TODO: Add address variables
        card_id = request.POST.get('card_id', None)
        image = request.POST.get('visitor_image_url', None)
        company_id = request.POST.get('company', None)

        if first_name is None or last_name is None or gender is None or dob is None or phone1 is None \
                or card_id is None or company_id is None or email is None or image is None:
            messages.add_message(request, messages.WARNING, 'Required fields must not be empty')
            return redirect('add-visitor')

        company_id = eval('' + company_id)  # TODO: change eval to int
        company = Manager.objects.get(id=company_id)

        visitor = Visitor()

        visitor.first_name = first_name
        visitor.middle_name = middle_name
        visitor.last_name = last_name
        visitor.gender = gender
        visitor.date_of_birth = dob
        visitor.phone1 = int(phone1)
        if phone2 != '':
            visitor.phone2 = int(phone2)
        visitor.email = email
        visitor.card_id = card_id
        visitor.picture = image
        visitor.company_to_visit = company

        visitor.save()

        data = model_to_dict(visitor)
        pusher_client.trigger('my-channel', str(visitor.company_to_visit_id), data)

        messages.add_message(request, messages.INFO, 'Visitor has been added')
        return redirect('reception-dashboard')


@is_logged_in('reception')
def all_visitors(request):
    reception_id = request.session.get('reception_id')
    receptionist = Receptionist.objects.get(id=reception_id)
    visitors = Visitor.objects.all()

    # TODO: company_id visitor_name
    visitor = {
        'picture': None,
        'name': 'Dip',
        'phone': '1234',
        'email': 'd@d.com',
        'company_to_visit': 'Company Demo',
        'in_time': '10:10',
        'is_inside_building': True,
    }

    pusher_client.trigger('my-channel', '3', visitor)

    return render(request, 'reception/all-visitors.html', {
        'all_visitors': visitors,
        'receptionist': receptionist
    })


@is_logged_in('reception')
def visitor_details(request, visitor_id):
    reception_id = request.session.get('reception_id')
    receptionist = Receptionist.objects.get(id=reception_id)

    visitor = get_object_or_404(Visitor, id=visitor_id)
    visitor_visits = Visitor.objects.filter(email=visitor.email)\
        .values('card_id', 'company_to_visit', 'in_time', 'meet_time', 'out_time', 'is_inside_building')

    return render(request, 'reception/visitor-details.html', {
        'visitor': visitor,
        'receptionist': receptionist,
        'visitor_visits': visitor_visits,
    })
