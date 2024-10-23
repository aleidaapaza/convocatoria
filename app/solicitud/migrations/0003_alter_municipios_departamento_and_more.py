# Generated by Django 5.1.2 on 2024-10-23 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipios',
            name='departamento',
            field=models.CharField(choices=[('ORURO ', 'ORURO'), ('LA PAZ', 'LA PAZ'), ('TARIJA', 'TARIJA'), ('SANTA CRUZ', 'SANTA CRUZ'), ('PANDO', 'PANDO'), ('CHUQUISACA', 'CHUQUISACA'), ('BENI', 'BENI'), ('POTOSI', 'POTOSI'), ('COCHABAMBA', 'COCHABAMBA')], max_length=30),
        ),
        migrations.AlterField(
            model_name='municipios',
            name='entidad_territorial',
            field=models.CharField(choices=[('GOBIERNO AUTÓNOMO MUNICIPAL ', 'GOBIERNOS AUTÓNOMOS MUNICIPALES'), ('GOBIERNO AUTÓNOMO REGIONAL ', 'GOBIERNOS AUTÓNOMOS REGIONAL'), ('GOBIERNO AUTÓNOMO INDIGENA ORIGINARIO CAMPESINO ', 'GOBIERNO AUTÓNOMO INDIGENA ORIGINARIO CAMPESINO'), ('GOBIERNO AUTÓNOMO DEPARTAMENTAL ', 'GOBIERNOS AUTÓNOMOS DEPARTAMENTALES')], max_length=100),
        ),
        migrations.AlterField(
            model_name='municipios',
            name='estado',
            field=models.CharField(choices=[('NINGUNO', 'NINGUNO'), ('SOLICITUD', 'SOLICITUD'), ('APROBADO', 'APROBADO')], max_length=255),
        ),
    ]