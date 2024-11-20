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
        
        # Asegúrate de que el formulario sea correcto
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        
        # Obtener el objeto Postulacion relacionado
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'DATOS PRINCIPALES DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'DATOS PRINCIPALES DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        return context

    def post(self, request, *args, **kwargs):
        # Obtén el objeto relacionado con el modelo principal (DatosProyectoBase)
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        
        # Obtener la instancia de Postulacion relacionada
        postulacion_pr = Postulacion.objects.get(slug=slug)
        
        # Crear el formulario con los datos POST
        form = self.form_class(request.POST, instance=self.object)
        
        # Verifica si el formulario es válido
        if form.is_valid():
            print('Formulario validado')

            # Guarda la instancia de DatosProyectoBase
            datos = form.save(commit=False)
            datos.fecha_actualizacion = timezone.now()

            # Si necesitas asociar la postulacion al objeto de DatosProyectoBase
            datos.postulacion = postulacion_pr
            
            # Guarda los datos
            datos.save()

            # Redirige a la siguiente vista (por ejemplo, registro_justificacion)
            return HttpResponseRedirect(reverse('proyecto:registro_justificacion', args=[postulacion_pr.slug]))
        else:
            # Si el formulario no es válido, muestra los errores
            print(form.errors)
            
            # Renderiza de nuevo la página con el formulario y sus errores
            return self.render_to_response(self.get_context_data(form=form))