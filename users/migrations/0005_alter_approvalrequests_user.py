# Generated by Django 4.2.1 on 2023-06-13 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalrequests',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
