from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import Scan
from reception.models import Visitor
from time import time


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
        visitor_departed(uid)
        card.delete()
    return HttpResponse(uid)


def visitor_departed(card_id):
    visitor = Visitor.objects.get(card_id=card_id)
    visitor.is_inside_building = False
    visitor.save()


@csrf_exempt
def visitor_reached(request):
    # visitor scans the card at the door of the company he wants to visit
    card_id = 0
    visitor = Visitor.objects.get(card_id=card_id)
    visitor.meet_time = now()
    visitor.save()


def scan_card(request):  # used for ajax
    if request.method == 'POST':
        data = {'uid': None}
        start_scan = time()
        while True:
            end_scan = time()
            if end_scan - start_scan > 3:
                break
            cards = Scan.objects.all()
            no_of_cards = len(cards)
            if no_of_cards == 0:
                continue
            card = cards[no_of_cards - 1]
            data['uid'] = card.uid
            break

        return JsonResponse(data)

    else:
        raise Http404
