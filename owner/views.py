from django.shortcuts import render, redirect
from django.http import Http404
from .models import Owner
from django.contrib import messages


def index(request):
    # TODO: change this to index page with all login options
    return render(request, 'owner/login.html')


def login(request):
    # TODO: if logged in, redirect to 'owner/dashboard'
    if 'owner_id' in request.session:
        return redirect('owner-dashboard')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            owner = Owner.objects.get(email=email, password=password)
            request.session['owner_id'] = owner.id
            return redirect('owner-dashboard')
        except Owner.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Wrong Email / Password')
            return render(request, 'owner/login.html', {'error': 'Wrong email or password'})
    else:
        return render(request, 'owner/login.html')


def dashboard(request):
    if 'owner_id' in request.session:
        return render(request, 'owner/dashboard.html')
    else:
        messages.add_message(request, messages.WARNING, 'You need to be logged in to access this page')
        return redirect('owner-login')


def logout(request):
    if request.method == 'POST':
        del request.session['owner_id']
        return redirect('owner-login')
    else:
        raise Http404
