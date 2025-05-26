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

from proyecto.models import Declaracion_jurada
from proyecto.forms import R_Declaracion_ITCP, R_Declaracion_juradaTotal

class Act_DeclaracionJurada(UpdateView):
    model = Declaracion_jurada
    template_name = 'Proyecto/R_DeclaracionJurada_02.html'
    form_class = R_Declaracion_juradaTotal

    def get_context_data(self, **kwargs):
        context = super(Act_DeclaracionJurada, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        objeto = self.model.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['postulacion'] = proyecto_p
        context['objeto'] = objeto  
        context['titulo'] = 'ITCP-DECLARACION JURADA'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-DECLARACION JURADA'
        context['accion'] = 'Actualizar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        objeto = self.model.objects.get(slug=slug)     
        form = self.form_class(request.POST, instance = objeto)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)

        if form.is_valid():
            print("valido")
            declaracion_d = form.cleaned_data.get('declaracion')
            itcp_d = form.cleaned_data.get('itcp')
            carta_ejec = form.cleaned_data.get('carta_ejec')

           # Validación del tamaño de los archivos
            if declaracion_d and declaracion_d.size > 2 * 1024 * 1024:  # 2 MB
                messages.error(request, 'El archivo DECLARACION JURADA no debe superar los 2 MB.')            
            print(proyecto_p.convocatoria.tamanoDoc)
            tamano_maximo = int(proyecto_p.convocatoria.tamanoDoc)
            print(tamano_maximo)
            if itcp_d and itcp_d.size > tamano_maximo * 1024 * 1024:  # Tamaño máximo en MB
                messages.error(request, 'El archivo ITCP no debe superar los ' + str(proyecto_p.convocatoria.tamanoDoc) + ' MB')

            if carta_ejec and carta_ejec.size > 2 * 1024 * 1024:  # 2 MB
                messages.error(request, 'El archivo CARTA DE SOLICITUD PARA LA EJECUCION DEL EDTP no debe superar los 2 MB.')
            
            if proyecto_p.tipo_financiamiento == 1:
                carta_elab = form.cleaned_data.get('carta_elab')
                if carta_elab and carta_elab.size > 2 * 1024 * 1024:  # 2 MB
                    messages.error(request, 'El CARTA DE SOLICITUD PARA LA ELABORACION DEL EDTP no debe superar los 2 MB.')
            
            # Si hay errores, volvemos a renderizar la página con los errores
            if messages.get_messages(request):
                return self.render_to_response(self.get_context_data(form=form))

            datos = form.save(commit=False)
            datos.fecha_actualizacion = timezone.now()
            datos.save()
            return HttpResponseRedirect(reverse('proyecto:actualizar_DeclaracionJurada', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

def descargar_docDeclaracion(request, slug, num):
    documento = get_object_or_404(Declaracion_jurada, slug=slug)
    if num == 1:
        response = HttpResponse(documento.declaracion, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{documento.declaracion.name}"'
    elif num == 2:
        response = HttpResponse(documento.itcp, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{documento.itcp.name}"'
    elif num == 3:
        response = HttpResponse(documento.carta_elab, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{documento.carta_elab.name}"'
    elif num == 4:
        response = HttpResponse(documento.carta_ejec, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{documento.carta_ejec.name}"'
    
    return response