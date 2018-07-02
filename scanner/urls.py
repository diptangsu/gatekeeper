from django.urls import path
from . import views

urlpatterns = [
    path('submit-card/<int:uid>', views.submit, name='submit-card'),
    path('issue-card', views.scan_card, name='issue-card'),
    path('get-scanned-card', views.scan_card, name='get-scanned-card'),
]
