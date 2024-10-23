from django.urls import path, include

from solicitud.views import solicitud,entidad
app_name = 'solicitud'
urlpatterns = [
    path('', solicitud.as_view(), name='Departamento'),
    path('solicitud/<str:departamento>/', entidad.as_view(), name='Entidad_Territorial'),
    
]

