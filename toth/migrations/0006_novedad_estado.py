# Generated by Django 5.1.5 on 2025-01-19 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0005_novedad'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedad',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
