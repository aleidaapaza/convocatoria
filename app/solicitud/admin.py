from django.contrib import admin

# Register your models here.
from solicitud.models import Municipios, Postulacion

class municipiosAdm(admin.ModelAdmin):
    fields = ('departamento', 'entidad_territorial', 'nombre_municipio', 'estado', 'p_a')
    list_display = ('departamento', 'entidad_territorial', 'nombre_municipio', 'estado', 'p_a')
    search_fields = ('departamento', 'entidad_territorial',)

class postulacionAdm(admin.ModelAdmin):
    fields = ('municipio', 'mae', 'responsable', 'estado')
    list_display = ('municipio', 'fecha_registro',)
    search_fields = ('municipio', 'mae',)
    
admin.site.register(Municipios, municipiosAdm)
admin.site.register(Postulacion, postulacionAdm)
