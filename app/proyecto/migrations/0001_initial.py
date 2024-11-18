# Generated by Django 5.1.2 on 2024-11-15 07:09

import proyecto.upload
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('hombre_directo', models.IntegerField()),
                ('mujer_directo', models.IntegerField()),
                ('hombre_indirecto', models.IntegerField()),
                ('mujer_indirecto', models.IntegerField()),
                ('familia', models.IntegerField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Beneficiario',
                'verbose_name_plural': 'Beneficiarios',
                'db_table': 'Beneficiario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Conclusion_recomendacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('conclusion', models.TextField(blank=True, null=True)),
                ('recomendacion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Conclusion_recomendacion',
                'verbose_name_plural': 'Conclusiones_recomendaciones',
                'db_table': 'Conclusion_recomendacion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DatosProyectoBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('n_comunidades', models.IntegerField()),
                ('comunidades', models.TextField()),
                ('tipologia_proy', models.BooleanField()),
                ('periodo_ejecu', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)])),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('solicitud_financ', models.BooleanField(default=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'DatosProyectoBase',
                'verbose_name_plural': 'DatosProyectosBase',
                'db_table': 'DatosProyectoBase',
            },
        ),
        migrations.CreateModel(
            name='Declaracion_jurada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
                ('declaracion', models.FileField(upload_to=proyecto.upload.docDeclaracionjurada)),
                ('itcp', models.FileField(upload_to=proyecto.upload.docDeclaracionjurada)),
                ('carta', models.FileField(upload_to=proyecto.upload.docDeclaracionjurada)),
                ('consultoria', models.FileField(upload_to=proyecto.upload.docDeclaracionjurada)),
            ],
            options={
                'verbose_name': 'Declaracion_jurada',
                'verbose_name_plural': 'Declaraciones_juradas',
                'db_table': 'Declaracion_jurada',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Derecho_propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('descripcion', models.TextField()),
                ('si_registro', models.FileField(blank=True, null=True, upload_to=proyecto.upload.docDerechoPropietario)),
                ('no_registro', models.TextField(blank=True, null=True)),
                ('zone', models.IntegerField()),
                ('easting', models.FloatField()),
                ('northing', models.FloatField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Derecho_propietario',
                'verbose_name_plural': 'Derechos_propietarios',
                'db_table': 'Derecho_propietario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Detalle_POA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Detalle_POA',
                'verbose_name_plural': 'Detalles_POA',
                'db_table': 'Detalle_POA',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Idea_Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('antecedente', models.TextField()),
                ('diagnostico', models.TextField()),
                ('planteamiento_problema', models.TextField()),
                ('actores_involucrados', models.TextField()),
                ('alternativa_1', models.TextField()),
                ('alternativa_2', models.TextField()),
                ('elige_alternativa', models.IntegerField(choices=[(1, 1), (2, 2)])),
                ('justificacion_alter', models.TextField()),
                ('objetivo_general', models.TextField()),
                ('beneficios_alter', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Idea_Proyecto',
                'verbose_name_plural': 'Ideas_Proyectos',
                'db_table': 'Idea_Proyecto',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Impacto_ambiental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('bosque_nivel', models.CharField(choices=[('Ninguno', 'Ninguno'), ('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')], max_length=255)),
                ('bosque_tempo', models.CharField(choices=[('Transitorio', 'Transitorio'), ('Permanente', 'Permanente')], max_length=255)),
                ('suelo_nivel', models.CharField(choices=[('Ninguno', 'Ninguno'), ('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')], max_length=255)),
                ('suelo_tempo', models.CharField(choices=[('Transitorio', 'Transitorio'), ('Permanente', 'Permanente')], max_length=255)),
                ('agua_nivel', models.CharField(choices=[('Ninguno', 'Ninguno'), ('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')], max_length=255)),
                ('agua_tempo', models.CharField(choices=[('Transitorio', 'Transitorio'), ('Permanente', 'Permanente')], max_length=255)),
                ('aire_nivel', models.CharField(choices=[('Ninguno', 'Ninguno'), ('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')], max_length=255)),
                ('aire_tempo', models.CharField(choices=[('Transitorio', 'Transitorio'), ('Permanente', 'Permanente')], max_length=255)),
                ('biodiversidad_nivel', models.CharField(choices=[('Ninguno', 'Ninguno'), ('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')], max_length=255)),
                ('biodiversidad_tempo', models.CharField(choices=[('Transitorio', 'Transitorio'), ('Permanente', 'Permanente')], max_length=255)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Impacto_ambiental',
                'verbose_name_plural': 'Impactos_ambientales',
                'db_table': 'Impacto_ambiental',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Justificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('justificacion1', models.BooleanField()),
                ('justificacion2', models.BooleanField()),
                ('justificacion3', models.BooleanField()),
                ('justificacion4', models.BooleanField()),
                ('justificacion5', models.BooleanField()),
                ('justificacion6', models.BooleanField()),
                ('justificacion7', models.BooleanField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Justificacion',
                'verbose_name_plural': 'Justificaciones',
                'db_table': 'Justificacion',
            },
        ),
        migrations.CreateModel(
            name='Modelo_Acta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('comunidades', models.CharField()),
                ('si_acta', models.FileField(blank=True, null=True, upload_to=proyecto.upload.docModeloActa)),
                ('no_acta', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Modelo_Acta',
                'verbose_name_plural': 'Modelo_Actas',
                'db_table': 'Modelo_Acta',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Objetivo_especifico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('objetivo', models.TextField()),
                ('componente', models.TextField()),
                ('linea_base', models.TextField()),
                ('indicador', models.TextField()),
                ('meta', models.TextField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Objetivo_especifico',
                'verbose_name_plural': 'Objetivos_especificos',
                'db_table': 'Objetivo_especifico',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PresupuestoReferencial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
                ('elab_sol', models.DecimalField(decimal_places=2, max_digits=10)),
                ('elab_fona', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('elab_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('elab_fona_p', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('elab_sol_p', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('elab_total_p', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ejec_fona', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ejec_sol', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ejec_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ejec_fona_p', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ejec_sol_p', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ejec_total_p', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name': 'PresupuestoReferencial',
                'verbose_name_plural': 'PresupuestosReferenciales',
                'db_table': 'PresupuestoReferencial',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('fechaenvio', models.DateTimeField(auto_now_add=True)),
                ('aceptar', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Proyectos',
                'db_table': 'Proyecto',
            },
        ),
        migrations.CreateModel(
            name='Riesgo_desastre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('riesgo', models.CharField(choices=[('Granizadas', 'Granizadas'), ('Heladas', 'Heladas'), ('Sequias', 'Sequias'), ('Inundaciones', 'Inundaciones'), ('Derrumbes', 'Derrumbes'), ('Incendios forestales', 'Incendios forestales'), ('Desertificacion', 'Desertificacion'), ('Erosion de suelos y/o suelos degradados', 'Erosion de suelos y/o suelos degradados'), ('Vientos fuertes', 'Vientos fuertes'), ('Deslizamientos', 'Deslizamientos'), ('Plagas y enfermedades', 'Plagas y enfermedades'), ('Sanitarias', 'Sanitarias')])),
                ('nivel', models.CharField(choices=[('Ninguno', 'Ninguno'), ('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')])),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Riesgo_desastre',
                'verbose_name_plural': 'Riesgos_desastres',
                'db_table': 'Riesgo_desastre',
                'managed': True,
            },
        ),
    ]