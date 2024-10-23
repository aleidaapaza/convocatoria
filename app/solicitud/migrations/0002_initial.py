# Generated by Django 5.1.2 on 2024-10-23 02:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('solicitud', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postulacion',
            name='mae',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encargado_mae_p', to='user.encargadomae'),
        ),
        migrations.AddField(
            model_name='postulacion',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Datos_base_proyecto', to='solicitud.municipios'),
        ),
        migrations.AddField(
            model_name='postulacion',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_p', to='user.responsablep'),
        ),
    ]
