from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count, Q
from datetime import datetime

from solicitud.models import Postulacion
from user.models import Revisor, SuperUser, User

from convocatoria.models import Convocatoria
from convocatoria.forms import R_Convocatoria, A_Convocatoria

from proyecto.models import (DatosProyectoBase, Justificacion, Idea_Proyecto,
                             Objetivo_especifico, Beneficiario, Modelo_Acta,
                             Derecho_propietario, Impacto_ambiental, Riesgo_desastre,
                             Detalle_POA, Conclusion_recomendacion, Declaracion_jurada,
                             PresupuestoReferencial, Proyecto)
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
        form = self.form_class(request.POST)
        if form.is_valid():
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
            context['form'] = self.form_class(self.request.GET)
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
        form = self.form_class(request.POST, instance = objeto)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('convocatoria:Actualizar_convocatoria', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ListaConvocatoria(ListView):
    model = Convocatoria
    template_name = 'convocatoria/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA DE CONVOCATORIA'
        context['activate'] = True
        context['entity'] = 'LISTA DE CONVOCATORIA'
        context['object_list'] = self.model.objects.all()
        estado = self.model.objects.filter(estado=True).count()
        if estado > 0:
            context['error'] = 'REGISTRAR CONVOCATORIA'
            context['message'] = 'Existe una convocatoria vigente actualmente, para registrar otra convocatoria se necesita que las anteriores no esten activas'
        else:
            context['entity_registro'] = reverse_lazy('convocatoria:registro_convocatoria')
            context['entity_registro_nom'] = 'REGISTRAR CONVOCATORIA'
        return context
    
class Index(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.is_municipio:
                context['titulo'] = 'AVANCE DEL REGISTRO'
                user_sl = self.request.user.username_proyecto.slug
                print(user_sl)
                context['slug']=user_sl
                postulacion_p = Postulacion.objects.get(slug =user_sl)
                context['proyecto'] = postulacion_p
                context['postulacion'] = postulacion_p
                context['datosProyecto'] = DatosProyectoBase.objects.filter(slug=user_sl).count()
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
                context['beneficiario'] = Beneficiario.objects.filter(slug=user_sl).count()
                context['modeloActa'] = Modelo_Acta.objects.filter(slug=user_sl).count()
                context['DerechoPropie'] = Derecho_propietario.objects.filter(slug=user_sl).count()
                context['impactoAmbiental'] = Impacto_ambiental.objects.filter(slug=user_sl).count()
                context['riesgoDesastre'] = Riesgo_desastre.objects.filter(slug=user_sl).count()
                context['detallePoa'] = Detalle_POA.objects.filter(slug=user_sl).count()
                context['conclusion'] = Conclusion_recomendacion.objects.filter(slug=user_sl).count()
                context['declaracion'] = Declaracion_jurada.objects.filter(slug=user_sl).count()
                context['Presupuesto'] = PresupuestoReferencial.objects.filter(slug=user_sl).count()
                if Proyecto.objects.filter(slug=user_sl).exists():
                    print(Proyecto.objects.filter(slug=user_sl).exists)
                    context['vista'] = True
                else:
                    context['vista'] = False
            elif self.request.user.is_revisor:
                user_sl = self.request.user.revisor_perfil.slug
                context['slug']=user_sl
                print(user_sl)
                postulacion_p = Revisor.objects.get(slug = user_sl)
                print(postulacion_p)
                context['postulacion'] = postulacion_p
            elif self.request.user.is_superuser:
                user_sl = self.request.user.superuser_perfil.slug
                context['slug']=user_sl
                postulacion_p = SuperUser.objects.get(slug = user_sl)
                context['postulacion'] = postulacion_p
                convocatorias = Convocatoria.objects.annotate(
                    num_true=Count('postulacion_convocatoria', filter=Q(postulacion_convocatoria__estado=True)),
                    num_false=Count('postulacion_convocatoria', filter=Q(postulacion_convocatoria__estado=False)),
                    num_none=Count('postulacion_convocatoria', filter=Q(postulacion_convocatoria__estado=None)),
                    num_total=Count('postulacion_convocatoria')
                )
                context['convocatoria'] = convocatorias
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
                elif fechalanzamiento >= fechaHoy:
                    context['fechaActivo'] = False
                    context['fecha_expiracion'] = fechalanzamiento.isoformat() if fechalanzamiento else None
                    context['message_fecha'] = 'ESPERANDO LA APERTURA DE LA CONVOCATORIA ACTUAL'   
                    context['estadotemporal']='LANZAMIENTO'
                    context['imagen'] = 'img/fondo/esperando.png'
                elif fechaCierre < fechaHoy:
                    context['fechaActivo'] = False
                    context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
                    context['message_fecha'] = 'SE CERRO LA CONVOCATORIA ACTUAL' 
                    context['estadotemporal']='CIERRE'
                    context['imagen'] = 'img/fondo/cierre.png'
            elif estado > 0:
                context['activo'] = False
                context['message'] = 'Se tiene mas de dos convocatorias activas por favor contactese con el encargado para reportar este error'
                context['conteo'] = estado
                context['imagen'] = 'img/fondo/problema.png'
            elif estado == 0:
                context['activo'] = False
                context['message'] = 'No se tiene una convocatoria vigente por el momento.'
                context['conteo'] = estado
                context['imagen'] = 'img/fondo/esperando.png'
        return context
