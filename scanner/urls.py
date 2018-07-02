from django.urls import path
from . import views

urlpatterns = [
    path('submit-card', views.submit, name='submit-card'),  # receptionist scan card
    path('issue-card', views.scan_card, name='issue-card'),  # used for ajax
    path('visitor-reached', views.visitor_reached, name='visitor-reached'),  # manager scan card
]
