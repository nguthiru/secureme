# Generated by Django 4.2.1 on 2023-07-05 11:21

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
