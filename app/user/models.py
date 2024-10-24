from typing import Iterable
from django.db import models

from django.forms.models import model_to_dict

import uuid
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from django.conf import settings
from app.settings import MEDIA_URL, STATIC_URL

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import pre_save

from user.upload import carnetdoc, asignaciondoc

# Create your models here.
def validate_file_size(archivo):
    limit = 2*1024*1024
    if archivo.size > limit:
        raise ValidationError('El tamaño del archivo no puede exceder los 2 MB')

class Persona(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    cargo = models.CharField(max_length=255, null=False, blank=False)
    celular = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f' {self.slug}-{self.nombre}-{self.apellido}-{self.celular}'
    
    def save(self, *args, **kwargs):
        self.nombre = (self.nombre).upper()
        self.apellido = (self.apellido).upper()
        self.cargo = (self.cargo).upper()
        return super(Persona, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
        db_table = 'Persona'

    def nombrecompleto(self):
        return f'{self.nombre} {self.apellido}'
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
        
class EncargadoMAE (models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, null=False, blank=False)
    carnet = models.FileField(upload_to=carnetdoc, null=False, blank=False)
    asignacion = models.FileField(upload_to=asignaciondoc, null=False, blank=False)
    correo = models.EmailField(null=False, blank=False, default="") 
    
    def __str__(self):
        return f' {self.slug}-{self.persona.nombre}-{self.persona.apellido}-{self.persona.celular}'
      
    class Meta:
        verbose_name = _('EncargadoMAE')
        verbose_name_plural = _('EncargadosMAE')
        db_table = 'EncargadoMAE'
        
    def toJSON(self):
        item = model_to_dict(self)
        return item

def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(
            '{}'.format(str(uuid.uuid4())[:4])
        )
        instance.slug = slug

pre_save.connect(set_slug, sender=EncargadoMAE)

class ResponsableP(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True, blank=True)
    correo = models.EmailField(null=False, blank=False)

    def __str__(self):
        return f' {self.slug}-{self.nombre}-{self.apellido}-{self.celular}'
    
    class Meta:
        verbose_name = _('ResponsableP')
        verbose_name_plural = _('ResponsablesP')
        db_table = 'ResponsableP'

    def toJSON(self):
        item = model_to_dict(self)
        return item

pre_save.connect(set_slug, sender=ResponsableP)

class AccountManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, password, **extra_fields):
        values = [username]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))

        for field_usuario, value in field_value_map.items():
            if not value:
                raise ValueError('Se debe establecer {}'.format(field_usuario))
        user = self.model(
              username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_revisor', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)
    
    def create_municipio(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_municipio', True)
        extra_fields.setdefault('is_revisor', False)
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El revisor debe tener is_staff=True.')
        if extra_fields.get('is_municipio') is not True:
            raise ValueError('El revisor debe tener is_municipio=True.')
        if extra_fields.get('is_revisor') is True:
            raise ValueError('El revisor debe tener is_revisor=False.')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('El revisor debe tener is_superuser=False.')
        return self._create_user(username, password, **extra_fields)

    def create_revisor(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_municipio', False)
        extra_fields.setdefault('is_revisor', True)
        extra_fields.setdefault('is_superuser', False)
        persona = Persona.objects.create()
        extra_fields.setdefault('persona', persona)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El revisor debe tener is_staff=True.')
        if extra_fields.get('is_municipio') is True:
            raise ValueError('El revisor debe tener is_municipio=False.')
        if extra_fields.get('is_revisor') is not True:
            raise ValueError('El revisor debe tener is_revisor=True.')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('El revisor debe tener is_superuser=False.')
        return Revisor.objects.create(user=self._create_user(username, password, **extra_fields))

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_municipio', False)
        extra_fields.setdefault('is_revisor', False)
        extra_fields.setdefault('is_superuser', True)
        persona = Persona.objects.create()
        extra_fields.setdefault('persona', persona)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El revisor debe tener is_staff=True.')
        if extra_fields.get('is_municipio') is True:
            raise ValueError('El revisor debe tener is_municipio=False.')
        if extra_fields.get('is_revisor') is True:
            raise ValueError('El revisor debe tener is_revisor=False.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El revisor debe tener is_superuser=True.')
        return SuperUser.objects.create(user=self._create_user(username, password, **extra_fields))

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Usuario'), max_length=255, unique=True)
    fecha_reg = models.DateField(_('Fecha Registro'), auto_now_add=True)
    is_active = models.BooleanField(_('Activo'), default=True)
    is_staff = models.BooleanField(_('Estado Staff'), default=False)
    is_municipio = models.BooleanField(_('Estado municipio'), default=False)    
    is_revisor = models.BooleanField(_('Estado municipio'), default=False)
    is_superuser = models.BooleanField(_('Estado municipio'), default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        db_table = 'User'


class Revisor(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, related_name="revisor_perfil",on_delete=models.CASCADE)
    
    def __str__(self):
        return f' {self.slug}-{self.persona.nombre}-{self.persona.apellido}-{self.persona.celular}'
    
    class Meta:
        verbose_name = _('Revisor')
        verbose_name_plural = _('Revisores')
        db_table = 'Revisor'

pre_save.connect(set_slug, sender=Revisor)

class SuperUser(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(Persona,related_name="superuser_perfil",on_delete=models.CASCADE)
    
    def __str__(self):
        return f' {self.slug}-{self.persona.nombre}-{self.persona.apellido}-{self.persona.celular}'
    
    class Meta:
        verbose_name = _('SuperUser')
        verbose_name_plural = _('SuperUsers')
        db_table = 'SuperUser'

pre_save.connect(set_slug, sender=SuperUser)

