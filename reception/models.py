from django.db import models
from manager.models import Manager


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
    email = models.EmailField(max_length=255, default='d@d.com')
    password = models.CharField(max_length=255, default='password')
    date_of_birth = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='img/', blank=True, null=True)
    company_to_visit = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
