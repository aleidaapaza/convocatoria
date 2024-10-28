from django.urls import path, include

from solicitud.views import solicitud,entidad, municipio, Mae_Responsable, Confirmacion, ListaSolicitudes
app_name = 'solicitud'
urlpatterns = [
    path('', solicitud.as_view(), name='Index'),
    path('solicitud/<int:departamento>/', entidad.as_view(), name='Entidad_Territorial'),
    path('solicitud/<int:departamento>/<int:entidad>/', municipio.as_view(), name='Municipio'),
    path('RegistroMae/<int:pk>/<int:entidad>/', Mae_Responsable.as_view(), name='Responsable_MAE'),
    path('confirmacion/<slug:slug>/', Confirmacion.as_view(), name='Confirmacion_solicitud'),
    path('listaSolicitud/', ListaSolicitudes.as_view(), name='ListaSolicitud')
]

