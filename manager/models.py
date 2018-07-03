from django.db import models


class Manager(models.Model):
    company_name = models.CharField(max_length=255, default='NA')
    first_name = models.CharField(max_length=255, default='John')
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, default='Doe')
    email = models.EmailField(max_length=255, default='d@d.com')
    password = models.CharField(max_length=255, default='password')
    date_of_birth = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return f'({self.id}) {self.first_name} {self.last_name} | {self.company_name}'

