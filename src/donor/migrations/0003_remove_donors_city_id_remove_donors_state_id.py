# Generated by Django 4.2.11 on 2024-04-15 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0002_donors_city_id_donors_state_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donors',
            name='city_id',
        ),
        migrations.RemoveField(
            model_name='donors',
            name='state_id',
        ),
    ]