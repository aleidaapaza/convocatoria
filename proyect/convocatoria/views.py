from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count, Q
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

from solicitud.models import Postulacion, Municipios
from user.models import Revisor, SuperUser, User
from convocatoria.funciones import obtener_estadisticas_convocatoria
from convocatoria.models import Convocatoria
from convocatoria.forms import R_Convocatoria, A_Convocatoria

from proyecto.models import (DatosProyectoBase, Justificacion, Idea_Proyecto,
                             Objetivo_especifico, Beneficiario, Modelo_Acta,
                             Derecho_propietario, Impacto_ambiental, Riesgo_desastre,
                             Detalle_POA, Conclusion_recomendacion, Declaracion_jurada,
                             PresupuestoReferencial, Proyecto, ObjetivoGeneralEjec, ObjetivoEspecificoEjec, UbicacionGeografica, EDTP)
# Create your views here.


class Reg_Convocatoria(CreateView):
    model=Convocatoria
    form_class = R_Convocatoria
    template_name = 'convocatoria/R_Convocatoria.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['titulo'] = 'REGISTRO DE LA CONVOCATORIA'
        context['entity'] = 'REGISTRO DE LA CONVOCATORIA'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse('convocatoria:lista_convocatoria', args=[])
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            elabEDTP = form.cleaned_data.get('montoElabEDTP')
            documento = form.cleaned_data.get('documento')
            guia = form.cleaned_data.get('guia')
            banner = form.cleaned_data.get('banner')
            if documento and documento.size > 2 * 1024 * 1024:  # 2 MB
                messages.error(request, 'El archivo DOCUMENTO no debe superar los 2 MB.')                
            if guia and guia.size > 2 * 1024 * 1024:  # 2 MB
                messages.error(request, 'El archivo GUIA no debe superar los 2 MB.')                
            if banner and banner.size > 2 * 1024 * 1024:  # 2 MB
                messages.error(request, 'El archivo IMAGEN BANNER no debe superar los 2 MB.')            
            if messages.get_messages(request):
                return self.render_to_response(self.get_context_data(form=form))
            form.save()
            return HttpResponseRedirect(reverse('convocatoria:lista_convocatoria', args=[]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Act_Convocatoria(UpdateView):
    model=Convocatoria
    form_class = A_Convocatoria
    template_name = 'convocatoria/R_Convocatoria.html'
    
    def get_context_data(self, **kwargs):
        context = super(Act_Convocatoria, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET, self.request.FILES)
        context['titulo'] = 'ACTUALIZACION DE LA CONVOCATORIA'
        context['entity'] = 'ACTUALIZACION DE LA CONVOCATORIA'
        context['accion'] = 'Actualizar'
        context['accion2'] = 'Volver'
        context['accion2_url'] = reverse('convocatoria:lista_convocatoria', args=[])
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        objeto = self.model.objects.get(slug=slug)     
        form = self.form_class(request.POST, request.FILES, instance = objeto)
        if form.is_valid():
            elabEDTP = form.cleaned_data.get('montoElabEDTP')
            print(elabEDTP)
            if elabEDTP == 0 or elabEDTP == None:
                conv = form.save(commit=False)
                conv.montoElabEDTP = 0
                conv.save()
            else:
                form.save()
            return HttpResponseRedirect(reverse('convocatoria:Actualizar_convocatoria', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Ver_Convocatoria(DetailView):  # Cambiar de UpdateView a DetailView
    model = Convocatoria
    template_name = 'convocatoria/V_Convocatoria.html'  # Plantilla para mostrar los datos
    context_object_name = 'convocatoria'  # Usamos el nombre 'convocatoria' para la instancia en la plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'DETALLES DE LA CONVOCATORIA'
        context['entity'] = 'Detalles de la Convocatoria'
        context['accion'] = 'Ver Detalles'
        context['accion2'] = 'Volver'
        context['accion2_url'] = reverse('convocatoria:lista_convocatoria')
        user = self.request.user  # Usamos el usuario actual
        stats = obtener_estadisticas_convocatoria(user)
        if stats:
            context.update({
                'c_sol_itcp': stats['c_sol_itcp'],
                'c_sol_edtp': stats['c_sol_edtp'],
                'c_itcp_SR': stats['c_itcp_SR'],
                'c_edtp_SR': stats['c_edtp_SR'],
                'c_itcp_CO': stats['c_itcp_CO'],
                'c_edtp_CO': stats['c_edtp_CO'],
            })
        return context

class ListaConvocatoria(ListView):
    model = Convocatoria
    template_name = 'convocatoria/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superuser']=True
        context['titulo'] = 'LISTA DE CONVOCATORIA'
        context['activate'] = True
        context['entity'] = 'LISTA DE CONVOCATORIA'
        context['object_list'] = self.model.objects.all()
        estado = self.model.objects.filter(estado=True).count()
        if estado > 0:
            context['error'] = 'REGISTRAR CONVOCATORIA'
            context['message'] = 'Existe una convocatoria vigente actualmente, para registrar otra convocatoria se necesita que las anteriores no esten activas'
        else:
            if self.request.user.is_authenticated:
                if self.request.user.is_superuser:                            
                    context['entity_registro'] = reverse_lazy('convocatoria:registro_convocatoria')
                    context['entity_registro_nom'] = 'REGISTRAR CONVOCATORIA'
        user = self.request.user  # Usamos el usuario actual
        stats = obtener_estadisticas_convocatoria(user)
        if stats:
            context.update({
                'c_sol_itcp': stats['c_sol_itcp'],
                'c_sol_edtp': stats['c_sol_edtp'],
                'c_itcp_SR': stats['c_itcp_SR'],
                'c_edtp_SR': stats['c_edtp_SR'],
                'c_itcp_CO': stats['c_itcp_CO'],
                'c_edtp_CO': stats['c_edtp_CO'],
            })
        return context
    
class Index(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        if messages:
        # Si hay mensajes de éxito, error, etc.
            for message in messages.get_messages(self.request):
                    if message.level_tag == 'success':
                        context['message_title'] = 'Actualización Exitosa'
                        context['message_content'] = message.message
                    elif message.level_tag == 'error':
                        context['message_title'] = 'Error al Actualizar'
                        context['message_content'] = message.message
                    elif message.level_tag == 'warning':
                        context['message_title'] = 'Advertencia'
                        context['message_content'] = message.message
                    else:
                        context['message_title'] = 'Información'
                        context['message_content'] = message.message
        if self.request.user.is_authenticated:
            if self.request.user.is_municipio:
                context['titulo'] = 'AVANCE DEL REGISTRO'
                user_sl = self.request.user.username_proyecto.slug
                context['slug']=user_sl
                postulacion_p = Postulacion.objects.get(slug =user_sl)
                postulacion_p.fecha_ultimaconexion = datetime.now()
                postulacion_p.save()
                context['proyecto'] = postulacion_p
                context['postulacion'] = postulacion_p
                context['datosProyecto'] = DatosProyectoBase.objects.filter(slug=user_sl).count()
                context['beneficiario'] = Beneficiario.objects.filter(slug=user_sl).count()
                context['declaracion'] = Declaracion_jurada.objects.filter(slug=user_sl).count()
                context['Presupuesto'] = PresupuestoReferencial.objects.filter(slug=user_sl).count()
                if postulacion_p.tipo_financiamiento == 1:
                    context['justificacion'] = Justificacion.objects.filter(slug=user_sl).count()
                    context['ideaProyecto'] = Idea_Proyecto.objects.filter(slug=user_sl).count()
                    context['objetivoEsp'] = Objetivo_especifico.objects.filter(slug=user_sl).count()
                    if Idea_Proyecto.objects.filter(slug=user_sl).exists():
                        idea = Idea_Proyecto.objects.get(slug=user_sl)
                        beneficio = idea.beneficios_alter
                        if beneficio == None:
                            context['beneficio'] = False
                        else:
                            context['beneficio'] = True
                    context['modeloActa'] = Modelo_Acta.objects.filter(slug=user_sl).count()
                    context['DerechoPropie'] = Derecho_propietario.objects.filter(slug=user_sl).count()
                    context['impactoAmbiental'] = Impacto_ambiental.objects.filter(slug=user_sl).count()
                    context['riesgoDesastre'] = Riesgo_desastre.objects.filter(slug=user_sl).count()
                    context['detallePoa'] = Detalle_POA.objects.filter(slug=user_sl).count()
                    context['conclusion'] = Conclusion_recomendacion.objects.filter(slug=user_sl).count()
                else:
                    context['ObjetivoGeneral'] = ObjetivoGeneralEjec.objects.filter(slug=user_sl).count()
                    context['ObjetivoEspecifico'] = ObjetivoEspecificoEjec.objects.filter(slug=user_sl).count()
                    context['Ubicacion'] = UbicacionGeografica.objects.filter(slug=user_sl).count()                
                if postulacion_p.tipo_financiamiento == 1:                    
                    if Proyecto.objects.filter(slug=user_sl).exists():
                        print(Proyecto.objects.filter(slug=user_sl).exists())                        
                        proyecto = Proyecto.objects.get(slug=user_sl)
                        if proyecto.estado == "CON OBSERVACION":
                            context['proyectoDatos'] = proyecto
                            context['vista'] = False
                        else:
                            context['vista'] = True
                    else:
                        context['vista'] = False
                else:
                    if EDTP.objects.filter(slug=user_sl).exists():
                        print(EDTP.objects.filter(slug=user_sl).exists())                        
                        proyecto = EDTP.objects.get(slug=user_sl)
                        if proyecto.estado == "CON OBSERVACION":
                            context['proyectoDatos'] = proyecto
                            context['vista'] = False
                        else:
                            context['vista'] = True
                    else:
                        context['vista'] = False
            elif self.request.user.is_revisor or self.request.user.is_superuser:                
                if self.request.user.is_revisor:
                    user_sl = self.request.user.revisor_perfil.slug
                    postulacion_p = Revisor.objects.get(slug = user_sl)
                elif self.request.user.is_superuser:
                    user_sl = self.request.user.superuser_perfil.slug
                    postulacion_p = SuperUser.objects.get(slug = user_sl)
                context['slug']=user_sl
                context['superuser']=True
                context['postulacion'] = postulacion_p
                user = self.request.user
                convocatoria = Convocatoria.objects.all().order_by('-id')
                context['convocatoria'] = convocatoria                
        else:
            estado = Convocatoria.objects.filter(estado=True).count()
            if estado == 1:
                context['activo'] = True
                fecha = Convocatoria.objects.get(estado=True)
                context['convocatoria']=fecha
                fechaHoy = datetime.now()
                print(fechaHoy, 'fecha actual')
                fechalanzamiento = datetime.combine(fecha.fechaLanzamiento, fecha.horaLanzamiento)
                fechaCierre = datetime.combine(fecha.fechaCierre, fecha.horaCierre)
                if fechalanzamiento <= fechaHoy and fechaHoy <= fechaCierre:
                    context['fechaActivo'] = True
                    context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
                    print(fechaCierre.isoformat(), "expiracion")
                elif fechalanzamiento >= fechaHoy:
                    context['fechaActivo'] = False
                    context['fecha_expiracion'] = fechalanzamiento.isoformat() if fechalanzamiento else None
                    context['message_fecha'] = 'ESPERANDO LA APERTURA DE LA CONVOCATORIA ACTUAL'   
                    context['estadotemporal']='LANZAMIENTO'
                    context['imagen'] = 'img/fondo/esperando.png'
                elif fechaCierre < fechaHoy:
                    context['fechaActivo'] = False
                    context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
                    print("cerrado")
                    fecha.estado = False
                    fecha.save()
                    context['message_fecha'] = 'SE CERRO LA CONVOCATORIA ACTUAL' 
                    context['estadotemporal']='CIERRE'
                    context['imagen'] = 'img/fondo/cierre.png'                
            elif estado > 0:
                context['activo'] = False
                context['message'] = 'Se tiene mas de dos convocatorias activas por favor contactese con el encargado para reportar este error'
                context['conteo'] = estado
                context['imagen'] = 'img/fondo/problema.png'
            elif estado == 0:
                fecha_actual = timezone.now().date()
                convocatorias_recientes = Convocatoria.objects.filter(fechaCierre__gte=fecha_actual).order_by('fechaCierre').first()
                if convocatorias_recientes and convocatorias_recientes.estado == False:
                    print(convocatorias_recientes)
                    fechaCierre = convocatorias_recientes.fechaCierre
                    fechalimite = fechaCierre + timedelta(days=10)
                    print(fechalimite)
                    print(fecha_actual)
                    if fecha_actual <= fechalimite:
                        context['activo'] = True  
                        context['message'] = 'SE CERRO LA CONVOCATORIA ACTUAL'
                        context['message_fecha'] = 'SE CERRO LA CONVOCATORIA ACTUAL' 
                        context['estadotemporal']='CIERRE'
                        context['convocatoria']= convocatorias_recientes
                        context['fecha_expiracion']= datetime.combine(convocatorias_recientes.fechaCierre, convocatorias_recientes.horaCierre)
                        context['imagen'] = 'img/fondo/cierre.png'
                    else:
                        print("No se encontró ninguna convocatoria reciente.")
                        context['activo'] = False
                        context['message'] = 'No se tiene una convocatoria vigente por el momento.'
                        context['conteo'] = estado
                        context['imagen'] = 'img/fondo/esperando.png'          
                else:
                    print("No se encontró ninguna convocatoria reciente.")
                    context['activo'] = False
                    context['message'] = 'No se tiene una convocatoria vigente por el momento.'
                    context['conteo'] = estado
                    context['imagen'] = 'img/fondo/esperando.png'            
        return context

class Detalle_convocatoria(TemplateView):
    template_name='index/Convocatoria/descripcion.html'
    def get_context_data(self, **kwargs):
        context = super(Detalle_convocatoria, self).get_context_data(**kwargs)
        id_conv = self.kwargs.get('slug', None)
        convocatoria = Convocatoria.objects.get(slug=id_conv)
        postulaciones = Postulacion.objects.filter(convocatoria__slug=convocatoria.slug)
        num_total = postulaciones.count()
        totalFin1 = postulaciones.filter(tipo_financiamiento=1).count()
        totalFin2 = postulaciones.filter(tipo_financiamiento=2).count()
        total_SR = postulaciones.filter(estado=False).count()
        context['convocatoria']=convocatoria
        context['postulaciones']=postulaciones
        context['num_total']=num_total
        context['totalFin1']=totalFin1
        context['totalFin2']=totalFin2
        context['total_SR']=total_SR
        if convocatoria.elabEdtp:
            fin1_env=Proyecto.objects.filter(datos_basicos__postulacion__convocatoria__slug=convocatoria.slug)
            fin1_no_env = Postulacion.objects.filter(convocatoria__slug=convocatoria.slug).filter(tipo_financiamiento=1).filter(datos_proyecto=None)
            fin1_env_c=fin1_env.count()
            fin1_srevisar = fin1_env.filter(estado='SIN REVISAR')
            fin1_srevisar_c = fin1_srevisar.count()
            fin1_observar = fin1_env.filter(estado='CON OBSERVACION')
            fin1_observar_c = fin1_observar.count()
            fin1_aprobado = fin1_env.filter(estado='APROBADO')
            fin1_aprobado_c = fin1_aprobado.count()
            context['fin1_env']=fin1_env
            context['fin1_no_env']=fin1_no_env
            context['fin1_env_c']=fin1_env_c
            context['fin1_sin_enviar']=totalFin1 - fin1_env_c
            context['fin1_srevisar_c']=fin1_srevisar_c
            context['fin1_observar_c']=fin1_observar_c
            context['fin1_aprobado_c']=fin1_aprobado_c
        if convocatoria.EjecEdtp:
            fin2_env=EDTP.objects.filter(datos_basicos__postulacion__convocatoria__slug=convocatoria.slug)
            fin2_no_env = Postulacion.objects.filter(convocatoria__slug=convocatoria.slug).filter(tipo_financiamiento=2).filter(datos_proyecto=None)
            fin2_env_c=fin2_env.count()
            fin2_srevisar = fin2_env.filter(estado='SIN REVISAR')
            fin2_srevisar_c = fin2_srevisar.count()
            fin2_observar = fin2_env.filter(estado='CON OBSERVACION')
            fin2_observar_c = fin2_observar.count()
            fin2_aprobado = fin2_env.filter(estado='APROBADO')
            fin2_aprobado_c = fin2_aprobado.count()
            context['fin2_env']=fin2_env
            context['fin2_no_env']=fin2_no_env
            context['fin2_env_c']=fin2_env_c
            context['fin2_sin_enviar']=totalFin2 - fin2_env_c
            context['fin2_srevisar_c']=fin2_srevisar_c
            context['fin2_observar_c']=fin2_observar_c
            context['fin2_aprobado_c']=fin2_aprobado_c
        return context
    
class ListaMunicipios(TemplateView):
    template_name='index/Convocatoria/municipios.html'
    def get_context_data(self, **kwargs):
        context = super(ListaMunicipios, self).get_context_data(**kwargs)
        municipio = Municipios.objects.all()
        context['municipio'] = municipio
        context['superuser']=True
        return context
    
class DetalleMuncipios(TemplateView):
    template_name='index/Convocatoria/municipiosDetalle.html'
    def get_context_data(self, **kwargs):
        context = super(DetalleMuncipios, self).get_context_data(**kwargs)
        id_mun = self.kwargs.get('id', None)
        municipio = Municipios.objects.get(id=id_mun)
        postulaciones = Postulacion.objects.filter(municipio__id=municipio.id)
        edtp_env = EDTP.objects.filter(datos_basicos__postulacion__municipio__id=municipio.id)
        itcp_env = Proyecto.objects.filter(datos_basicos__postulacion__municipio__id=municipio.id)
        context['superuser']=True
        context['municipio'] = municipio
        context['postulaciones'] = postulaciones
        context['edtp_env'] = edtp_env
        context['itcp_env'] = itcp_env
        return context