from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='manager-dashboard'),
    path('login', views.login, name='manager-login'),
    path('logout', views.logout, name='manager-logout'),
]
