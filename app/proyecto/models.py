from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save
from datetime import datetime

from proyecto.choices import periodo_ejecucion, elige_alternativas, nivel, temporalidad, riesgos, estado_proyecto,tipo_hectareas
from user.models import User

from proyecto.upload import docModeloActa, docDerechoPropietario, docDeclaracionjurada
# Create your models here.

def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(
            '{}'.format(str(uuid.uuid4())[:4])
        )
        instance.slug = slug

class DatosProyectoBase(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE, related_name='username_proyecto')   
    nombre = models.CharField(max_length=255)
    comunidades = models.TextField()
    tipologia_proy = models.BooleanField()
    periodo_ejecu = models.IntegerField(choices=periodo_ejecucion)

    def __str__(self):
        return f'{self.slug} {self.nombre}'
    
    class Meta:
        verbose_name = _('DatosProyectoBase')
        verbose_name_plural = _('DatosProyectosBase')
        db_table = 'DatosProyectoBase'

class Justificacion(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    justificacion1 = models.BooleanField()
    justificacion2 = models.BooleanField()
    justificacion3 = models.BooleanField()
    justificacion4 = models.BooleanField()
    justificacion5 = models.BooleanField()
    justificacion6 = models.BooleanField()
    justificacion7 = models.BooleanField()    

    def __str__(self):
        return f'{self.slug}'
    
    class Meta:
        verbose_name = _('Justificacion')
        verbose_name_plural = _('Justificaciones')
        db_table = 'Justificacion'
    
class Idea_Proyecto(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    antecedente = models.TextField(null=False, blank=False)
    diagnostico = models.TextField(null=False, blank=False)
    planteamiento_problema = models.TextField(null=False, blank=False)
    actores_involucrados = models.TextField(null=False, blank=False)
    alternativa_1 = models.TextField(null=False, blank=False)
    alternativa_2 = models.TextField(null=False, blank=False)
    elige_alternativa = models.IntegerField(choices=elige_alternativas)
    justificacion_alter = models.TextField(null=False, blank=False)
    objetivo_general = models.TextField(null=False, blank=False)
    beneficios_alter = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Idea_Proyecto'
        managed = True
        verbose_name = 'Idea_Proyecto'
        verbose_name_plural = 'Ideas_Proyectos'

class Objetivo_especifico(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)    
    objetivo = models.TextField(null=False, blank=False)   
    componente = models.TextField(null=False, blank=False)   
    linea_base = models.TextField(null=False, blank=False)   
    indicador = models.TextField(null=False, blank=False)   
    meta = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Objetivo_especifico'
        managed = True
        verbose_name = 'Objetivo_especifico'
        verbose_name_plural = 'Objetivos_especificos'

class Beneficiario(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)    
    hombre_directo = models.IntegerField(null=False, blank=False)
    mujer_directo = models.IntegerField(null=False, blank=False)
    hombre_indirecto = models.IntegerField(null=False, blank=False)
    mujer_indirecto = models.IntegerField(null=False, blank=False)
    familia = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.slug+"beneficiario"}'

    class Meta:
        db_table = 'Beneficiario'
        managed = True
        verbose_name = 'Beneficiario'
        verbose_name_plural = 'Beneficiarios'
    
    def total_directo(self):
        return self.hombre_directo + self.mujer_directo
    
    def total_indirecto(self):
        return self.hombre_indirecto + self.mujer_indirecto
    
    def total_hombres(self):
        return self.hombre_indirecto + self.hombre_directo
    
    def total_mujeres(self):
        return self.mujer_directo + self.mujer_indirecto
    
    def total_t(self):
        return self.total_hombres() + self.total_mujeres()

    def porcentaje_hombres_directo(self):
        total = self.total_directo()
        return (self.hombre_directo / total * 100) if total > 0 else 0
    
    def porcentaje_hombres_indirecto(self):
        total = self.total_indirecto()
        return (self.hombre_indirecto / total * 100) if total > 0 else 0

    def porcentaje_mujeres_directo(self):
        total = self.total_directo()
        return (self.mujer_directo / total * 100) if total > 0 else 0
    
    def porcentaje_mujeres_indirecto(self):
        total = self.total_indirecto()
        return (self.mujer_indirecto / total * 100) if total > 0 else 0
    
    def porcentaje_hombre(self):
        total = self.total_t()
        return (self.total_hombres() / total * 100) if total > 0 else 0
    
    def porcentaje_mujeres(self):
        total = self.total_t()
        return (self.total_mujeres() / total * 100) if total > 0 else 0
    
class Modelo_Acta(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)    
    comunidades = models.CharField(null=False, blank=False)
    si_acta = models.FileField(upload_to=docModeloActa,null=True, blank=True)
    no_acta = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Modelo_Acta'
        managed = True
        verbose_name = 'Modelo_Acta'
        verbose_name_plural = 'Modelo_Actas'

class Derecho_propietario(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)    
    descripcion = models.TextField(null=False, blank=False)
    si_registro = models.FileField(upload_to=docDerechoPropietario, null=True, blank = True)
    no_registro = models.TextField(null=True, blank=True)
    zone = models.IntegerField(null=False, blank=False)
    easting = models.FloatField(null=False, blank=False)
    northing = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Derecho_propietario'
        managed = True
        verbose_name = 'Derecho_propietario'
        verbose_name_plural = 'Derechos_propietarios'

class Impacto_ambiental(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    bosque_nivel = models.CharField(choices=nivel, max_length=255)
    bosque_tempo = models.CharField(choices=temporalidad, max_length=255)
    suelo_nivel = models.CharField(choices=nivel, max_length=255)
    suelo_tempo = models.CharField(choices=temporalidad, max_length=255)
    agua_nivel = models.CharField(choices=nivel, max_length=255)
    agua_tempo = models.CharField(choices=temporalidad, max_length=255)
    aire_nivel = models.CharField(choices=nivel, max_length=255)
    aire_tempo = models.CharField(choices=temporalidad, max_length=255)
    biodiversidad_nivel = models.CharField(choices=nivel, max_length=255)
    biodiversidad_tempo = models.CharField(choices=temporalidad, max_length=255)
    otro_nombre = models.CharField(max_length=255, blank=True, null=True)
    otro_tempo = models.CharField(choices=temporalidad, max_length=255, blank=True, null=True)
    otro_nivel = models.CharField(choices=nivel, max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Impacto_ambiental'
        managed = True
        verbose_name = 'Impacto_ambiental'
        verbose_name_plural = 'Impactos_ambientales'

class Riesgo_desastre(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    riesgo = models.CharField(choices=riesgos)
    nivel = models.CharField(choices=nivel)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Riesgo_desastre'
        managed = True
        verbose_name = 'Riesgo_desastre'
        verbose_name_plural = 'Riesgos_desastres'

class Detalle_POA(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Detalle_POA'
        managed = True
        verbose_name = 'Detalle_POA'
        verbose_name_plural = 'Detalles_POA'

class Conclusion_recomendacion(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    conclusion = models.TextField(null=True, blank=True)
    recomendacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Conclusion_recomendacion'
        managed = True
        verbose_name = 'Conclusion_recomendacion'
        verbose_name_plural = 'Conclusiones_recomendaciones'

class Declaracion_jurada(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    declaracion = models.FileField(upload_to=docDeclaracionjurada)
    itcp = models.FileField(upload_to=docDeclaracionjurada)
    carta_elab = models.FileField(upload_to=docDeclaracionjurada, null=True, blank=True)
    carta_ejec = models.FileField(upload_to=docDeclaracionjurada, null=True, blank=True)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'Declaracion_jurada'
        managed = True
        verbose_name = 'Declaracion_jurada'
        verbose_name_plural = 'Declaraciones_juradas'

class PresupuestoReferencial(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    elab_sol = models.DecimalField(max_digits=10, decimal_places=2)    
    elab_fona = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    elab_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    elab_fona_p = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    elab_sol_p = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    elab_total_p = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ejec_fona = models.DecimalField(max_digits=10, decimal_places=2)
    ejec_sol = models.DecimalField(max_digits=10, decimal_places=2)
    ejec_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ejec_fona_p = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ejec_sol_p = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ejec_total_p = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        db_table = 'PresupuestoReferencial'
        managed = True
        verbose_name = 'PresupuestoReferencial'
        verbose_name_plural = 'PresupuestosReferenciales'

class Proyecto(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fechaenvio = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    aceptar = models.BooleanField()
    estado = models.CharField(choices=estado_proyecto, max_length=50, default='SIN REVISAR')
    fechaEstado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    revisor = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    comentarios = models.TextField(null=True, blank=True)
    datos_basicos = models.ForeignKey(DatosProyectoBase, on_delete=models.CASCADE, related_name='proyectoDatosBase')
    justificacion = models.ForeignKey(Justificacion, on_delete=models.CASCADE, related_name='proyectoJustificacion')
    ideaProyecto = models.ForeignKey(Idea_Proyecto, on_delete=models.CASCADE, related_name='proyectoIdea')
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, related_name='proyectoBeneficiario')
    impactoAmbiental = models.ForeignKey(Impacto_ambiental, on_delete=models.CASCADE, related_name='proyectoImpactoAmbiental')
    detallePoa = models.ForeignKey(Detalle_POA, on_delete=models.CASCADE, related_name='proyectoDetallePoa')
    conclusion = models.ForeignKey(Conclusion_recomendacion, on_delete=models.CASCADE, related_name='proyectoConclusionR')
    declaracionJurada = models.ForeignKey(Declaracion_jurada, on_delete=models.CASCADE, related_name='proyectoDeclaracionJ')
    presupuestoRef = models.ForeignKey(PresupuestoReferencial, on_delete=models.CASCADE, related_name='proyectoPreupuestoRef')
    
    class Meta:
        verbose_name = _('ProyectoITCP')
        verbose_name_plural = _('ProyectosITCP')
        db_table = 'ProyectoITCP'

class ObjetivoGeneralEjec(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fechaenvio = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    objetivo_general = models.TextField(null=False, blank=False)
    hectareas = models.IntegerField(null=False, blank=False, default=0)
    tipo_hectareas =  models.CharField(choices=tipo_hectareas, null=False, blank=False, default="")

    class Meta:
        verbose_name = _('ObjetivoGeneralEjec')
        verbose_name_plural = _('ObjetivosGeneralesEjec')
        db_table = 'ObjetivoGeneralEjec'
    
class ObjetivoEspecificoEjec(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=False)
    fechaenvio = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    objetivo = models.TextField(null=False, blank=False)   
    componente = models.TextField(null=False, blank=False)   
    meta = models.TextField(null=False, blank=False)

    class Meta:
        verbose_name = _('ObjetivoEspecificoEjec')
        verbose_name_plural = _('ObjetivosEspecificoEjec')
        db_table = 'ObjetivoEspecificoEjec'

class UbicacionGeografica(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fechaenvio = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    alturaForestacion = models.IntegerField()
    class Meta:
        verbose_name = _('UbicacionGeografica')
        verbose_name_plural = _('UbicacionesGeografica')
        db_table = 'UbicacionGeografica'
        
class EDTP(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)
    fechaenvio = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    aceptar = models.BooleanField()
    estado = models.CharField(choices=estado_proyecto, max_length=50, default='SIN REVISAR')
    fechaEstado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    revisor = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    comentarios = models.TextField(null=True, blank=True)
    datos_basicos = models.ForeignKey(DatosProyectoBase, on_delete=models.CASCADE, related_name='EDTPDatosBase')
    objetivo_gen = models.ForeignKey(ObjetivoGeneralEjec, on_delete=models.CASCADE, related_name='EDTPObjGeneral')
    Ubicacion = models.ForeignKey(UbicacionGeografica, on_delete=models.CASCADE, related_name='EDTPubicacion')
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, related_name='EDTPproyectoBeneficiario')
    presupuestoRef = models.ForeignKey(PresupuestoReferencial, on_delete=models.CASCADE, related_name='EDTPPreupuestoRef')
    declaracionJurada = models.ForeignKey(Declaracion_jurada, on_delete=models.CASCADE, related_name='EDTPDeclaracionJ')
    
    class Meta:
        verbose_name = _('EDTP')
        verbose_name_plural = _('EDTP')
        db_table = 'EDTP'