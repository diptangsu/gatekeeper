from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='manager-dashboard'),
    path('login', views.login, name='manager-login'),
    path('logout', views.logout, name='manager-logout'),
    path('all-visitors', views.all_visitors, name='manager-all-visitors'),
    path('add-employees', views.add_employees, name='manager-add-employees'),
    path('manager-upload-csv', views.manager_upload_csv, name='manager-upload-csv')
]
