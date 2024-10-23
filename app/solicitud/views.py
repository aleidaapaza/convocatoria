from django.shortcuts import render

# Create your views here.

from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.views.generic import CreateView, ListView
from solicitud.models import Municipios

class solicitud(TemplateView):
    template_name = 'index.html'

class entidad(TemplateView):
    template_name = 'homepage/entidadTerritorial.html'
    def get_context_data(self, **kwargs):
        context = super(entidad, self).get_context_data(**kwargs)
        departamento = self.kwargs.get('departamento', 0)
        context['dep'] = departamento
        context['entity'] = 'ENTIDAD TERRITORIAL'
        return context

class municipio(ListView):
    model = Municipios
    template_name = 'homepage/municipio.html'

    def get_context_data(self, **kwargs):
        context = super(municipio, self).get_context_data(**kwargs)
        departamento = self.kwargs.get('departamento', 0)
        entidad = self.kwargs.get('entidad',0)
        municipios_f = model.
        context['dep'] = departamento
        context['ent'] = entidad
        
        context['entity'] = 'ENTIDAD TERRITORIAL'
        return context
