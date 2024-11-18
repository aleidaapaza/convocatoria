# Generated by Django 5.1.2 on 2024-11-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0003_postulacion_convocatoria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipios',
            name='departamento',
            field=models.CharField(choices=[('TARIJA', 'TARIJA'), ('ORURO', 'ORURO'), ('PANDO', 'PANDO'), ('COCHABAMBA', 'COCHABAMBA'), ('LA PAZ', 'LA PAZ'), ('CHUQUISACA', 'CHUQUISACA'), ('POTOSI', 'POTOSI'), ('BENI', 'BENI'), ('SANTA CRUZ', 'SANTA CRUZ')], max_length=30),
        ),
        migrations.AlterField(
            model_name='municipios',
            name='estado',
            field=models.CharField(choices=[('NINGUNO', 'NINGUNO'), ('RECHAZADO', 'RECHAZADO'), ('APROBADO', 'APROBADO'), ('SOLICITUD', 'SOLICITUD')], max_length=255),
        ),
    ]
