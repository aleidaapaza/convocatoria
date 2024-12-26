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

from proyecto.models import Detalle_POA
from proyecto.forms import R_DetallePOA

class Reg_DetallePOA(CreateView):
    model = Detalle_POA
    template_name = 'Proyecto/R_DetallePOA.html'
    form_class = R_DetallePOA

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        postulacion_p = get_object_or_404(Postulacion, slug=slug)
        poa_p = Detalle_POA.objects.filter(slug=postulacion_p.slug).exists()
        print(poa_p)
        if Detalle_POA.objects.filter(slug=postulacion_p.slug).exists():
            print("REdirecionar")
            return redirect('proyecto:actualizar_DetallePOA', slug=postulacion_p.slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Reg_DetallePOA, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-DESCRIBA SI EL PROYECTO ESTA INSCRITO EN EL POA DE SU ENTIDAD Y OTROS ASPECTOS QUE SE CONSIDEREN NECESARIOS, DE ACUERDO A LAS CARACTERISTICAS Y COMPLEJIDAD DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-DESCRIBA SI EL PROYECTO ESTA INSCRITO EN EL POA DE SU ENTIDAD Y OTROS ASPECTOS QUE SE CONSIDEREN NECESARIOS, DE ACUERDO A LAS CARACTERISTICAS Y COMPLEJIDAD DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        form = self.form_class(request.POST)
        if form.is_valid():
            poa = form.save(commit=False)
            poa.slug = slug
            poa.save()
            return HttpResponseRedirect(reverse('proyecto:registro_PresupuestoRef', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
class Act_DetallePOA(UpdateView):
    model = Detalle_POA
    template_name = 'Proyecto/R_DetallePOA.html'
    form_class = R_DetallePOA

    def get_context_data(self, **kwargs):
        context = super(Act_DetallePOA, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['titulo'] = 'ITCP-DESCRIBA SI EL PROYECTO ESTA INSCRITO EN EL POA DE SU ENTIDAD Y OTROS ASPECTOS QUE SE CONSIDEREN NECESARIOS, DE ACUERDO A LAS CARACTERISTICAS Y COMPLEJIDAD DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-DESCRIBA SI EL PROYECTO ESTA INSCRITO EN EL POA DE SU ENTIDAD Y OTROS ASPECTOS QUE SE CONSIDEREN NECESARIOS, DE ACUERDO A LAS CARACTERISTICAS Y COMPLEJIDAD DEL PROYECTO'
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
            messages.success(request, 'ITCP-DESCRIBA SI EL PROYECTO ESTA INSCRITO EN EL POA DE SU ENTIDAD Y OTROS ASPECTOS QUE SE CONSIDEREN NECESARIOS, DE ACUERDO A LAS CARACTERISTICAS Y COMPLEJIDAD DEL PROYECTO - se actualizo correctamente.')
            return redirect('proyecto:registro_PresupuestoRef', slug=slug) 
        else:
            return self.render_to_response(self.get_context_data(form=form))
