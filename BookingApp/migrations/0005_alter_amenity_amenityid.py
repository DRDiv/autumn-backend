# Generated by Django 4.2.5 on 2023-10-23 21:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0004_alter_event_eventid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='amenityId',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
