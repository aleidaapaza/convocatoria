from django.db import models

import uuid
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from django.conf import settings
from app.settings import MEDIA_URL, STATIC_URL

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import pre_save, post_save

from user.upload import carnetdoc, asignaciondoc

# Create your models here.
def validate_file_size(archivo):
    limit = 2*1024*1024
    if archivo.size > limit:
        raise ValidationError('El tamaño del archivo no puede exceder los 2 MB')

class EncargadoMAE (models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    carnet = models.FileField(upload_to=carnetdoc, null=False, blank=False)
    cargo = models.CharField(max_length=255, null=False, blank=False)
    asignacion = models.FileField(upload_to=asignaciondoc, null=False, blank=False)
    celular = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f' {self.slug}-{self.nombre}-{self.apellido}-{self.celular}'
    
    class Meta:
        verbose_name = _('EncargadoMAE')
        verbose_name_plural = _('EncargadosMAE')
        db_table = 'EncargadoMAE'

def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(
            '{}'.format(str(uuid.uuid4())[:4])
        )
        instance.slug = slug

pre_save.connect(set_slug, sender=EncargadoMAE)


