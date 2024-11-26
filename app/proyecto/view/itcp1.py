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
from proyecto.models import DatosProyectoBase
from proyecto.forms import Reg_DatosBase


class RegistroDatosBasicos(UpdateView):
    model = DatosProyectoBase
    template_name = 'Proyecto/R_DatosProyecto.html'
    form_class = Reg_DatosBase

    def get_context_data(self, **kwargs):
        context = super(RegistroDatosBasicos, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'DATOS PRINCIPALES DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'DATOS PRINCIPALES DEL PROYECTO'
        context['accion'] = 'Registrar'
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
        # Definir la URL de siguiente paso
        context['next_url'] = reverse('proyecto:registro_justificacion', args=[slug])
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = Postulacion.objects.get(slug=slug)
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            print('Formulario validado')
            datos = form.save(commit=False)
            datos.fecha_actualizacion = timezone.now()
            datos.save()
            postulacion_pr.datos_proyecto = slug
            postulacion_pr.save()
            # Agregar mensaje de éxito al contexto
            messages.success(request, 'Los datos se actualizaron correctamente.')
            return redirect('proyecto:registro_Base', slug=slug)
        else:
            messages.error(request, 'Hubo un error al actualizar los datos.')

            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))
        
