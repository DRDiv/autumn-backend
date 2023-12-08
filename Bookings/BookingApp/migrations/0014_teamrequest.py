# Generated by Django 4.2.5 on 2023-12-08 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0013_booking_dateslot_booking_timestart'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookingApp.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookingApp.user')),
            ],
        ),
    ]
