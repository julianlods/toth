# Generated by Django 5.1.5 on 2025-01-26 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0017_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='clase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='toth.clase'),
        ),
    ]
