# Generated by Django 5.1.5 on 2025-01-20 02:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0006_novedad_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosPersonales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar_origen', models.CharField(blank=True, max_length=100, null=True)),
                ('edad', models.PositiveIntegerField(blank=True, null=True)),
                ('estilo_musical_favorito', models.CharField(blank=True, max_length=100, null=True)),
                ('profesor_favorito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alumnos', to='toth.profesor')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='datos_personales', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='PreferenciasUsuario',
        ),
    ]
