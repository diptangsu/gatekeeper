from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import Scan
from manager.models import Manager
from reception.models import Visitor
from time import time
from gatekeeper.cipher import decode
from django.contrib import messages


def visitor_departed(card_id):
    try:
        visitor = Visitor.objects.get(card_id=card_id)
    except Visitor.DoesNotExist:
        pass
    else:
        visitor.is_inside_building = False
        visitor.save()


@csrf_exempt
def submit(request):
    if request.method == 'GET':
        raise Http404

    uid = request.POST.get('uid', None)
    picture = request.FILES.get('image', None)
    if uid is None and picture is None:
        raise Http404

    card_id = uid  # decode(uid)
    try:
        card = Scan.objects.get(uid=card_id)
    except Scan.DoesNotExist:
        s = Scan()
        s.uid = card_id
        s.save()
    else:
        visitor_departed(uid)
        card.delete()
        messages.add_message(request, messages.INFO, 'The visitor has departed')

    return HttpResponse(uid)


@csrf_exempt
def visitor_reached(request):
    # visitor scans the card at the door of the company he wants to visit
    if request.method == 'GET':
        raise Http404

    uid = request.POST.get('uid', None)
    company_id = request.POST.get('company_id', None)
    if uid is None or company_id is None:
        raise Http404

    card_id = uid  # decode(uid)

    try:
        company = Manager.objects.get(id=company_id)
        visitor = Visitor.objects.get(card_id=card_id)
    except Visitor.DoesNotExist or Manager.DoesNotExist:
        raise Http404
    else:
        if visitor.company_to_visit != company:
            raise Http404
        visitor.meet_time = now()
        visitor.save()
        messages.add_message(request, messages.INFO, 'The visitor has reached the building')
    return HttpResponse('0')


def get_scanned_card(request):  # used for ajax
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


def get_scanned_image(request):  # used for ajax
    if request.method == 'POST':
        data = {'image': None}
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
            data['image'] = card.image.url
            break

        return JsonResponse(data)

    else:
        raise Http404
