from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:uid>', views.submit, name='submit'),
]
