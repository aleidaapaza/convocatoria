from django.db.models import Count
from convocatoria.models import Convocatoria
from solicitud.models import Postulacion
from proyecto.models import Proyecto, EDTP
def obtener_estadisticas_convocatoria(user):
    # Filtrar las convocatorias activas (estado=True)
    estado = Convocatoria.objects.filter(estado=True)
    
    # Verificar si solo hay un elemento en el queryset
    if estado.count() == 1:
        select_conv = estado.first()
        convocatoria = Convocatoria.objects.get(slug=select_conv.slug)
        
        # Obtener las estadísticas relacionadas con las postulaciones y proyectos
        c_sol_itcp = Postulacion.objects.filter(convocatoria=convocatoria, tipo_financiamiento=1, estado=None).count()
        c_sol_edtp = Postulacion.objects.filter(convocatoria=convocatoria, tipo_financiamiento=2, estado=None).count()
        
        c_itcp_SR = Proyecto.objects.filter(
            datos_basicos__postulacion__convocatoria=convocatoria,
            datos_basicos__postulacion__tipo_financiamiento=1,
            estado='SIN REVISAR'
        ).count()

        c_edtp_SR = EDTP.objects.filter(
            datos_basicos__postulacion__convocatoria=convocatoria,
            datos_basicos__postulacion__tipo_financiamiento=2,
            estado='SIN REVISAR'
        ).count()

        c_itcp_CO = Proyecto.objects.filter(
            datos_basicos__postulacion__convocatoria=convocatoria,
            datos_basicos__postulacion__tipo_financiamiento=1,
            estado__in=['CON OBSERVACION', 'CORREGIDO'],
            revisor=user,
        ).count()

        c_edtp_CO = EDTP.objects.filter(
            datos_basicos__postulacion__convocatoria=convocatoria,
            datos_basicos__postulacion__tipo_financiamiento=2,
            estado__in=['CON OBSERVACION', 'CORREGIDO'],
            revisor=user,
        ).count()

        # Retornar los resultados en un diccionario
        return {
            'c_sol_itcp': c_sol_itcp,
            'c_sol_edtp': c_sol_edtp,
            'c_itcp_SR': c_itcp_SR,
            'c_edtp_SR': c_edtp_SR,
            'c_itcp_CO': c_itcp_CO,
            'c_edtp_CO': c_edtp_CO
        }
    return None

def contar_por_convocatoria(user, id_conv):
    postulaciones = Postulacion.objects.filter(convocatoria__slug=id_conv)
    sin_revisar_sol_1 = postulaciones.filter(estado=None).filter(tipo_financiamiento=1).count()
    sin_revisar_sol_2 = postulaciones.filter(estado=None).filter(tipo_financiamiento=2).count()
    return {
        'sin_revisar_sol_1' : sin_revisar_sol_1,
        'sin_revisar_sol_2' : sin_revisar_sol_2,
    }