# Generated by Django 5.2.1 on 2025-07-07 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0015_busroute_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatbooking',
            name='busroute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='busapp.busroute'),
        ),
    ]
