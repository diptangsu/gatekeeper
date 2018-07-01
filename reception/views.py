from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib import messages
from time import time
import json
from gatekeeper.decorators import is_logged_in
from collections import namedtuple
from django.utils.timezone import now

from scanner.models import Scan
from .models import Receptionist, Visitor
from manager.models import Manager


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
    VisitorInfo = namedtuple('VisitorInfo', 'company visitors percentage')
    all_visitors = []
    for manager in managers:
        v = Visitor.objects.filter(company_to_visit=manager)  # get all visitors for one company/manager
        vp = round(100. * len(v) / total_visitors if total_visitors != 0 else 1)
        all_visitors.append(VisitorInfo(company=manager.company_name, visitors=v, percentage=vp))

    all_visitors = sorted(all_visitors, key=lambda x: x.percentage, reverse=True)

    return render(request, 'reception/dashboard.html',
                  {
                      'receptionist': receptionist,
                      'all_visitors': all_visitors,
                      'total_visitors': total_visitors,
                      'total_companies': len(managers)
                  })


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
        companies = Manager.objects.all()
        return render(request, 'reception/addVisitor.html', {'companies': companies})
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
        company_id = request.POST.get('company', None)

        data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'gender': gender,
            'dob': dob,
            'phone1': phone1,
            'phone2': phone2,
            'email': email,
            'card_id': card_id,
            'company_id': company_id
        }

        if first_name is None or last_name is None or gender is None or dob is None or phone1 is None \
                or card_id is None or company_id is None or email is None:
            messages.add_message(request, messages.WARNING, 'Required fields must not be empty')
            # return HttpResponse(json.dumps(data), content_type="application/json")
            return redirect('add-visitor')

        company_id = eval('' + company_id)
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
        visitor.company_to_visit = company
        visitor.is_inside_building = True

        visitor.save()

        messages.add_message(request, messages.INFO, 'Visitor has been added')
        return redirect('reception-dashboard')


def visitor_reached(request):
    # visitor scans the card at the door of the company he wants to visit
    card_id = 0
    visitor = Visitor.objects.get(card_id=card_id)
    visitor.meet_time = now()
    visitor.save()


def visitor_departed(request):
    card_id = 0
    visitor = Visitor.objects.get(card_id=card_id)
    visitor.is_inside_building = False
    visitor.save()


def scan_card(request):
    if request.method == 'POST':
        data = {'uid': None}
        start_scan = time()
        while True:
            end_scan = time()
            if end_scan - start_scan > 3:
                break
            cards = Scan.objects.all()
            no_of_cards = len(cards)
            if no_of_cards == 0:
                continue
            card = cards[no_of_cards - 1]
            data['uid'] = card.uid
            break

        return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        raise Http404
