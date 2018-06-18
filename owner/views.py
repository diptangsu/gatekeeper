from django.shortcuts import render


def index(request):
    # TODO: change this to index page with all login options
    return render(request, 'owner/login.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'owner/login.html')
    else:
        pass
