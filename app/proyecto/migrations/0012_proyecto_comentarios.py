# Generated by Django 5.1.2 on 2024-12-02 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0011_proyecto_fecha_actualizacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='comentarios',
            field=models.TextField(blank=True, null=True),
        ),
    ]