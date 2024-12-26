# Generated by Django 5.1.2 on 2024-11-27 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0009_alter_municipios_departamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipios',
            name='departamento',
            field=models.CharField(choices=[('CHUQUISACA', 'CHUQUISACA'), ('ORURO', 'ORURO'), ('COCHABAMBA', 'COCHABAMBA'), ('PANDO', 'PANDO'), ('SANTA CRUZ', 'SANTA CRUZ'), ('POTOSI', 'POTOSI'), ('BENI', 'BENI'), ('LA PAZ', 'LA PAZ'), ('TARIJA', 'TARIJA')], max_length=30),
        ),
        migrations.AlterField(
            model_name='municipios',
            name='estado',
            field=models.CharField(choices=[('RECHAZADO', 'RECHAZADO'), ('APROBADO', 'APROBADO'), ('SOLICITUD', 'SOLICITUD'), ('NINGUNO', 'NINGUNO')], max_length=255),
        ),
    ]