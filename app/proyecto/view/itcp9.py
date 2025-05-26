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

from proyecto.models import PresupuestoReferencial

class Reg_PresupuestoRef(View):
    model = PresupuestoReferencial
    template_name = 'Proyecto/R_PresupuestoRefer.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if self.model.objects.filter(slug=slug).exists():
            print('redireccionando')
            return redirect('proyecto:actualizar_PresupuestoRef', slug=slug)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        if proyecto_p.tipo_financiamiento == 1:
            titulo = "ITCP-PRESUPUESTO REFERENCIAL"
        else:
            titulo = "PRESUPUESTO REFERENCIAL"

        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'titulo': titulo,
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': titulo,
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'error_messages': []
        }
        return render(request, self.template_name, context)

    def render_form(self, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        if proyecto_p.tipo_financiamiento == 1:
            titulo = "ITCP-PRESUPUESTO REFERENCIAL"
        else:
            titulo = "PRESUPUESTO REFERENCIAL"
        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'titulo': titulo,
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': titulo,
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'error_messages': []
        }
        return render(self.request, self.template_name, context)

    def post(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        error_messages = []
        if proyecto_p.tipo_financiamiento == 1:
            elabSolicBs = float(request.POST.get('elabSolicBs', 0))
        else:
            elabSolicBs = 1
        ejecFonaBs = float(request.POST.get('ejecFonaBs', 0))
        ejecSolicBs = float(request.POST.get('ejecSolicBs', 0))
        
        if elabSolicBs != 0.00 and ejecFonaBs != 0.00 and ejecSolicBs != 0.00:
            ejecTotalBs = ejecFonaBs + ejecSolicBs
            ejecFonaPor = round((ejecFonaBs * 100) / ejecTotalBs, 2)
            ejecSolicPor = round((ejecSolicBs * 100) / ejecTotalBs, 2)
            
            if ejecFonaPor > 70.00 or ejecSolicPor < 30.00:
                error_messages.append(f'El porcentaje de la ejecucion del EDTP por parte del FONABOSQUE supera el 70%: {ejecFonaPor:.2f}% y por parte del SOLICITANTE es menor al 30%: {ejecSolicPor :.2f}%')                
                if error_messages:
                    if proyecto_p.tipo_financiamiento == 1:
                        titulo = "ITCP-PRESUPUESTO REFERENCIAL"
                    else:
                        titulo = "PRESUPUESTO REFERENCIAL"
                    context = {
                        'proyecto': proyecto_p,
                        'postulacion' : proyecto_p,
                        'titulo': titulo,
                        'entity': 'REGISTRO DATOS DEL PROYECTO',
                        'entity2': titulo,
                        'accion': 'Actualizar',
                        'accion2': 'Cancelar',
                        'accion2_url': reverse('convocatoria:Index'),
                        'error_messages': error_messages,
                    }
                    return render(request, self.template_name, context)
        
        # Lógica de creación de objetos si no hay error
        if proyecto_p.tipo_financiamiento == 1:
            elab_sol = request.POST.get('elabSolicBs', '').replace(',', '.')
            elab_fona = request.POST.get('elabFonaBs', '').replace(',', '.')
            elab_total = request.POST.get('elabTotalBs', '').replace(',', '.')
            elab_fona_p = request.POST.get('elabFonaPor', '').replace(',', '.')
            elab_sol_p = request.POST.get('elabSolicPor', '').replace(',', '.')
            elab_total_p = request.POST.get('elabTotalPor', '').replace(',', '.')
        ejec_fona = request.POST.get('ejecFonaBs', '').replace(',', '.')
        ejec_sol = request.POST.get('ejecSolicBs', '').replace(',', '.')
        ejec_total = request.POST.get('ejecTotalBs', '').replace(',', '.')
        ejec_fona_p = request.POST.get('ejecFonaPor', '').replace(',', '.')
        ejec_sol_p = request.POST.get('ejecSolicPor', '').replace(',', '.')
        ejec_total_p = request.POST.get('ejecTotalPor', '').replace(',', '.')

        if proyecto_p.tipo_financiamiento == 1:
            self.model.objects.create(
                slug=slug,
                elab_sol=float(elab_sol),
                elab_fona=float(elab_fona),
                elab_total=float(elab_total),
                elab_fona_p=float(elab_fona_p),
                elab_sol_p=float(elab_sol_p),
                elab_total_p=float(elab_total_p),
                ejec_fona=float(ejec_fona),
                ejec_sol=float(ejec_sol),
                ejec_total=float(ejec_total),
                ejec_fona_p=float(ejec_fona_p),
                ejec_sol_p=float(ejec_sol_p),
                ejec_total_p=float(ejec_total_p),
            )
        else:
            self.model.objects.create(
                slug=slug,
                elab_sol=float(0),
                elab_fona=float(0),
                elab_total=float(0),
                elab_fona_p=float(0),
                elab_sol_p=float(0),
                elab_total_p=float(0),
                ejec_fona=float(ejec_fona),
                ejec_sol=float(ejec_sol),
                ejec_total=float(ejec_total),
                ejec_fona_p=float(ejec_fona_p),
                ejec_sol_p=float(ejec_sol_p),
                ejec_total_p=float(ejec_total_p),
            )
        if proyecto_p.tipo_financiamiento == 1:
            return redirect('proyecto:registro_ConclRec', slug=slug)
        else:
            return redirect('proyecto:registro_DeclaracionJurada', slug=slug)
            

class Act_PresupuestoRef(View):
    model = PresupuestoReferencial
    template_name = 'Proyecto/A_PresupuestoRefer.html'

    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = self.model.objects.get(slug=slug)
        if proyecto_p.tipo_financiamiento == 1:
            titulo = "ITCP-PRESUPUESTO REFERENCIAL"
        else:
            titulo = "PRESUPUESTO REFERENCIAL"
        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'objetivo': objetivos,
            'titulo': titulo,
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': titulo,
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'error_messages': []
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
        error_messages = []
        objetivos = self.model.objects.get(slug=slug)
        print(objetivos.elab_sol, 'en el post')
        proyecto_p = get_object_or_404(Postulacion, slug=slug)

        # Función para convertir de manera segura a float
        def safe_float(value, default_value):
            # Si el valor está vacío o es None, retornar el valor predeterminado
            if not value or value.strip() == '':
                return default_value
            # Si no está vacío, reemplazar ',' por '.' y convertir a float
            return float(value.replace(',', '.'))
        if proyecto_p.tipo_financiamiento == 1:
            elabSolicBs = safe_float(request.POST.get('elabSolicBs', objetivos.elab_sol), objetivos.elab_sol)
            elabFonaBs = safe_float(request.POST.get('elabFonaBs', objetivos.elab_fona), objetivos.elab_fona)
            elabTotalBs = safe_float(request.POST.get('elabTotalBs', objetivos.elab_total), objetivos.elab_total)
            elabFonaPor = safe_float(request.POST.get('elabFonaPor', objetivos.elab_fona_p), objetivos.elab_fona_p)
            elabSolicPor = safe_float(request.POST.get('elabSolicPor', objetivos.elab_sol_p), objetivos.elab_sol_p)
            elabTotalPor = safe_float(request.POST.get('elabTotalPor', objetivos.elab_total_p), objetivos.elab_total_p)
        ejecFonaBs = safe_float(request.POST.get('ejecFonaBs', objetivos.ejec_fona), objetivos.ejec_fona)
        ejecSolicBs = safe_float(request.POST.get('ejecSolicBs', objetivos.ejec_sol), objetivos.ejec_sol)
        ejecTotalBs = safe_float(request.POST.get('ejecTotalBs', objetivos.ejec_total), objetivos.ejec_total)
        ejecFonaPor = safe_float(request.POST.get('ejecFonaPor', objetivos.ejec_fona_p), objetivos.ejec_fona_p)
        ejecSolicPor = safe_float(request.POST.get('ejecSolicPor', objetivos.ejec_sol_p), objetivos.ejec_sol_p)
        ejecTotalPor = safe_float(request.POST.get('ejecTotalPor', objetivos.ejec_total_p), objetivos.ejec_total_p)

        if proyecto_p.tipo_financiamiento == 1:
            elabSolicBs = float(request.POST.get('elabSolicBs', 0))
        else:
            elabSolicBs = 1

        if elabSolicBs != 0.00 and ejecFonaBs != 0.00 and ejecSolicBs != 0.00:
            if objetivos.ejec_fona == ejecFonaBs and objetivos.elab_sol ==elabSolicBs and objetivos.ejec_sol == ejecSolicBs:
                print('sin modificaciones')
                messages.success(request, 'ITCP-PRESUPUESTO REFERENCIAL - se actualizó correctamente.')
                return redirect('proyecto:registro_ConclRec', slug=slug)            
            else:
                if proyecto_p.tipo_financiamiento == 1:
                    objetivos.elab_sol = elabSolicBs
                    objetivos.elab_fona = elabFonaBs
                    objetivos.elab_total = elabTotalBs
                    objetivos.elab_fona_p = elabFonaPor
                    objetivos.elab_sol_p = elabSolicPor
                    objetivos.elab_total_p = elabTotalPor
                    
                objetivos.ejec_fona = ejecFonaBs 
                objetivos.ejec_sol = ejecSolicBs
                objetivos.ejec_total = ejecTotalBs
                objetivos.ejec_fona_p = ejecFonaPor
                objetivos.ejec_sol_p = ejecSolicPor
                objetivos.ejec_total_p = ejecTotalPor
                objetivos.fecha_actualizacion = timezone.now()
                objetivos.save()
                proyecto_p = get_object_or_404(Postulacion, slug=slug)
                objetivos = self.model.objects.get(slug=slug)
                if proyecto_p.tipo_financiamiento == 1:
                    messages.success(request, 'ITCP-PRESUPUESTO REFERENCIAL - se actualizó correctamente.')
                    return redirect('proyecto:registro_ConclRec', slug=slug)
                else:
                    messages.success(request, 'PRESUPUESTO REFERENCIAL - se actualizó correctamente.')
                    return redirect('proyecto:registro_DeclaracionJurada', slug=slug)