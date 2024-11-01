# Generated by Django 5.1.2 on 2024-10-29 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatosProyectoBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('n_comunidades', models.IntegerField()),
                ('comunidades', models.TextField()),
                ('tipologia_proy', models.BooleanField()),
                ('periodo_ejecu', models.IntegerField(choices=[('3', '3'), ('2', '2'), ('1', '1')])),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'DatosProyectoBase',
                'verbose_name_plural': 'DatosProyectosBase',
                'db_table': 'DatosProyectoBase',
            },
        ),
    ]
