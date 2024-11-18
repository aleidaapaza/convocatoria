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
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = Postulacion.objects.get(slug=slug)        
        form = self.form_class(request.POST, instance = postulacion_pr)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.fecha_actualizacion = timezone.now()
            datos.save()
            return HttpResponseRedirect(reverse('proyecto:registro_justificacion', args=[postulacion_pr.slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))