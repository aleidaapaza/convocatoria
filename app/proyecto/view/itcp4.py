import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.utils import timezone
from django.contrib import messages

from django.conf import settings

from solicitud.models import Postulacion

from proyecto.models import Modelo_Acta

class R_Modelo_Acta(View):
    model=Modelo_Acta
    template_name = 'Proyecto/R_Modelo_acta01.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        if self.model.objects.filter(slug=slug).exists():
            print('redireccionando')
            return redirect('proyecto:actualizar_ModeloActa', slug=slug)
        else:
            context = {
                'proyecto': proyecto_p,
                'postulacion' : proyecto_p,
                'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'accion': ' Registrar',
                'accion2': 'Cancelar',
                'accion2_url': reverse_lazy('convocatoria:Index'),
                'error_messages': []  # Inicializa una lista vacía para los mensajes de error
            }
            return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        comunidades_list = []
        si_acta_files = []
        no_acta_texts = []
        error_messages = []

        index = 0

        while True:
            comunidad = request.POST.get(f'comunidades_{index}')
            si_acta = request.FILES.get(f'si_acta_{index}')
            no_acta = request.POST.get(f'no_acta_{index}')
            
            if comunidad is None:
                break
            comunidades_list.append(comunidad)
            si_acta_files.append(si_acta)
            no_acta_texts.append(no_acta)            
            index += 1
            
        for si_acta in si_acta_files:
            if si_acta:
                if si_acta.size > 2 * 1024 * 1024:
                    error_messages.append('El archivo no debe superar los 2 MB.')
                if not si_acta.name.endswith('.pdf'):
                    error_messages.append('El archivo debe ser en formato PDF.')
                
        if error_messages:
            context = {
                'proyecto': get_object_or_404(Postulacion, slug=slug),
                'postulacion' : get_object_or_404(Postulacion, slug=slug),
                'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'accion': 'Actualizar',
                'accion2': 'Cancelar',
                'accion2_url': reverse_lazy('convocatoria:Index'),
                'error_messages': error_messages,
            }
            return render(request, self.template_name, context)

        for i in range(len(comunidades_list)):
            comunidad = comunidades_list[i]
            si_acta = si_acta_files[i]
            no_acta = no_acta_texts[i]
            if comunidad:
                Modelo_Acta.objects.create(
                    slug=slug,
                    comunidades=comunidad,
                    si_acta=si_acta if si_acta else None,
                    no_acta=no_acta if not si_acta else no_acta
                )
        return HttpResponseRedirect(reverse('proyecto:registro_DerechoPropietario', args=[slug]))
    
class A_Modelo_Acta(View):
    template_name = 'Proyecto/A_Modelo_acta01.html'

    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = Modelo_Acta.objects.filter(slug=slug) # Formulario vacío para nuevos objetivos
        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'modelo_acta': objetivos,
            'titulo': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'entity_registro': reverse_lazy('proyecto:registro_ModeloActa01', args=[slug]),
            'entity_registro_nom': 'Registrar',
            'error_messages': [],

        }
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
        return render(request, self.template_name, context)
     
    def post(self, request, slug):
        id_list = []
        comunidades_list = []
        si_acta_files = []
        no_acta_texts = []
        error_messages = []
        index = 0        
        while True:            
            idn = self.request.POST.get(f'idn_{index}')
            comunidad = request.POST.get(f'comunidades_{index}')
            si_acta = request.FILES.get(f'si_acta_{index}')
            no_acta = request.POST.get(f'no_acta_{index}')
            if comunidad is None:
                break
            id_list.append(idn)
            comunidades_list.append(comunidad)
            si_acta_files.append(si_acta)
            no_acta_texts.append(no_acta)        
            index += 1
            if si_acta:
                if si_acta.size > 2 * 1024 * 1024:  # 2 MB
                    error_messages.append('El archivo no debe superar los 2 MB.')
                if not si_acta.name.endswith('.pdf'):
                    error_messages.append('El archivo debe ser en formato PDF.')
            else:
                continue
        
        if error_messages:
            proyecto_p = get_object_or_404(Postulacion, slug=slug)
            objetivos = Modelo_Acta.objects.filter(slug=slug)
            context = {
                'proyecto': proyecto_p,
                'postulacion' : proyecto_p,
                'modelo_acta': objetivos,
                'titulo': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'accion': 'Actualizar',
                'accion2': 'Cancelar',
                'accion2_url': reverse('convocatoria:Index'),
                'entity_registro': reverse_lazy('proyecto:registro_ModeloActa01', args=[slug]),
                'entity_registro_nom': 'Registrar',
                'error_messages': error_messages,  # Pasa los mensajes de error
            }
            return render(request, self.template_name, context)
        
        for i in range(len(id_list)):            
            idn = id_list[i]
            comunidad = comunidades_list[i]
            si_acta = si_acta_files[i]
            no_acta = no_acta_texts[i]
            if Modelo_Acta.objects.filter(id=idn).exists():
                acta = Modelo_Acta.objects.get(id=idn)
                acta.comunidades = comunidad
                acta.si_acta = si_acta if si_acta else acta.si_acta
                acta.no_acta = no_acta if no_acta else acta.no_acta
                acta.fecha_actualizacion = timezone.now()
                acta.save()
            else:
                Modelo_Acta.objects.create(
                    slug = slug,
                    fecha_registro = timezone.now(),
                    fecha_actualizacion = timezone.now(),
                    comunidades = comunidad,
                    si_acta = si_acta,
                    no_acta = no_acta,
                )
        messages.success(request, 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO - se actualizo correctamente.')
        return redirect('proyecto:registro_DerechoPropietario', slug=slug)                
    
def descargar_archivo(request, slug, id):
    documento = Modelo_Acta.objects.get(id=id)
    response = HttpResponse(documento.si_acta, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{documento.si_acta.name}"'
    return response

def eliminar_ModeloActa(request, objetivo_id):
    if request.method == 'POST':
        objeto = Modelo_Acta.objects.get(id=objetivo_id)
        slug = objeto.slug
        objetivo = get_object_or_404(Modelo_Acta, id=objetivo_id)
        objetivo.delete()
        return redirect('proyecto:actualizar_ModeloActa', slug=slug)
    
class R_Modelo_Acta_R(View):
    template_name = 'Proyecto/R_Modelo_acta01.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'accion': 'Añadir',
            'accion2': 'Cancelar',
            'accion2_url': reverse('proyecto:actualizar_ModeloActa', args=[slug]),
            'error_messages': []  # Inicializa una lista vacía para los mensajes de error
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        comunidades_list = []
        si_acta_files = []
        no_acta_texts = []
        error_messages = []
        index = 0
        while True:
            comunidad = request.POST.get(f'comunidades_{index}')
            si_acta = request.FILES.get(f'si_acta_{index}')
            no_acta = request.POST.get(f'no_acta_{index}')
            if comunidad is None:
                break  # Salir del bucle si no hay más comunidades
            comunidades_list.append(comunidad)
            si_acta_files.append(si_acta)
            no_acta_texts.append(no_acta)
            index += 1
            if si_acta:
                if si_acta.size > 2 * 1024 * 1024:  # 2 MB
                    error_messages.append('El archivo no debe superar los 2 MB.')
                if not si_acta.name.endswith('.pdf'):
                    error_messages.append('El archivo debe ser en formato PDF.')
            else:
                continue
        if error_messages:
            context = {
                'proyecto': get_object_or_404(Postulacion, slug=slug),
                'postulacion' : get_object_or_404(Postulacion, slug=slug),
                'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'accion': 'Registrar',
                'accion2': 'Cancelar',
                'accion2_url': reverse_lazy('convocatoria:actualizar_ModeloActa', args=[slug]),
                'error_messages': error_messages,  # Pasa los mensajes de error
            }
            return render(request, self.template_name, context)

        for i in range(len(comunidades_list)):
            comunidad = comunidades_list[i]
            si_acta = si_acta_files[i]
            no_acta = no_acta_texts[i]
            if comunidad:
                Modelo_Acta.objects.create(
                    slug=slug,
                    comunidades=comunidad,
                    si_acta=si_acta if si_acta else None,
                    no_acta=no_acta if not si_acta else no_acta
                )
        return HttpResponseRedirect(reverse('proyecto:actualizar_ModeloActa', args=[slug]))
