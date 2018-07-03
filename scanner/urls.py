from django.urls import path
from . import views

urlpatterns = [
    path('submit-card', views.submit, name='submit-card'),  # receptionist scan card
    path('get-scanned-card', views.get_scanned_card, name='get-scanned-card'),  # used for ajax
    path('get-scanned-image', views.get_scanned_image, name='get-scanned-image'),  # used for ajax
    path('visitor-reached', views.visitor_reached, name='visitor-reached'),  # manager scan card
]
