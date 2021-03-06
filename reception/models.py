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
    gender = models.CharField(max_length=15, default='Flying Fuck')
    phone1 = models.CharField(max_length=14, default=None)
    phone2 = models.CharField(max_length=14, default=None, blank=True, null=True)
    email = models.EmailField(max_length=255, default=None)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(default="Hogwarts")
    pin_code = models.IntegerField(default=0)
    picture = models.CharField(max_length=255, default=None, blank=True)
    company_to_visit = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    card_id = models.CharField(max_length=255, default=None, null=True)
    in_time = models.DateTimeField(auto_now_add=True)
    meet_time = models.DateTimeField(default=None, blank=True, null=True)
    out_time = models.DateTimeField(auto_now=True)
    is_inside_building = models.BooleanField(default=True)

    def __str__(self):
        return f'({self.id}) {self.first_name} {self.last_name} -> ' \
               f'{self.company_to_visit.company_name} | {self.in_time.date()}'

    def name(self):
        full_name = self.first_name
        if self.middle_name is not None:
            full_name += ' ' + self.middle_name
        full_name += ' ' + self.last_name
        return full_name
