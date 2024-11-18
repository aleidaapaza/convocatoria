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
from proyecto.forms import R_PresupuestoReferencial

class Reg_PresupuestoRef(View):
    model = PresupuestoReferencial
    template_name = 'Proyecto/R_PresupuestoRefer.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if self.model.objects.filter(slug=slug).exists():
            print('redireccionando')
            return redirect('proyecto:actualizar_PresupuestoRef', slug=slug)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = self.model.objects.filter(slug=slug)
        context = {
            'proyecto': proyecto_p,
            'objetivos_esp': objetivos,
            'titulo': 'ITCP-PRESUPUESTO REFERENCIAL',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-PRESUPUESTO REFERENCIAL',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'error_messages': []
        }
        return render(request, self.template_name, context)

    def render_form(self, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = self.model.objects.filter(slug=slug)
        context = {
            'proyecto': proyecto_p,
            'objetivos_esp': objetivos,
            'titulo': 'ITCP-PRESUPUESTO REFERENCIAL',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-PRESUPUESTO REFERENCIAL',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'error_messages': []
        }

        # Renderiza el template con el contexto
        return render(self.request, self.template_name, context)
    
    def post(self, request, slug):
        error_messages = []
        elabSolicBs = float(request.POST.get('elabSolicBs', 0))
        ejecFonaBs = float(request.POST.get('ejecFonaBs', 0))
        ejecSolicBs = float(request.POST.get('ejecSolicBs', 0))

        if elabSolicBs != 0.00 and ejecFonaBs != 0.00 and ejecSolicBs!=0.00:
            ejecTotalBs = ejecFonaBs + ejecSolicBs
            ejecFonaPor = round((ejecFonaBs * 100) / ejecTotalBs, 2)
            ejecSolicPor = round((ejecSolicBs * 100) / ejecTotalBs, 2)
            print(ejecFonaPor)
            print(ejecSolicPor)
            if ejecFonaPor > 70.00 or ejecSolicPor < 30.00:
                error_messages.append(f'El porcentaje de la ejecucion del EDTP por parte del FONABOSQUE supera el 70%: {ejecFonaPor:.2f}% y por parte del SOLICITANTE es menor al 30%: {ejecSolicPor :.2f}%')
                print(error_messages, 'MOSTRAR1')
                if error_messages:
                    proyecto_p = get_object_or_404(Postulacion, slug=slug)
                    objetivos = self.model.objects.get(slug=slug)
                    print(objetivos.elab_sol)
                    context = {
                        'proyecto': proyecto_p,
                        'objetivo': objetivos,
                        'titulo': 'ITCP-PRESUPUESTO REFERENCIAL',
                        'entity': 'REGISTRO DATOS DEL PROYECTO',
                        'entity2': 'ITCP-PRESUPUESTO REFERENCIAL',
                        'accion': 'Actualizar',
                        'accion2': 'Cancelar',
                        'accion2_url': reverse('convocatoria:Index'),
                        'error_messages': error_messages,
                    }
                    print
                    return render(self.request, self.template_name, context)
            else:
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

                self.model.objects.create(
                    slug=slug,
                    elab_sol=float(elab_sol),
                    ejec_fona=float(ejec_fona),
                    ejec_sol=float(ejec_sol),
                    elab_fona=float(elab_fona),
                    elab_total=float(elab_total),
                    elab_fona_p=float(elab_fona_p),
                    elab_sol_p=float(elab_sol_p),
                    elab_total_p=float(elab_total_p),
                    ejec_total=float(ejec_total),
                    ejec_fona_p=float(ejec_fona_p),
                    ejec_sol_p=float(ejec_sol_p),
                    ejec_total_p=float(ejec_total_p),
                )
                return redirect('proyecto:registro_ConclRec', slug=slug)
            

class Act_PresupuestoRef(View):
    model = PresupuestoReferencial
    template_name = 'Proyecto/A_PresupuestoRefer.html'

    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = self.model.objects.get(slug=slug)
        print(objetivos.elab_sol)
        context = {
            'proyecto': proyecto_p,
            'objetivo': objetivos,
            'titulo': 'ITCP-PRESUPUESTO REFERENCIAL',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-PRESUPUESTO REFERENCIAL',
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'error_messages': []
        }
        return render(request, self.template_name, context)
        
    def post(self, request, slug):
        error_messages = []
        objetivos = self.model.objects.get(slug=slug)
        print(objetivos.elab_sol, 'en el post')
        elabSolicBs = float(request.POST.get('elabSolicBs', objetivos.elab_sol ).replace(',', '.')) 
        elabFonaBs = float(request.POST.get('elabFonaBs', objetivos.elab_fona ).replace(',', '.')) 
        elabTotalBs = float(request.POST.get('elabTotalBs', objetivos.elab_total ).replace(',', '.'))
        elabFonaPor = float(request.POST.get('elabFonaPor', objetivos.elab_fona_p ).replace(',', '.')) 
        elabSolicPor = float(request.POST.get('elabSolicPor', objetivos.elab_sol_p ).replace(',', '.'))
        elabTotalPor = float(request.POST.get('elabTotalPor', objetivos.elab_total_p ).replace(',', '.'))
        ejecFonaBs = float(request.POST.get('ejecFonaBs', objetivos.ejec_fona ).replace(',', '.'))
        ejecSolicBs = float(request.POST.get('ejecSolicBs', objetivos.ejec_sol ).replace(',', '.'))
        ejecTotalBs = float(request.POST.get('ejecTotalBs', objetivos.ejec_total ).replace(',', '.'))
        ejecFonaPor = float(request.POST.get('ejecFonaPor', objetivos.ejec_fona_p ).replace(',', '.'))
        ejecSolicPor = float(request.POST.get('ejecSolicPor', objetivos.ejec_sol_p ).replace(',', '.'))
        ejecTotalPor = float(request.POST.get('ejecTotalPor', objetivos.ejec_total_p ).replace(',', '.'))

        if elabSolicBs != 0.00 and ejecFonaBs != 0.00 and ejecSolicBs!=0.00:
            if ejecFonaPor > 70.00 or ejecSolicPor < 30.00:
                error_messages.append(f'El porcentaje de la ejecucion del EDTP por parte del FONABOSQUE supera el 70%: {ejecFonaPor:.2f}% y por parte del SOLICITANTE es menor al 30%: {ejecSolicPor :.2f}%')
                print(error_messages, 'MOSTRAR1')
                if error_messages:
                    proyecto_p = get_object_or_404(Postulacion, slug=slug)
                    objetivos = self.model.objects.get(slug=slug)
                    print(objetivos.elab_sol)
                    context = {
                        'proyecto': proyecto_p,
                        'objetivo': objetivos,
                        'titulo': 'ITCP-PRESUPUESTO REFERENCIAL',
                        'entity': 'REGISTRO DATOS DEL PROYECTO',
                        'entity2': 'ITCP-PRESUPUESTO REFERENCIAL',
                        'accion': 'Actualizar',
                        'accion2': 'Cancelar',
                        'accion2_url': reverse('convocatoria:Index'),
                        'error_messages': error_messages,
                    }
                    print
                    return render(self.request, self.template_name, context)
            else:        
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
                return redirect('proyecto:actualizar_PresupuestoRef', slug=slug)
