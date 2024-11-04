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

from proyecto.models import (DatosProyectoBase, Justificacion, Idea_Proyecto, Objetivo_especifico, Beneficiario,
                             Modelo_Acta, Derecho_propietario)
from proyecto.forms import (Reg_DatosBase, Reg_Justificacion, R_Idea_Proyecto, R_Objetivo_especifico, ObjetivoEspecificoForm,
                            Beneficios_esperados, A_Beneficiarios, R_ModeloActa)

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
        context['accion2_url'] = reverse_lazy('solicitud:Index')
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

class Reg_Justificaciones(CreateView):
    model=Justificacion
    template_name = 'Proyecto/R_Justificacion.html'
    form_class = Reg_Justificacion

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        postulacion_p = get_object_or_404(Postulacion, slug=slug)
        
        if self.model.objects.filter(slug=postulacion_p.slug).exists:
            return redirect('proyecto:actualizar_justificacion', slug=postulacion_p.slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Reg_Justificaciones, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        form = self.form_class(request.POST)
        if form.is_valid():
            justificacion = form.save(commit=False)
            justificacion.slug = slug
            justificacion.save()
            return HttpResponseRedirect(reverse('solicitud:registro_Idea_proyecto', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Act_Justificacion(UpdateView):
    model = Justificacion
    template_name = 'Proyecto/R_Justificacion.html'
    form_class = Reg_Justificacion

    def get_context_data(self, **kwargs):
        context = super(Act_Justificacion, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['accion'] = 'Actualizar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
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
            return HttpResponseRedirect(reverse('solicitud:Index', args=[]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Reg_Idea_Proyecto(CreateView):
    model=Idea_Proyecto
    template_name = 'Proyecto/R_Idea_proyecto.html'
    form_class = R_Idea_Proyecto

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if Idea_Proyecto.objects.filter(slug=slug).exists():
            return redirect('proyecto:actualizar_Idea_proyecto', slug=slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Reg_Idea_Proyecto, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        form = self.form_class(request.POST)
        if form.is_valid():
            dato = form.save(commit=False)
            dato.slug = slug
            dato.save()
            return HttpResponseRedirect(reverse('proyecto:registro_obj_especifico', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Act_Idea_Proyecto(UpdateView):
    model = Idea_Proyecto
    template_name = 'Proyecto/R_Idea_proyecto.html'
    form_class = R_Idea_Proyecto

    def get_context_data(self, **kwargs):
        context = super(Act_Idea_Proyecto, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['titulo'] = 'ITCP-IDEA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-IDEA DEL PROYECTO'
        context['accion'] = 'Actualizar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
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
            return HttpResponseRedirect(reverse('solicitud:Index', args=[]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Reg_Objetivo_especifico(CreateView):
    model=Objetivo_especifico
    template_name = 'Proyecto/R_obj_especifico.html'
    form_class = R_Objetivo_especifico

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if self.model.objects.filter(slug=slug).exists():
            print('redireccionando')
            return redirect('proyecto:actualizar_obj_especifico', slug=slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Reg_Objetivo_especifico, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity3'] = 'OBJETIVOS ESPECIFICOS'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        objetivos = request.POST.getlist('objetivo')
        componentes = request.POST.getlist('componente')
        lineas_base = request.POST.getlist('linea_base')
        indicadores = request.POST.getlist('indicador')
        metas = request.POST.getlist('meta')
        for objetivo, componente, linea_base, indicador, meta in zip(objetivos, componentes, lineas_base, indicadores, metas):
            if objetivo and componente and linea_base and indicador and meta:
                self.model.objects.create(
                    slug=slug,
                    objetivo=objetivo,
                    componente=componente,
                    linea_base=linea_base,
                    indicador=indicador,
                    meta=meta
                )        
        return HttpResponseRedirect(reverse('proyecto:registro_Beneficios', args=[slug]))

class Act_Objetivo_especifico(View):
    template_name = 'Proyecto/A_obj_especifico.html'

    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = Objetivo_especifico.objects.filter(slug=slug)
        form = ObjetivoEspecificoForm()  # Formulario vacío para nuevos objetivos
        context = {
            'proyecto': proyecto_p,
            'objetivos_esp': objetivos,
            'form': form,
            'titulo': 'ITCP-IDEA DEL PROYECTO',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-IDEA DEL PROYECTO',
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('solicitud:Index'),
            'entity_registro': reverse_lazy('proyecto:registro_obj_especifico_01', args=[slug]),
            'entity_registro_nom': 'Registrar',
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        print('post method')
        # Actualizar los objetivos existentes
        for objetivo in Objetivo_especifico.objects.filter(slug=slug):
            objetivo.objetivo = request.POST.get(f'objetivo_{objetivo.id}', objetivo.objetivo)
            objetivo.componente = request.POST.get(f'componente_{objetivo.id}', objetivo.componente)
            objetivo.linea_base = request.POST.get(f'linea_base_{objetivo.id}', objetivo.linea_base)
            objetivo.indicador = request.POST.get(f'indicador_{objetivo.id}', objetivo.indicador)
            objetivo.meta = request.POST.get(f'meta_{objetivo.id}', objetivo.meta)
            objetivo.save()

        # Comprobar si se han agregado nuevos objetivos
        return redirect(reverse('solicitud:Index'))

def eliminar_objetivo(request, objetivo_id):
    if request.method == 'POST':
        objeto = Objetivo_especifico.objects.get(id=objetivo_id)
        slug = objeto.slug
        objetivo = get_object_or_404(Objetivo_especifico, id=objetivo_id)
        objetivo.delete()
        return redirect('proyecto:actualizar_obj_especifico', slug=slug)
    
class Reg_Objetivo_especifico01(CreateView):
    model=Objetivo_especifico
    template_name = 'Proyecto/R_obj_especifico.html'
    form_class = R_Objetivo_especifico

    def get_context_data(self, **kwargs):
        context = super(Reg_Objetivo_especifico01, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity3'] = 'OBJETIVOS ESPECIFICOS'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        objetivos = request.POST.getlist('objetivo')
        componentes = request.POST.getlist('componente')
        lineas_base = request.POST.getlist('linea_base')
        indicadores = request.POST.getlist('indicador')
        metas = request.POST.getlist('meta')
        for objetivo, componente, linea_base, indicador, meta in zip(objetivos, componentes, lineas_base, indicadores, metas):
            if objetivo and componente and linea_base and indicador and meta:
                self.model.objects.create(
                    slug=slug,
                    objetivo=objetivo,
                    componente=componente,
                    linea_base=linea_base,
                    indicador=indicador,
                    meta=meta
                )        
        return HttpResponseRedirect(reverse('proyecto:actualizar_obj_especifico', args=[slug]))
    
class R_Beneficios(UpdateView):
    model = Idea_Proyecto
    template_name = 'Proyecto/R_Beneficios.html'
    form_class = Beneficios_esperados

    def get_context_data(self, **kwargs):
        context = super(R_Beneficios, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFCACION DE LA INICIATIVA DEL PROYECTO'
        context['entity3'] = 'BENEFICIOS ESPERADOS DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = self.model.objects.get(slug=slug)        
        form = self.form_class(request.POST, instance = postulacion_pr)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.fecha_actualizacion = timezone.now()
            datos.save()
            return HttpResponseRedirect(reverse('proyecto:registro_justificacion', args=[postulacion_pr.slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class R_Beneficiarios(View):
    model = Beneficiario
    template_name = 'Proyecto/R_Beneficiarios.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if self.model.objects.filter(slug=slug).exists():
            print('redireccionando')
            return redirect('proyecto:actualizar_Beneficiarios', slug=slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug', None)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = self.model.objects.filter(slug=slug)
        context = {
            'proyecto': proyecto_p,
            'objetivos_esp': objetivos,
            'titulo': 'ITCP-IDEA DEL PROYECTO - BENEFICIARIOS',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-IDEA DEL PROYECTO',
            'entity3': 'BENEFICIARIOS',
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('solicitud:Index'),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        hombre_directo = int(request.POST.get('hombresDirecto', 0))
        mujer_directo = int(request.POST.get('mujeresDirecto', 0))
        hombre_indirecto = int(request.POST.get('hombresIndirecto', 0))
        mujer_indirecto = int(request.POST.get('mujeresIndirecto', 0))
        familia = int(request.POST.get('familia', 0))
        self.model.objects.create(
            slug=slug,
            hombre_directo=hombre_directo,
            mujer_directo=mujer_directo,
            hombre_indirecto=hombre_indirecto,
            mujer_indirecto=mujer_indirecto,
            familia=familia,
            )
        return redirect(reverse('solicitud:Index'))

class A_Beneficiarios(View):
    model = Beneficiario
    template_name = 'Proyecto/A_Beneficiarios.html'

    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = self.model.objects.get(slug=slug)
        print(objetivos.hombre_directo, "espa")
        context = {
            'proyecto': proyecto_p,
            'objetivo': objetivos,
            'titulo': 'ITCP-IDEA DEL PROYECTO - BENEFICIARIOS',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-IDEA DEL PROYECTO',
            'entity3': 'BENEFICIARIOS',
            'accion2_url': reverse('solicitud:Index'),            
            'accion2': 'Cancelar',
        }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        print('post method')
        objetivos = self.model.objects.get(slug=slug)
        objetivos.hombre_directo = int(request.POST.get('hombresDirecto', objetivos.hombre_directo))
        objetivos.mujer_directo = int(request.POST.get('mujeresDirecto', objetivos.mujer_directo))
        objetivos.hombre_indirecto = int(request.POST.get('hombresIndirecto', objetivos.hombre_indirecto))
        objetivos.mujer_indirecto = int(request.POST.get('mujeresIndirecto', objetivos.mujer_indirecto))
        objetivos.familia = int(request.POST.get('familia', objetivos.familia))
        objetivos.save()

        # Comprobar si se han agregado nuevos objetivos
        return redirect(reverse('solicitud:Index'))

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
                'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'accion': ' Actualizar',
                'accion2': 'Cancelar',
                'accion2_url': reverse_lazy('solicitud:Index'),
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

        print("Comunidades:", comunidades_list)
        print("Actas:", si_acta_files)
        print("No Actas:", no_acta_texts)

        # Iterar a través de las comunidades

        for si_acta in si_acta_files:
            if si_acta and si_acta.size > 2 * 1024 * 1024:  # 2 MB
                print(si_acta.size, 'tamaño dia')
                error_messages.append('El archivo no debe superar los 2 MB.')

        if error_messages:
            # Renderiza de nuevo con los mensajes de error
            context = {
                'proyecto': get_object_or_404(Postulacion, slug=slug),
                'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'accion': 'Actualizar',
                'accion2': 'Cancelar',
                'accion2_url': reverse_lazy('solicitud:Index'),
                'error_messages': error_messages,  # Pasa los mensajes de error
            }
            return render(request, self.template_name, context)

        for i in range(len(comunidades_list)):
            comunidad = comunidades_list[i]
            si_acta = si_acta_files[i]
            no_acta = no_acta_texts[i]
            print('Ingreso al for para la comunidad:', comunidad)
            if comunidad:
                print('Creando objeto para:', comunidad)
                # Crear el objeto en la base de datos
                Modelo_Acta.objects.create(
                    slug=slug,
                    comunidades=comunidad,
                    si_acta=si_acta if si_acta else None,
                    no_acta=no_acta if not si_acta else no_acta
                )
        print('Finalizado')
        return HttpResponseRedirect(reverse('proyecto:actualizar_ModeloActa', args=[slug]))
    
class A_Modelo_Acta(View):
    template_name = 'Proyecto/A_Modelo_acta01.html'

    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = Modelo_Acta.objects.filter(slug=slug) # Formulario vacío para nuevos objetivos
        context = {
            'proyecto': proyecto_p,
            'modelo_acta': objetivos,
            'titulo': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('solicitud:Index'),
            'entity_registro': reverse_lazy('proyecto:registro_ModeloActa01', args=[slug]),
            'entity_registro_nom': 'Registrar',
            'error_messages': [],

        }
        return render(request, self.template_name, context)
     
    def post(self, request, slug):
        print('ingreso de post')
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
            
            print("Comunidades:", comunidades_list)
            print("Actas:", si_acta_files)
            print("No Actas:", no_acta_texts)

        for si_acta in si_acta_files:
            if si_acta and si_acta.size > 2 * 1024 * 1024:  # 2 MB
                print(si_acta.size, 'tamaño dia')
                error_messages.append('El archivo no debe superar los 2 MB.')

            if error_messages:
                    # Renderiza de nuevo con los mensajes de error
                proyecto_p = get_object_or_404(Postulacion, slug=slug)
                objetivos = Modelo_Acta.objects.filter(slug=slug)
                context = {
                        'proyecto': proyecto_p,
                        'modelo_acta': objetivos,
                        'titulo': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                        'entity': 'REGISTRO DATOS DEL PROYECTO',
                        'entity2': 'TCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                        'accion': 'Actualizar',
                        'accion2': 'Cancelar',
                        'accion2_url': reverse('solicitud:Index'),
                        'entity_registro': reverse_lazy('proyecto:registro_ModeloActa01', args=[slug]),
                        'entity_registro_nom': 'Registrar',
                        'error_messages': error_messages,  # Pasa los mensajes de error
                    }
                return render(request, self.template_name, context)

        # Actualizar los registros
        for i in range(len(comunidades_list)):
            comunidad = comunidades_list[i]
            si_acta = si_acta_files[i]
            no_acta = no_acta_texts[i]

            if comunidad:
                acta_instance, created = Modelo_Acta.objects.get_or_create(
                    slug=slug,
                    comunidades=comunidad,
                    defaults={'si_acta': si_acta, 'no_acta': no_acta}
                )

                if not created:
                    # Si la instancia ya existía, actualiza los campos
                    if si_acta:
                        # Eliminar el archivo antiguo, si existe
                        if acta_instance.si_acta:
                            # Construir la ruta completa del archivo
                            file_path = os.path.join(settings.MEDIA_ROOT, str(acta_instance.si_acta))
                            if os.path.isfile(file_path):
                                os.remove(file_path)  # Eliminar el archivo

                        acta_instance.si_acta = si_acta  # Asignar el nuevo archivo

                    if no_acta is not None:  # Permitir actualizar no_acta incluso si está vacío
                        acta_instance.no_acta = no_acta

                acta_instance.save()

        return HttpResponseRedirect(reverse('proyecto:actualizar_ModeloActa', args=[slug]))
    

def descargar_archivo(request, slug, id):
    #documento = get_object_or_404(Modelo_Acta, slug=slug)
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
            'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse_lazy('solicitud:Index'),
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

        print("Comunidades:", comunidades_list)
        print("Actas:", si_acta_files)
        print("No Actas:", no_acta_texts)

        # Iterar a través de las comunidades

        for si_acta in si_acta_files:
            if si_acta and si_acta.size > 2 * 1024 * 1024:  # 2 MB
                error_messages.append('El archivo no debe superar los 2 MB.')

        if error_messages:
            # Renderiza de nuevo con los mensajes de error
            context = {
                'proyecto': get_object_or_404(Postulacion, slug=slug),
                'titulo': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO',
                'accion': 'Registrar',
                'accion2': 'Cancelar',
                'accion2_url': reverse_lazy('solicitud:Index'),
                'error_messages': error_messages,  # Pasa los mensajes de error
            }
            return render(request, self.template_name, context)

        for i in range(len(comunidades_list)):
            comunidad = comunidades_list[i]
            si_acta = si_acta_files[i]
            no_acta = no_acta_texts[i]
            print('Ingreso al for para la comunidad:', comunidad)
            if comunidad:
                print('Creando objeto para:', comunidad)
                # Crear el objeto en la base de datos
                Modelo_Acta.objects.create(
                    slug=slug,
                    comunidades=comunidad,
                    si_acta=si_acta if si_acta else None,
                    no_acta=no_acta if not si_acta else no_acta
                )
        print('Finalizado')
        return HttpResponseRedirect(reverse('proyecto:actualizar_ModeloActa', args=[slug]))
    
class R_Derecho_propietario(View):
    model=Derecho_propietario
    template_name = 'Proyecto/R_DerechoPropietario.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)

        context = {
            'proyecto': proyecto_p,
            'titulo': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse_lazy('solicitud:Index'),
            'error_messages': []  # Inicializa una lista vacía para los mensajes de error
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):

        slug = self.kwargs.get('slug', None)
        error_messages = []
        index = 0

        while True:
            descripcion = request.POST.get(f'descripcion_{index}')
            si_registro = request.FILES.get(f'si_registro_{index}')
            no_registro = request.POST.get(f'no_registro_{index}')
            zone = request.POST.get(f'zone_{index}')
            easting = request.POST.get(f'easting_{index}')
            northing = request.POST.get(f'northing_{index}')

            if descripcion is None:
                break  # Salir del bucle si no hay más datos      
            # Validación de tamaño del archivo
            if si_registro and si_registro.size > 2 * 1024 * 1024:  # 2 MB
                error_messages.append('El archivo no debe superar los 2 MB.')

            # Crear el objeto solo si hay descripción y sin errores
            if descripcion and not error_messages:
                Derecho_propietario.objects.create(
                    slug=slug,
                    descripcion=descripcion,
                    si_registro=si_registro if si_registro else None,
                    no_registro=no_registro if not si_registro else no_registro,
                    zone=zone,
                    easting=easting,
                    northing=northing,
                )

            index += 1

        if error_messages:
            context = {
                'proyecto': get_object_or_404(Postulacion, slug=slug),
                'titulo': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
                'accion': 'Registrar',
                'accion2': 'Cancelar',
                'accion2_url': reverse_lazy('solicitud:Index'),
                'error_messages': error_messages,  # Pasa los mensajes de error
            }
            return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('proyecto:actualizar_ModeloActa', args=[slug]))