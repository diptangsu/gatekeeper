from django.shortcuts import render


def index(request):
    return render(request, 'owner/login.html')


def login(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'owner/login.html')
