# Generated by Django 5.1.5 on 2025-01-20 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0008_rename_video_contenido_video_url_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoriacontenido',
            options={'verbose_name': 'Categoria contenido', 'verbose_name_plural': 'Categoria contenidos'},
        ),
    ]
