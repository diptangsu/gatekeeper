from django.shortcuts import HttpResponse
from .models import Scan
from reception.models import Visitor


def submit(request, uid):
    user_id = uid  # decode(uid)
    try:
        card = Scan.objects.get(uid=user_id)
    except Scan.DoesNotExist:
        s = Scan()
        s.uid = user_id
        s.save()
    else:
        # Visitor.objects.get()
        # TODO: add out time for Visitor
        card.delete()
    return HttpResponse(uid)
