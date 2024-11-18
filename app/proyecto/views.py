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

from proyecto.models import Proyecto

class Lista_Proyectos(ListView):
    model = Postulacion
    template_name = 'Proyecto/lista.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_Proyectos, self).get_context_data(**kwargs)
        proyectos = self.model.objects.filter(estado=True)
        context['titulo'] = 'LISTA DE PROYECTOS CON INICIO DE SESION'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS CON INICIO DE SESION'
        context['object_list'] = proyectos
        return context
    
class Reg_Proyecto(View):
    model = Proyecto