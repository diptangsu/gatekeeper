from django.shortcuts import render


def index(request):
    return render(request, 'owner/index.html')


def login(request):
    pass
