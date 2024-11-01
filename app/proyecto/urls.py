from django.urls import path, include

from proyecto.views import Lista_Proyectos, RegistroDatosBasicos, Reg_Justificaciones

app_name = 'proyecto'

urlpatterns = [
    path('lista_aprobados/', Lista_Proyectos.as_view(), name='lista_inicio'),
    path('Reg_DatosPrincipales/<slug:slug>', RegistroDatosBasicos.as_view(), name='registro_Base'),
    path('Reg_Justificacion/<slug:slug>', Reg_Justificaciones.as_view(), name='registro_justificacion'),
    ]
