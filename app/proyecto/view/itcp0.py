import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.utils import timezone

from django.conf import settings
from django.contrib import messages

from solicitud.models import Postulacion
from proyecto.models import DatosProyectoBase
from proyecto.forms import Reg_DatosBase

class DatosPostulacion(TemplateView):
    template_name = 'perfil/municipio.html'
    def get_context_data(self, **kwargs):
        context = super(DatosPostulacion, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.is_municipio:
                user_sl = self.request.user.username_proyecto.slug
                context['slug']=user_sl
                print(user_sl)
                postulacion_p = Postulacion.objects.get(slug =user_sl)
                print(postulacion_p)
                context['proyecto'] = postulacion_p
                context['postulacion'] = postulacion_p
        return context
