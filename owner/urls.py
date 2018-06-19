from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='owner-dashboard'),
    path('login', views.login, name='owner-login'),
    path('logout', views.logout, name='owner-logout'),
]
