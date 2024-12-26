from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.utils import timezone
from django.contrib import messages

from solicitud.models import Postulacion

from proyecto.models import Justificacion
from proyecto.forms import Reg_Justificacion


class Reg_Justificaciones(CreateView):
    model=Justificacion
    template_name = 'Proyecto/R_Justificacion.html'
    form_class = Reg_Justificacion

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        postulacion_p = get_object_or_404(Postulacion, slug=slug)
        
        if self.model.objects.filter(slug=postulacion_p.slug).exists():
            return redirect('proyecto:actualizar_justificacion', slug=postulacion_p.slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Reg_Justificaciones, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        form = self.form_class(request.POST)
        if form.is_valid():
            justificacion = form.save(commit=False)
            justificacion.slug = slug
            justificacion.save()
            return HttpResponseRedirect(reverse('proyecto:registro_Idea_proyecto', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Act_Justificacion(UpdateView):
    model = Justificacion
    template_name = 'Proyecto/R_Justificacion.html'
    form_class = Reg_Justificacion

    def get_context_data(self, **kwargs):
        context = super(Act_Justificacion, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
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
        # Definir la URL de siguiente paso
        context['next_url'] = reverse('proyecto:registro_Idea_proyecto', args=[slug])
        
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
            messages.success(request, 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO - se actualizo correctamente.')
            return redirect('proyecto:registro_Idea_proyecto', slug=slug)        
        else:
            messages.error(request, 'Hubo un error al actualizar los datos.')
            return self.render_to_response(self.get_context_data(form=form))
