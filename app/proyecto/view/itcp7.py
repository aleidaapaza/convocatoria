import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.utils import timezone

from django.conf import settings
from django.contrib import messages

from solicitud.models import Postulacion

from proyecto.models import Riesgo_desastre
from proyecto.forms import Rg_RiesgoDesastre

class R_RiesgoDesastre(View):
    model = Riesgo_desastre
    template_name = 'Proyecto/R_RiesgoDesastre.html'
    
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if self.model.objects.filter(slug=slug).exists():
            return redirect('proyecto:actualizar_RiesgoDesastre', slug=slug)
        return self.render_form(slug)

    def render_form(self, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        form = Rg_RiesgoDesastre()
        context = {
            'form': form,
            'postulacion' : proyecto_p,
            'proyecto': proyecto_p,
            'titulo': 'ITCP-IDENTIFICACION DE POSIBLES RIESGOS DE DESASTRES',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-IDENTIFICACION DE POSIBLES RIESGOS DE DESASTRES',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse_lazy('convocatoria:Index'),
            'error_messages': []  # Inicializa una lista vacía para los mensajes de error
        }
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        riesgos = request.POST.getlist('riesgo')  # Listado de riesgos seleccionados
        niveles = request.POST.getlist('nivel')  # Listado de niveles seleccionados
        print("riesgo", riesgos)
        print("nivel", niveles)
        # Guardamos los datos en la base de datos
        for riesgo, nivel in zip(riesgos, niveles):
            # Crear un nuevo registro Riesgo_desastre por cada fila
            Riesgo_desastre.objects.create(slug=slug, riesgo=riesgo, nivel=nivel)
        return HttpResponseRedirect(reverse('proyecto:registro_DetallePOA', args=[slug,]))
    
class Act_RiesgoDesastre(View):
    model = Riesgo_desastre
    template_name = 'Proyecto/A_RiesgoDesastre.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        riesgos = Riesgo_desastre.objects.filter(slug=slug)
        if not riesgos:
            return redirect('proyecto:registro_RiesgoDesastre', slug=slug)
        form_data = riesgos
        form = Rg_RiesgoDesastre()  # No necesitamos datos en el formulario, solo los valores pre-cargados
        proyecto_p = Postulacion.objects.get(slug=slug)
        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'form': form,
            'form_data': form_data,  # Pasamos los registros existentes a la plantilla
            'slug': slug,
            'titulo': 'ITCP-IDENTIFICACION DE POSIBLES RIESGOS DE DESASTRES',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-IDENTIFICACION DE POSIBLES RIESGOS DE DESASTRES',
            'accion': 'Actualizar',
            'accion2_url': reverse_lazy('convocatoria:Index'),
            'accion2': 'Cancelar',
            'entity_registro': reverse_lazy('proyecto:registro_RiesgoDesastre_R', args=[slug]),
            'entity_registro_nom': 'Registrar',
        }
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
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        riesgos = request.POST.getlist('riesgo')
        niveles = request.POST.getlist('nivel')
        for riesgo, nivel in zip(riesgos, niveles):
            # Obtén todos los registros que coincidan
            riesgos_existentes = Riesgo_desastre.objects.filter(slug=slug, riesgo=riesgo)
            for obj in riesgos_existentes:
                obj.nivel = nivel
                obj.fecha_actualizacion = timezone.now()
                obj.save()
        messages.success(request, 'ITCP-IDENTIFICACION DE POSIBLES RIESGOS DE DESASTRES - se actualizo correctamente.')
        return redirect('proyecto:registro_DetallePOA', slug=slug)


class R_RiesgoDesastre_R(View):
    model = Riesgo_desastre
    template_name = 'Proyecto/R_RiesgoDesastre.html'
    
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        return self.render_form(slug)

    def render_form(self, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        form = Rg_RiesgoDesastre()
        context = {
            'form': form,
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'titulo': 'ITCP-IDENTIFICACION DE POSIBLES RIESGOS DE DESASTRES',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-IDENTIFICACION DE POSIBLES RIESGOS DE DESASTRES',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('proyecto:registro_RiesgoDesastre', args=[slug]),
            'error_messages': []  # Inicializa una lista vacía para los mensajes de error
        }
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        riesgos = request.POST.getlist('riesgo')
        niveles = request.POST.getlist('nivel')
        print("riesgo", riesgos)
        print("nivel", niveles)
        for riesgo, nivel in zip(riesgos, niveles):
            Riesgo_desastre.objects.create(slug=slug, riesgo=riesgo, nivel=nivel)
        return HttpResponseRedirect(reverse('proyecto:registro_RiesgoDesastre', args=[slug,]))
    
def eliminar_Riesgos(request, objetivo_id):
    if request.method == 'POST':
        objeto = Riesgo_desastre.objects.get(id=objetivo_id)
        slug = objeto.slug
        objetivo = get_object_or_404(Riesgo_desastre, id=objetivo_id)
        objetivo.delete()
        return redirect('proyecto:actualizar_RiesgoDesastre', slug=slug)
