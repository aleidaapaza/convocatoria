from django.urls import path, include

from solicitud.views import solicitud,entidad, municipio
app_name = 'solicitud'
urlpatterns = [
    path('', solicitud.as_view(), name='Departamento'),
    path('solicitud/<int:departamento>/', entidad.as_view(), name='Entidad_Territorial'),
    path('solicitud/<int:departamento>/<int:entidad>/', municipio.as_view(), name='Municipio'),
]

