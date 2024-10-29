from django.urls import path, include

from solicitud.views import solicitud,entidad, municipio, MAE, Confirmacion, ListaSolicitudes, ResponsableProy, fichaSolicitud
app_name = 'solicitud'
urlpatterns = [
    path('', solicitud.as_view(), name='Index'),
    path('solicitud/<int:departamento>/', entidad.as_view(), name='Entidad_Territorial'),
    path('solicitud/<int:departamento>/<int:entidad>/', municipio.as_view(), name='Municipio'),
    path('RegistroMae/<int:pk>/<int:entidad>/', MAE.as_view(), name='MAE'),
    path('RegistroEncargado/<slug:slug>/', ResponsableProy.as_view(), name='ResponsableProyecto'),
    path('confirmacion/<slug:slug>/', Confirmacion.as_view(), name='Confirmacion_solicitud'),
    path('listaSolicitud/', ListaSolicitudes.as_view(), name='ListaSolicitud'),
    path('fichaPostulacion/<slug:slug>/', fichaSolicitud.as_view(), name='Ficha_solicitud')
]

