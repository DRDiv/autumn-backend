# Generated by Django 4.2.5 on 2023-10-21 12:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('amenityId', models.CharField(default='0', max_length=100, primary_key=True, serialize=False)),
                ('amenityName', models.CharField(max_length=100)),
                ('amenityPicture', models.ImageField(blank=True, upload_to='images/')),
                ('recurrance', models.CharField(choices=[('D', 'daily'), ('W', 'weekly'), ('M', 'monthly'), ('Y', 'yearly'), ('O', 'onetime')], default='D')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eventId', models.CharField(default='0', max_length=100, primary_key=True, serialize=False)),
                ('eventName', models.CharField(max_length=100)),
                ('eventPicture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('eventDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('minTeamSize', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('maxTeamSize', models.IntegerField(default=1)),
                ('payment', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.CharField(default='0', max_length=100, primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=100)),
                ('data', models.JSONField(default=dict)),
                ('penalties', models.IntegerField(default=0)),
                ('ammenityProvider', models.BooleanField(default=False)),
                ('userSession', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamId', models.CharField(default='0', max_length=100, primary_key=True, serialize=False)),
                ('teamName', models.CharField(max_length=100)),
                ('isAdmin', models.JSONField(blank=True, default=dict)),
                ('bookedEvents', models.ManyToManyField(blank=True, to='BookingApp.event')),
                ('users', models.ManyToManyField(to='BookingApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('requestId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timeRequest', models.DateTimeField(default=django.utils.timezone.now)),
                ('capacity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('payment', models.ImageField(null=True, upload_to='images/')),
                ('dateSlot', models.DateField(blank=True, null=True)),
                ('timeStart', models.TimeField(blank=True, null=True)),
                ('amenity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.amenity')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.event')),
                ('individuals', models.ManyToManyField(blank=True, to='BookingApp.user')),
                ('teamId', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.team')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='userProvider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.user'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('bookingId', models.CharField(default='0', max_length=100, primary_key=True, serialize=False)),
                ('timeRequest', models.DateTimeField(default=django.utils.timezone.now)),
                ('capacity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('verified', models.BooleanField(default=False)),
                ('amenity', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.amenity')),
                ('event', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.event')),
                ('individuals', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.user')),
                ('teamId', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.team')),
            ],
        ),
        migrations.CreateModel(
            name='AmenitySlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenityDate', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('ammenitySlotStart', models.TimeField(default=django.utils.timezone.now)),
                ('ammenitySlotEnd', models.TimeField(default=django.utils.timezone.now)),
                ('capacity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookingApp.amenity')),
            ],
        ),
        migrations.AddField(
            model_name='amenity',
            name='userProvider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingApp.user'),
        ),
    ]
