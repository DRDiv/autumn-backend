# Generated by Django 4.2.5 on 2023-10-23 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0005_alter_amenity_amenityid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='amenityId',
            field=models.CharField(default='0', max_length=100, primary_key=True, serialize=False),
        ),
    ]