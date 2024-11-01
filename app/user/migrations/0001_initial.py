# Generated by Django 5.1.2 on 2024-10-29 15:44

import django.db.models.deletion
import user.models
import user.upload
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('cargo', models.CharField(max_length=255)),
                ('celular', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'db_table': 'Persona',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='Usuario')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Estado Staff')),
                ('is_municipio', models.BooleanField(default=False, verbose_name='Estado municipio')),
                ('is_revisor', models.BooleanField(default=False, verbose_name='Estado revisor')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Estado superuser')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'User',
            },
            managers=[
                ('objects', user.models.AccountManager()),
            ],
        ),
        migrations.CreateModel(
            name='EncargadoMAE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('carnet', models.FileField(upload_to=user.upload.carnetdoc)),
                ('asignacion', models.FileField(upload_to=user.upload.asignaciondoc)),
                ('correo', models.EmailField(default='', max_length=254)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.persona')),
            ],
            options={
                'verbose_name': 'EncargadoMAE',
                'verbose_name_plural': 'EncargadosMAE',
                'db_table': 'EncargadoMAE',
            },
        ),
        migrations.CreateModel(
            name='ResponsableP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('correo', models.EmailField(max_length=254)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.persona')),
            ],
            options={
                'verbose_name': 'ResponsableP',
                'verbose_name_plural': 'ResponsablesP',
                'db_table': 'ResponsableP',
            },
        ),
        migrations.CreateModel(
            name='Revisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('persona', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.persona')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='revisor_perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Revisor',
                'verbose_name_plural': 'Revisores',
                'db_table': 'Revisor',
            },
        ),
        migrations.CreateModel(
            name='SuperUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='superuser_persona', to='user.persona')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='superuser_perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SuperUser',
                'verbose_name_plural': 'SuperUsers',
                'db_table': 'SuperUser',
            },
        ),
    ]
