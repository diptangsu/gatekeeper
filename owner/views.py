from django.shortcuts import render, redirect
from django.http import Http404
from .models import Owner
from django.contrib import messages


def index(request):
    # TODO: change this to index page with all login options
    return render(request, 'owner/login.html')


def login(request):
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
            try:
                Owner.objects.get(email=email)
            except Owner.DoesNotExist:
                error = 'Your email does not belong to an account'
                messages.add_message(request, messages.ERROR, error)
                return render(request, 'owner/login.html')
            else:
                error = 'You entered an incorrect password'
                messages.add_message(request, messages.ERROR, error)
                return render(request, 'owner/login.html', {'email': request.POST.get('email', None)})
    else:
        return render(request, 'owner/login.html')


def dashboard(request):
    if 'owner_id' in request.session:
        return render(request, 'owner/dashboard.html')
    else:
        messages.add_message(request, messages.WARNING, 'Please login to visit the dashboard')
        return redirect('owner-login')


def logout(request):
    if request.method == 'POST':
        del request.session['owner_id']
        return redirect('owner-login')
    else:
        raise Http404
