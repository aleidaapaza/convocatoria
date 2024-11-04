from django.urls import path, include

from proyecto.views import (Lista_Proyectos, RegistroDatosBasicos, Reg_Justificaciones, Act_Justificacion, Reg_Idea_Proyecto, Act_Idea_Proyecto,
                            Reg_Objetivo_especifico, Act_Objetivo_especifico, Reg_Objetivo_especifico01, R_Beneficios,
                            R_Beneficiarios, A_Beneficiarios, R_Modelo_Acta, A_Modelo_Acta, R_Modelo_Acta_R, R_Derecho_propietario)
from proyecto.views import (eliminar_objetivo, eliminar_ModeloActa)

app_name = 'proyecto'

urlpatterns = [
    path('lista_aprobados/', Lista_Proyectos.as_view(), name='lista_inicio'),
    path('Reg_DatosPrincipales/<slug:slug>', RegistroDatosBasicos.as_view(), name='registro_Base'),
    path('Reg_Justificacion/<slug:slug>', Reg_Justificaciones.as_view(), name='registro_justificacion'),
    path('Act_Justificacion/<slug:slug>', Act_Justificacion.as_view(), name='actualizar_justificacion'),
    path('Reg_Idea_Proyecto/<slug:slug>', Reg_Idea_Proyecto.as_view(), name='registro_Idea_proyecto'),
    path('Act_Idea_Proyecto/<slug:slug>', Act_Idea_Proyecto.as_view(), name='actualizar_Idea_proyecto'),
    path('Reg_Objetivos_Especificos/<slug:slug>', Reg_Objetivo_especifico.as_view(), name='registro_obj_especifico'),
    path('Reg_Objetivos_Especificos/<slug:slug>/', Reg_Objetivo_especifico01.as_view(), name='registro_obj_especifico_01'),
    path('Act_Objetivos_Especificos/<slug:slug>', Act_Objetivo_especifico.as_view(), name='actualizar_obj_especifico'),
    path('eliminar-objetivo/<int:objetivo_id>/', eliminar_objetivo, name='eliminar_objetivo'),
    path('Beneficios/<slug:slug>', R_Beneficios.as_view(), name='registro_Beneficios'),
    path('Reg_Beneficiarios/<slug:slug>', R_Beneficiarios.as_view(), name='registro_Beneficiarios'),
    path('Act_Beneficiarios/<slug:slug>', A_Beneficiarios.as_view(), name='actualizar_Beneficiarios'),
    path('Reg_ModeloActa/<slug:slug>', R_Modelo_Acta.as_view(), name='registro_ModeloActa'),
    path('Reg_ModeloActaR/<slug:slug>', R_Modelo_Acta_R.as_view(), name='registro_ModeloActa01'),
    path('Act_ModeloActa/<slug:slug>', A_Modelo_Acta.as_view(), name='actualizar_ModeloActa'),
    path('eliminar-modeloActa/<int:objetivo_id>/', eliminar_ModeloActa, name='eliminar_modeloActa'),
    path('Reg_DerechoPropietario/<slug:slug>', R_Derecho_propietario.as_view(), name='registro_DerechoPropietario'),
    ]
