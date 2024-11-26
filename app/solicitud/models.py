from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

from solicitud.choices import departamentos, entidad_territorial_autonoma, estado_proyecto
from user.models import EncargadoMAE, ResponsableP
from convocatoria.models import Convocatoria
from proyecto.models import DatosProyectoBase
# Create your models here.

class Municipios(models.Model):
    departamento = models.CharField(choices=departamentos, max_length=30)
    entidad_territorial = models.CharField(choices=entidad_territorial_autonoma, max_length=100 )
    nombre_municipio = models.CharField(max_length=255)
    estado = models.CharField(choices=estado_proyecto, max_length=255)
    p_a= models.BooleanField(_('Postulo Anteriormente'),default=False)
        
    def __str__(self):
        return f' {self.departamento}-{self.entidad_territorial}-{self.nombre_municipio}-{self.estado}'
    
    class Meta:
        verbose_name = _('Municipio')
        verbose_name_plural = _('Municipios')
        db_table = 'Municipio'

class Postulacion(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    municipio = models.ForeignKey(Municipios, related_name='Datos_base_proyecto', on_delete=models.CASCADE)
    mae = models.ForeignKey(EncargadoMAE, related_name='encargado_mae_p', on_delete=models.CASCADE)
    responsable = models.ForeignKey(ResponsableP, related_name='responsable_p', on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(null=True, blank=True)
    modificacion = models.BooleanField(default=False)
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='postulacion_convocatoria', null=True, blank=True)
    datos_proyecto = models.OneToOneField(DatosProyectoBase, null=True, blank=True, on_delete=models.CASCADE, related_name='postulacion', to_field='slug')

    def __str__(self):
        return f' {self.municipio} {self.fecha_registro}'
    
    class Meta:
        verbose_name = _('Postulacion')
        verbose_name_plural = _('Postulaciones')
        db_table = 'Postulaciones'
        
def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(
            '{}'.format(str(uuid.uuid4())[:4])
        )
        instance.slug = slug

pre_save.connect(set_slug, sender=Postulacion)