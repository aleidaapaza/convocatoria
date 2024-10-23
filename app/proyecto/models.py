from django.db import models
from django.utils.translation import gettext_lazy as _

from proyecto.choices import periodo_ejecucion
# Create your models here.

class DatosProyectoBase(models.Model):
    nombre = models.CharField(max_length=255)
    n_comunidades = models.IntegerField()
    comunidades = models.TextField()
    tipologia_proy = models.BooleanField()
    periodo_ejecu = models.IntegerField(choices=periodo_ejecucion)

    def __str__(self):
        return f' {self.nombre}'
    
    class Meta:
        verbose_name = _('DatosProyectoBase')
        verbose_name_plural = _('DatosProyectosBase')
        db_table = 'DatosProyectoBase'
