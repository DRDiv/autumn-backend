# Generated by Django 4.2.5 on 2023-10-25 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0010_alter_booking_bookingid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='individuals',
        ),
        migrations.AddField(
            model_name='booking',
            name='individuals',
            field=models.ManyToManyField(blank=True, to='BookingApp.user'),
        ),
    ]
