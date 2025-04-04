# Generated by Django 5.1.5 on 2025-01-19 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0004_remove_profesor_usuario_profesor_nombre_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Novedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='novedades/')),
                ('video', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
