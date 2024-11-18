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

from proyecto.models import Conclusion_recomendacion
from proyecto.forms import R_ConclusionRecomen

class Reg_ConclRec(CreateView):
    model = Conclusion_recomendacion
    template_name = 'Proyecto/R_DetallePOA.html'
    form_class = R_ConclusionRecomen

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        postulacion_p = get_object_or_404(Postulacion, slug=slug)
        poa_p = self.model.objects.filter(slug=postulacion_p.slug).exists()
        print(poa_p)
        if self.model.objects.filter(slug=postulacion_p.slug).exists():
            print("REdirecionar")
            return redirect('proyecto:actualizar_ConclRec', slug=postulacion_p.slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Reg_ConclRec, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-CONCLUSIONES Y RECOMENDACIONES'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-CONCLUSIONES Y RECOMENDACIONES'
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
            return HttpResponseRedirect(reverse('proyecto:registro_DeclaracionJurada', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
class Act_ConclRec(UpdateView):
    model = Conclusion_recomendacion
    template_name = 'Proyecto/R_DetallePOA.html'
    form_class = R_ConclusionRecomen

    def get_context_data(self, **kwargs):
        context = super(Act_ConclRec, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['titulo'] = 'ITCP-CONCLUSIONES Y RECOMENDACIONES'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-CONCLUSIONES Y RECOMENDACIONES'
        context['accion'] = 'Actualizar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
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
            return HttpResponseRedirect(reverse('proyecto:actualizar_ConclRec', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))
