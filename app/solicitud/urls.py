from django.urls import path, include

from solicitud.views import solicitud
app_name = 'solicitud'
urlpatterns = [
    path('', solicitud.as_view(), name='Departamento'),
]

