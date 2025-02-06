# Generated by Django 5.1.2 on 2025-02-04 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0020_objetivoespecificoejec_objetivogeneralejec_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objetivoespecificoejec',
            name='nro',
        ),
        migrations.AlterField(
            model_name='objetivogeneralejec',
            name='hectareas',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='objetivogeneralejec',
            name='tipo_hectareas',
            field=models.CharField(choices=[('Forestacion', 'Forestacion'), ('Reforestacion', 'Reforestacion'), ('Manejo sustentable de bosque', 'Manejo sustentable de bosque'), ('Forestacion y Reforestacion', 'Forestacion y Reforestacion'), ('Forestacion y Manejo sustentable de bosque', 'Forestacion y Manejo sustentable de bosque'), ('Reforestacion y Manejo sustentable de bosque', 'Reforestacion y Manejo sustentable de bosque'), ('Forestacion, Reforestacion y Manejo sustentable de bosque', 'Forestacion, Reforestacion y Manejo sustentable de bosque')], default=''),
        ),
    ]
