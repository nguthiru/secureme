# Generated by Django 4.2.1 on 2023-06-13 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_station_approvalrequests_customuser_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='station',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.station'),
        ),
    ]
