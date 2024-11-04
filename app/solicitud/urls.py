from django.urls import path, include

from solicitud.views import solicitud,entidad, municipio, Confirmacion, ListaSolicitudes, ResponsableProy, fichaSolicitud, mae_r, Act_ficha_Resp, Act_Ficha_MAE
app_name = 'solicitud'
urlpatterns = [
    path('', solicitud.as_view(), name='Index'),
    path('solicitud/<int:departamento>/', entidad.as_view(), name='Entidad_Territorial'),
    path('solicitud/<int:departamento>/<int:entidad>/', municipio.as_view(), name='Municipio'),
    path('RegistroMae/<int:pk>/<int:entidad>/', mae_r.as_view(), name='MAE'),
    path('RegistroEncargado/<slug:slug>/', ResponsableProy.as_view(), name='ResponsableProyecto'),
    path('confirmacion/<slug:slug>/', Confirmacion.as_view(), name='Confirmacion_solicitud'),
    path('listaSolicitud/', ListaSolicitudes.as_view(), name='ListaSolicitud'),
    path('fichaPostulacionn/<slug:slug>/', fichaSolicitud.as_view(), name='Ficha_solicitud'),
    path('actualizarPostulacionMAE/<slug:slug>', Act_Ficha_MAE.as_view(), name='Actualizar_Ficha'),
    path('actualizarPostulacionENC/<slug:slug>', Act_ficha_Resp.as_view(), name='Actualizar_Ficha_eNC'),
]

