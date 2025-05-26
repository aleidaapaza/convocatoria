from django.urls import path, include

from proyecto.views import (Lista_Proyectos, EnviarDatos, enviarDatos2, Lista_ProyectosDatos, verDatos, 
                            Lista_ProyectosSinRevisar, Lista_ProyectosObservados, Lista_ProyectosAprobados,
                            Lista_ProyectosEjec, Lista_ProyectosDatosEjec, Lista_ProyectosSinRevisarEjec,
                            Lista_ProyectosAprobadosEJEC, Lista_ProyectosObservadosEjec)
from proyecto.view.itcp0 import DatosPostulacion
from proyecto.view.itcp1 import RegistroDatosBasicos
from proyecto.view.itcp2 import Reg_Justificaciones, Act_Justificacion
from proyecto.view.itcp3 import (Reg_Idea_Proyecto, Act_Idea_Proyecto, Reg_Objetivo_especifico,
                                Reg_Objetivo_especifico01, Act_Objetivo_especifico, eliminarObjetivoITCP, 
                                R_Beneficios, R_Beneficiarios, A_Beneficiarios)
from proyecto.view.itcp4 import R_Modelo_Acta, R_Modelo_Acta_R, A_Modelo_Acta, eliminar_ModeloActa
from proyecto.view.itcp5 import R_Derecho_propietario, R_Derecho_propietario_R, A_Derecho_propietario, eliminar_Derecho
from proyecto.view.itcp6 import Reg_ImpactoAmbiental, Act_ImpactoAmbiental
from proyecto.view.itcp7 import R_RiesgoDesastre, Act_RiesgoDesastre, R_RiesgoDesastre_R, eliminar_Riesgos
from proyecto.view.itcp8 import Reg_DetallePOA, Act_DetallePOA
from proyecto.view.itcp9 import Reg_PresupuestoRef, Act_PresupuestoRef
from proyecto.view.itcp10 import Reg_ConclRec, Act_ConclRec
from proyecto.view.itcp11 import Reg_DeclaracionJurada, Act_DeclaracionJurada

from proyecto.viewEjec.edtp02 import (R_ObjetivoGeneral, A_ObjetivoGeneral, 
                                      R_ObjetivoEspecifico, A_ObjetivoEspecifico,
                                    eliminar_objetivoEjec, Reg_ObjetivoEsp)
from proyecto.viewEjec.edtp04 import (R_DerechoPropietarioE, A_DerechoPropietarioE, 
                                      eliminar_DerechoE, R_DerechoPropietarioER)

app_name = 'proyecto'

urlpatterns = [    
    #ListaITCP
    path('lista_aprobados/', Lista_Proyectos.as_view(), name='lista_inicio'),
    path('lista_aprobadosDatos/', Lista_ProyectosDatos.as_view(), name='lista_datos'),
      #LISTA ESTADO DE REVISIONES
    path('lista_SinRevisar/', Lista_ProyectosSinRevisar.as_view(), name='lista_datosSinrevisar'),
    path('lista_Observados/', Lista_ProyectosObservados.as_view(), name='lista_datosObservados'),
    path('lista_Aprobados/', Lista_ProyectosAprobados.as_view(), name='lista_datosAprobados'),
    #ListaEDTP
    path('lista_aprobadosEjec/', Lista_ProyectosEjec.as_view(), name='lista_inicioEjec'),
    path('lista_aprobadosDatosEjec/', Lista_ProyectosDatosEjec.as_view(), name='lista_datosEjec'),
      #LISTA ESTADO DE REVISIONES
    path('lista_SinRevisarEjec/', Lista_ProyectosSinRevisarEjec.as_view(), name='lista_datosSinrevisarEjec'),
    path('lista_ObservadosEjec/', Lista_ProyectosObservadosEjec.as_view(), name='lista_datosObservadosEjec'),
    path('lista_AprobadosEjec/', Lista_ProyectosAprobadosEJEC.as_view(), name='lista_datosAprobadosEjec'),
    #Datos Postulacion
    path('DatosPostulacion/<slug:slug>', DatosPostulacion.as_view(), name='datos_postulacion'),
    #ITCP y EDTP
    path('Reg_DatosPrincipales/<slug:slug>', RegistroDatosBasicos.as_view(), name='registro_Base'),
    path('Reg_Beneficiarios/<slug:slug>', R_Beneficiarios.as_view(), name='registro_Beneficiarios'),
    path('Act_Beneficiarios/<slug:slug>', A_Beneficiarios.as_view(), name='actualizar_Beneficiarios'),
    path('Reg_DeclaracionJurada/<slug:slug>', Reg_DeclaracionJurada.as_view(), name='registro_DeclaracionJurada'),
    path('Act_DeclaracionJurada/<slug:slug>', Act_DeclaracionJurada.as_view(), name='actualizar_DeclaracionJurada'),
    path('Reg_PresupuestoReferencial/<slug:slug>', Reg_PresupuestoRef.as_view(), name='registro_PresupuestoRef'),
    path('Act_PresupuestoReferencial/<slug:slug>', Act_PresupuestoRef.as_view(), name='actualizar_PresupuestoRef'),
    #ITCP
    path('Reg_Justificacion/<slug:slug>', Reg_Justificaciones.as_view(), name='registro_justificacion'),
    path('Act_Justificacion/<slug:slug>', Act_Justificacion.as_view(), name='actualizar_justificacion'),
    path('Reg_Idea_Proyecto/<slug:slug>', Reg_Idea_Proyecto.as_view(), name='registro_Idea_proyecto'),
    path('Act_Idea_Proyecto/<slug:slug>', Act_Idea_Proyecto.as_view(), name='actualizar_Idea_proyecto'),
    path('Reg_Objetivos_Especificos/<slug:slug>', Reg_Objetivo_especifico.as_view(), name='registro_obj_especifico'),
    path('Reg_Objetivos_Especificos/<slug:slug>/', Reg_Objetivo_especifico01.as_view(), name='registro_obj_especifico_01'),
    path('Act_Objetivos_EspecificosITCP/<slug:slug>', Act_Objetivo_especifico.as_view(), name='actualizar_obj_especifico'),
    path('eliminar-objetivoITCP/<int:objetivo_id>/', eliminarObjetivoITCP, name='eliminar_objetivoITCP'),
    path('Beneficios/<slug:slug>/', R_Beneficios.as_view(), name='registro_Beneficios'),    
    path('Reg_ModeloActa/<slug:slug>', R_Modelo_Acta.as_view(), name='registro_ModeloActa'),
    path('Reg_ModeloActaR/<slug:slug>', R_Modelo_Acta_R.as_view(), name='registro_ModeloActa01'),
    path('Act_ModeloActa/<slug:slug>', A_Modelo_Acta.as_view(), name='actualizar_ModeloActa'),
    path('eliminar-modeloActa/<int:objetivo_id>/', eliminar_ModeloActa, name='eliminar_modeloActa'),
    path('Reg_DerechoPropietario/<slug:slug>', R_Derecho_propietario.as_view(), name='registro_DerechoPropietario'),
    path('Reg_DerechoPropietario_R/<slug:slug>', R_Derecho_propietario_R.as_view(), name='registro_DerechoPropietario_R'),
    path('Act_DerechoPropietario/<slug:slug>', A_Derecho_propietario.as_view(), name='actualizar_DerechoPropietario'),
    path('eliminar-DerechoPropI/<int:objetivo_id>/', eliminar_Derecho, name='eliminar_Derecho'),
    path('Reg_ImpactoAmbiental/<slug:slug>', Reg_ImpactoAmbiental.as_view(), name='registro_ImpactoAmbiental'),
    path('Act_ImpactoAmbiental/<slug:slug>', Act_ImpactoAmbiental.as_view(), name='actualizar_ImpactoAmbiental'),
    path('Reg_RiesgoDesastre/<slug:slug>', R_RiesgoDesastre.as_view(), name='registro_RiesgoDesastre'),
    path('Reg_RiesgoDesastcre_R/<slug:slug>', R_RiesgoDesastre_R.as_view(), name='registro_RiesgoDesastre_R'),
    path('Act_RiesgoDesastre/<slug:slug>', Act_RiesgoDesastre.as_view(), name='actualizar_RiesgoDesastre'),
    path('eliminar-Riesgo/<int:objetivo_id>/', eliminar_Riesgos, name='eliminar_Riesgo'),
    path('Reg_DetallePOA/<slug:slug>', Reg_DetallePOA.as_view(), name='registro_DetallePOA'),
    path('Act_DetallePOA/<slug:slug>', Act_DetallePOA.as_view(), name='actualizar_DetallePOA'),
    path('Reg_ConclusionRecomendacion/<slug:slug>', Reg_ConclRec.as_view(), name='registro_ConclRec'),
    path('Act_ConclusionRecomendacion/<slug:slug>', Act_ConclRec.as_view(), name='actualizar_ConclRec'),
    #EDTP
    path('Reg_ObjetivoGeneralEjec/<slug:slug>', R_ObjetivoGeneral.as_view(), name='registro_ObjetivoGeneral'),
    path('Act_ObjetivoGeneralEjec/<slug:slug>', A_ObjetivoGeneral.as_view(), name='actualizar_ObjetivoGeneral'),
    path('Reg_ObjetivoEspecificoEjec/<slug:slug>', R_ObjetivoEspecifico.as_view(), name='registro_ObjetivoEspecifico'),
    path('Act_ObjetivoEspecificoEjec/<slug:slug>', A_ObjetivoEspecifico.as_view(), name='actualizar_ObjetivoEspecifico'),
    path('eliminarObjetivoEjec/<int:objetivo_id>/', eliminar_objetivoEjec, name='eliminarObjetivoEjec'),
    path('Act_ObjetivoEspecificoEjec/<slug:slug>', Reg_ObjetivoEsp.as_view(), name='actualizar_ObjetivoEspecificoE'),
    path('Reg_DerechoPropietarioEjec/<slug:slug>', R_DerechoPropietarioE.as_view(), name='registro_DerechoPropietarioE'),
    path('Act_DerechoPropietarioEjec/<slug:slug>', A_DerechoPropietarioE.as_view(), name='actualizar_DerechoPropietarioE'),
    path('eliminar-DerechoProp/<int:objetivo_id>/', eliminar_DerechoE, name='eliminar_DerechoE'),
    path('Act_DerechoPropietarioER/<slug:slug>', R_DerechoPropietarioER.as_view(), name='agregar_DerechoPropietarioE'),

    #ENVIO DE DATOS    
    path('EnviarDatos/<slug:slug>', EnviarDatos.as_view(), name='enviar_datos'),
    path('EnviarDatos1/<slug:slug>', enviarDatos2.as_view(), name='enviar_datos2'),
    #VISUALIZAR DATOS ENVIADOS
    path('VerDatos/<slug:slug>', verDatos.as_view(), name='ver_Datos'),    
    
    ]
