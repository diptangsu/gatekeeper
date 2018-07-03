from django.db import models


class Scan(models.Model):
    uid = models.CharField(max_length=50, primary_key=True)
    image = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return self.uid
