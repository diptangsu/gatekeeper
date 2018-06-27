from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import Receptionist, Visitor
from manager.models import Manager
from scanner.models import Scan
from django.contrib import messages
from time import time
import json
from gatekeeper.decorators import is_logged_in


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
                messages.add_message(request, messages.INFO, error)
                return render(request, 'reception/login.html', {'email': request.POST.get('email', None)})
    else:
        return render(request, 'reception/login.html')


@is_logged_in('reception')
def dashboard(request):
    receptionist = Receptionist.objects.get(id=request.session.get('reception_id'))
    return render(request, 'reception/dashboard.html', {'receptionist': receptionist})


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
        visitor = Visitor()
        # TODO: save visitor data

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
            card.delete()
            break

        return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        raise Http404
