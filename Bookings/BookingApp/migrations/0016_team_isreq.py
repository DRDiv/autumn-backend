# Generated by Django 4.2.5 on 2023-12-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0015_delete_teamrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='isReq',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
