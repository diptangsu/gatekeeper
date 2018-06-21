from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import Receptionist
from scanner.models import Scan
from django.contrib import messages
from time import time
import json


def login(request):
    if 'receptionist_id' in request.session:
        return redirect('reception-dashboard')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            receptionist = Receptionist.objects.get(email=email, password=password)
            request.session['receptionist_id'] = receptionist.id
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


def dashboard(request):
    if 'receptionist_id' in request.session:
        receptionist = Receptionist.objects.get(id=request.session.get('receptionist_id'))
        return render(request, 'reception/dashboard.html', {'receptionist': receptionist})
    else:
        messages.add_message(request, messages.WARNING, 'Please login to visit the dashboard')
        return redirect('reception-login')


def logout(request):
    if request.method == 'POST':
        del request.session['receptionist_id']
        return redirect('reception-login')
    else:
        raise Http404


def add_visitor(request):
    if 'receptionist_id' not in request.session:
        messages.add_message(request, messages.WARNING, 'Please login to add a new visitor')
        return redirect('reception-login')
    if request.method == 'GET':
        return render(request, 'reception/addVisitor.html')
    else:
        pass


def get_card_id(request):  # TODO: add visitor id to session instead of using POST
    if 'receptionist_id' not in request.session:
        messages.add_message(request, messages.WARNING, 'Please login to add a new visitor')
        return redirect('reception-login')
    if request.method == 'POST':  # TODO: change to GET
        messages.add_message(request, messages.WARNING, 'Visitor details must be entered before a card can be issued')
        return redirect('add-visitor')
    else:  # TODO: POST visitor data to this url
        scanned = False
        card = None
        start_scan = time()
        while True:
            end_scan = time()
            if end_scan - start_scan > 2:
                break
            cards = Scan.objects.all()
            no_of_cards = len(cards)
            if no_of_cards == 0:
                continue
            card = cards[no_of_cards - 1]
            card.delete()
            scanned = True
            break
        if scanned:  # TODO: save visitor object from here and redirect to dashboard
            return HttpResponse(card.uid)
        else:  # TODO: return to scan page with error toast saying scan timeout
            return render(request, 'reception/scanCard.html')


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
