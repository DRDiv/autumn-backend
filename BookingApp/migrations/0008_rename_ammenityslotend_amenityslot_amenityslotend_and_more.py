# Generated by Django 4.2.5 on 2023-10-23 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0007_alter_amenity_amenityid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amenityslot',
            old_name='ammenitySlotEnd',
            new_name='amenitySlotEnd',
        ),
        migrations.RenameField(
            model_name='amenityslot',
            old_name='ammenitySlotStart',
            new_name='amenitySlotStart',
        ),
    ]
