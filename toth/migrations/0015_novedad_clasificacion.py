# Generated by Django 5.1.5 on 2025-01-23 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0014_datospersonales_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedad',
            name='clasificacion',
            field=models.CharField(choices=[('general', 'General'), ('sos_vos', 'Sos vos')], default='general', max_length=10, verbose_name='Clasificación'),
        ),
    ]
