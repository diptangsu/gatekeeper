from django.shortcuts import render, redirect
from django.http import Http404
from .models import Manager
from django.contrib import messages


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
                messages.add_message(request, messages.INFO, error)
                return render(request, 'manager/login.html')
            else:
                error = 'You entered an incorrect password'
                messages.add_message(request, messages.INFO, error)
                return render(request, 'manager/login.html', {'email': request.POST.get('email', None)})
    else:
        return render(request, 'manager/login.html')


def dashboard(request):
    if 'manager_id' in request.session:
        return render(request, 'manager/dashboard.html')
    else:
        messages.add_message(request, messages.WARNING, 'Please login to visit the dashboard')
        return redirect('manager-login')


def logout(request):
    if request.method == 'POST':
        del request.session['manager_id']
        return redirect('manager-login')
    else:
        raise Http404
