from django.shortcuts import HttpResponse
from .models import Scan


def submit(request, uid):
    user_id = uid
    if user_id != 0:
        s = Scan()
        s.uid = user_id
        s.save()
    return HttpResponse(uid)
