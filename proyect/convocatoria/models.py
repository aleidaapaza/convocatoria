from django.db import models
import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save
from convocatoria.choices import megas
from convocatoria.upload import convocatoria_doc
# Create your models here.

def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(
            '{}'.format(str(uuid.uuid4())[:4])
        )
        instance.slug = slug

class Convocatoria(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(null=False, blank=False, max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=False)
    fechaLanzamiento = models.DateField(null=False, blank=False)
    horaLanzamiento = models.TimeField(null=False, blank=False)
    fechaCierre = models.DateField(null=False, blank=False)
    horaCierre = models.TimeField(null=False, blank=False)
    montoElabEDTP = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montoEjecEDTP = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.BooleanField(default=False)
    tamanoDoc = models.IntegerField(choices=megas, null=False, blank=False, default=2)
    elabEdtp = models.BooleanField(default=False)
    EjecEdtp = models.BooleanField(default=False)
    documento = models.FileField(upload_to=convocatoria_doc)
    guia = models.FileField(upload_to=convocatoria_doc)
    guiaVideo = models.CharField(max_length=255, null=True, blank=True)
    banner = models.ImageField(upload_to=convocatoria_doc, null=True, blank=True)
    
    def __str__(self):
        return f' {self.slug} {self.nombre}'

    class Meta:
        db_table = 'Convocatoria'
        managed = True
        verbose_name = 'Convocatoria'
        verbose_name_plural = 'Convocatorias'

pre_save.connect(set_slug, sender=Convocatoria)
