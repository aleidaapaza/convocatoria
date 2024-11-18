from django.urls import path, include
from convocatoria.views import Reg_Convocatoria, Act_Convocatoria, ListaConvocatoria, Index

app_name = 'convocatoria'
urlpatterns = [
    path('', Index.as_view(), name='Index'),
    path('ListaConvocatoria/', ListaConvocatoria.as_view(), name='lista_convocatoria'),
    path('RegistroConvocatoria/', Reg_Convocatoria.as_view(), name='registro_convocatoria'),
    path('ActualizarConvocatoria/<slug:slug>/', Act_Convocatoria.as_view(), name='Actualizar_convocatoria'),
]