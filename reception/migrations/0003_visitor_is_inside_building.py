# Generated by Django 2.0.6 on 2018-07-01 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reception', '0002_visitor_meet_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='is_inside_building',
            field=models.BooleanField(default=False),
        ),
    ]
