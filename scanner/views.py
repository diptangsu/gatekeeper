from django.shortcuts import HttpResponse
from .models import Scan
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
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
