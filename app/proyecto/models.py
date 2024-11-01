from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save

from proyecto.choices import periodo_ejecucion
from solicitud.models import Postulacion
from user.models import User
# Create your models here.

def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(
            '{}'.format(str(uuid.uuid4())[:4])
        )
        instance.slug = slug

class DatosProyectoBase(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)    
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE, related_name='username_proyecto')   
    nombre = models.CharField(max_length=255)
    n_comunidades = models.IntegerField()
    comunidades = models.TextField()
    tipologia_proy = models.BooleanField()
    periodo_ejecu = models.IntegerField(choices=periodo_ejecucion)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    solicitud_financ = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.slug} {self.nombre}'
    
    class Meta:
        verbose_name = _('DatosProyectoBase')
        verbose_name_plural = _('DatosProyectosBase')
        db_table = 'DatosProyectoBase'

class Justificacion(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    justificacion1 = models.BooleanField()
    justificacion2 = models.BooleanField()
    justificacion3 = models.BooleanField()
    justificacion4 = models.BooleanField()
    justificacion5 = models.BooleanField()
    justificacion6 = models.BooleanField()
    justificacion7 = models.BooleanField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.slug}'
    
    class Meta:
        verbose_name = _('Justificacion')
        verbose_name_plural = _('Justificaciones')
        db_table = 'Justificacion'
    
'''
class Proyecto(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    datos_basicos = models.ForeignKey(DatosProyectoBase, on_delete=models.CASCADE)
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos')
        db_table = 'Proyecto'
'''


