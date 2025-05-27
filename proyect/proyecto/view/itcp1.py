import os
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils import timezone

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
        context['postulacion'] = proyecto_p
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
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = Postulacion.objects.get(slug=slug)
        datos_proy = DatosProyectoBase.objects.get(slug=postulacion_pr.slug)
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.fecha_actualizacion = timezone.now()
            datos.save()
            postulacion_pr.datos_proyecto = datos_proy
            postulacion_pr.save()
            messages.success(request, 'DATOS PRINCIPALES DEL PROYECTO - se actualizo correctamente.')
            if postulacion_pr.tipo_financiamiento == 1:
                return redirect('proyecto:registro_justificacion', slug=slug)
            else:
                return redirect('proyecto:registro_ObjetivoGeneral', slug=slug)
        else:
            messages.error(request, 'Hubo un error al actualizar los datos.')
            return self.render_to_response(self.get_context_data(form=form))
        
