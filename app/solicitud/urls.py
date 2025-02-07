from django.urls import path, include

from solicitud.views import (departamento, entidad, municipio, Confirmacion, ListaSolicitudes, ListaCompleta, ListaRechazados,
                             ResponsableProy, fichaSolicitud, mae_r, Act_ficha_Resp, Act_Ficha_MAE,
                             ListaSolicitudesEJEC, ListaRechazadosEJEC)
app_name = 'solicitud'
urlpatterns = [
    path('departamento/<int:financiamiento>/', departamento.as_view(), name='Departamento'),
    path('entidadTerritorial/<int:financiamiento>/<int:departamento>/', entidad.as_view(), name='Entidad_Territorial'),
    path('municipio/<int:financiamiento>/<int:departamento>/<int:entidad>/', municipio.as_view(), name='Municipio'),
    path('RegistroMae/<int:pk>/<int:entidad>/<int:financiamiento>/', mae_r.as_view(), name='MAE'),
    path('RegistroEncargado/<slug:slug>/', ResponsableProy.as_view(), name='ResponsableProyecto'),
    path('confirmacion/<slug:slug>/', Confirmacion.as_view(), name='Confirmacion_solicitud'),
    path('listaCompleta/', ListaCompleta.as_view(), name='ListaCompleta'),
    #ITCP
    path('listaSolicitud/', ListaSolicitudes.as_view(), name='ListaSolicitud'),
    path('listaNoAprobados/', ListaRechazados.as_view(), name='ListaRechazados'),
    path('fichaPostulacionn/<slug:slug>/', fichaSolicitud.as_view(), name='Ficha_solicitud'),
    path('actualizarPostulacionMAE/<slug:slug>', Act_Ficha_MAE.as_view(), name='Actualizar_Ficha'),
    path('actualizarPostulacionENC/<slug:slug>', Act_ficha_Resp.as_view(), name='Actualizar_Ficha_eNC'),
    #EDTP
    path('listaSolicitudEjec/', ListaSolicitudesEJEC.as_view(), name='ListaSolicitudEj'),
    path('listaNoAprobadosEjec/', ListaRechazadosEJEC.as_view(), name='ListaRechazadosEj'),
    
]

