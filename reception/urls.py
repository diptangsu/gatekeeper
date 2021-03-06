from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='reception-dashboard'),
    path('login', views.login, name='reception-login'),
    path('logout', views.logout, name='reception-logout'),
    path('add-visitor', views.add_visitor, name='add-visitor'),
    path('all-visitors', views.all_visitors, name='reception-all-visitors'),
    path('visitor/<int:visitor_id>', views.visitor_details, name='visitor-details'),
]
