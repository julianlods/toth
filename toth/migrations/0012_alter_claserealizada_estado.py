# Generated by Django 5.1.5 on 2025-01-21 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0011_remove_claserealizada_realizada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claserealizada',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente de realizarse'), ('realizada', 'Realizada')], default='pendiente', max_length=20),
        ),
    ]
