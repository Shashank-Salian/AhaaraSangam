# Generated by Django 4.2.11 on 2024-04-18 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0005_remove_donors_city_iso2'),
    ]

    operations = [
        migrations.AddField(
            model_name='donations',
            name='items',
            field=models.CharField(default='', max_length=500),
        ),
    ]
