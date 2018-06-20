from django.shortcuts import render, redirect
from django.http import Http404
from .models import Receptionist
from django.contrib import messages


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
