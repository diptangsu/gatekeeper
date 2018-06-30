from django.db import models
from manager.models import Manager
from datetime import datetime


class Receptionist(models.Model):
    first_name = models.CharField(max_length=255, default='John')
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, default='Doe')
    email = models.EmailField(max_length=255, default='d@d.com')
    password = models.CharField(max_length=255, default='password')
    date_of_birth = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Visitor(models.Model):
    first_name = models.CharField(max_length=255, default='John')
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, default='Doe')
    gender = models.CharField(max_length=15, default='Flying Fuck')
    phone1 = models.IntegerField(default=0)
    phone2 = models.IntegerField(default=0)
    email = models.EmailField(max_length=255, default=None)
    password = models.CharField(max_length=255, default='password')
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(default="Hogwarts")
    pin_code = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='img/', blank=True, null=True)
    company_to_visit = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    card_id = models.CharField(max_length=255, default=None, null=True)
    # in_time = models.TimeField(auto_now_add=True)
    # out_time = models.TimeField(auto_now_add=True)
    # TODO: add these fields to Visitor

    def __str__(self):
        return f'{self.first_name} {self.last_name} -> {self.company_to_visit.company_name}'
