from django.urls import path, include
from convocatoria.views import Reg_Convocatoria, Act_Convocatoria, ListaConvocatoria, Index, Ver_Convocatoria, Detalle_convocatoria
from proyecto.views import generate_pdf

app_name = 'convocatoria'
urlpatterns = [
    path('', Index.as_view(), name='Index'),
    path('ListaConvocatoria/', ListaConvocatoria.as_view(), name='lista_convocatoria'),
    path('RegistroConvocatoria/', Reg_Convocatoria.as_view(), name='registro_convocatoria'),
    path('ActualizarConvocatoria/<slug:slug>/', Act_Convocatoria.as_view(), name='Actualizar_convocatoria'),
    path('VerConvocatoria/<slug:slug>/', Ver_Convocatoria.as_view(), name='Ver_convocatoria'),
    path('generar_pdf/<slug:slug>/', generate_pdf, name='generar_pdf'),
    path('detalleConvocatria/<int:id>/', Detalle_convocatoria.as_view(), name='detalle_convocatoria'),
    ]