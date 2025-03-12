# Generated by Django 5.1.5 on 2025-03-12 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toth', '0022_pago_comprobante_alter_pago_metodo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('informado', 'Informado'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], default='pendiente', max_length=20),
        ),
    ]
