# Generated by Django 2.0.6 on 2018-07-02 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reception', '0004_auto_20180701_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='password',
        ),
    ]
