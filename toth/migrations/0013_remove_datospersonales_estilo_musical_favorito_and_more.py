# Generated by Django 5.1.5 on 2025-01-22 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0012_alter_claserealizada_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datospersonales',
            name='estilo_musical_favorito',
        ),
        migrations.AddField(
            model_name='datospersonales',
            name='estilos_musicales_favoritos',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Estilos musicales favoritos'),
        ),
    ]
