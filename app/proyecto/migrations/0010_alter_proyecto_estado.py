# Generated by Django 5.1.2 on 2024-11-28 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0009_proyecto_revisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(choices=[('CON OBSERVACION', 'CON OBSERVACION'), ('APROBADO', 'APROBADO')], default='SIN REVISAR', max_length=50),
        ),
    ]
