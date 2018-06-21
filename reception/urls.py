from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='reception-dashboard'),
    path('login', views.login, name='reception-login'),
    path('logout', views.logout, name='reception-logout'),
    path('add-visitor', views.add_visitor, name='add-visitor'),
    path('scan-card', views.scan_card, name='scan-card'),
]
