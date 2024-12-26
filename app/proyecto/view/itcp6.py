import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.utils import timezone
from solicitud.models import Postulacion
from django.contrib import messages

from proyecto.models import Impacto_ambiental
from proyecto.forms import R_Impacto_Ambiental

class Reg_ImpactoAmbiental(CreateView):
    model=Impacto_ambiental
    template_name = 'Proyecto/R_ImpactoAmbiental.html'
    form_class = R_Impacto_Ambiental

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if Impacto_ambiental.objects.filter(slug=slug).exists():
            return redirect('proyecto:actualizar_ImpactoAmbiental', slug=slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Reg_ImpactoAmbiental, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-IDENTIFICACION DE POSIBLES IMPACTOS AMBIENTALES'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-IDENTIFICACION DE POSIBLES IMPACTOS AMBIENTALES'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        form = self.form_class(request.POST)
        if form.is_valid():
            dato = form.save(commit=False)
            dato.slug = slug
            dato.save()
            return HttpResponseRedirect(reverse('proyecto:registro_RiesgoDesastre', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Act_ImpactoAmbiental(UpdateView):
    model=Impacto_ambiental
    template_name = 'Proyecto/R_ImpactoAmbiental.html'
    form_class = R_Impacto_Ambiental

    def get_context_data(self, **kwargs):
        context = super(Act_ImpactoAmbiental, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['titulo'] = 'ITCP-IDENTIFICACION DE POSIBLES IMPACTOS AMBIENTALES'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-IDENTIFICACION DE POSIBLES IMPACTOS AMBIENTALES'
        context['accion'] = 'Actualizar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
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
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        objeto = self.model.objects.get(slug=slug)     
        form = self.form_class(request.POST, instance = objeto)
        if form.is_valid():
            print("valido")
            datos = form.save(commit=False)
            datos.fecha_actualizacion = timezone.now()
            datos.save()
            messages.success(request, 'ITCP-IDENTIFICACION DE POSIBLES IMPACTOS AMBIENTALES - se actualizo correctamente.')
            return redirect('proyecto:registro_RiesgoDesastre', slug=slug)
        else:
            return self.render_to_response(self.get_context_data(form=form))

