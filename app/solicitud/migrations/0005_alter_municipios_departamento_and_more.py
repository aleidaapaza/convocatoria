# Generated by Django 5.1.2 on 2025-02-09 04:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0004_alter_municipios_departamento_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipios',
            name='departamento',
            field=models.CharField(choices=[('BENI', 'BENI'), ('PANDO', 'PANDO'), ('COCHABAMBA', 'COCHABAMBA'), ('POTOSI', 'POTOSI'), ('ORURO', 'ORURO'), ('TARIJA', 'TARIJA'), ('CHUQUISACA', 'CHUQUISACA'), ('LA PAZ', 'LA PAZ'), ('SANTA CRUZ', 'SANTA CRUZ')], max_length=30),
        ),
        migrations.AlterField(
            model_name='municipios',
            name='entidad_territorial',
            field=models.CharField(choices=[('GOBIERNO AUTÓNOMO INDIGENA ORIGINARIO CAMPESINO', 'GOBIERNO AUTÓNOMO INDIGENA ORIGINARIO CAMPESINO'), ('GOBIERNO AUTÓNOMO DEPARTAMENTAL', 'GOBIERNOS AUTÓNOMOS DEPARTAMENTALES'), ('GOBIERNO AUTÓNOMO REGIONAL', 'GOBIERNOS AUTÓNOMOS REGIONAL'), ('GOBIERNO AUTÓNOMO MUNICIPAL', 'GOBIERNOS AUTÓNOMOS MUNICIPALES')], max_length=100),
        ),
        migrations.AlterField(
            model_name='municipios',
            name='estado',
            field=models.CharField(choices=[('SOLICITUD', 'SOLICITUD'), ('RECHAZADO', 'RECHAZADO'), ('NINGUNO', 'NINGUNO'), ('APROBADO', 'APROBADO')], max_length=255),
        ),
        migrations.AlterField(
            model_name='postulacion',
            name='creador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
