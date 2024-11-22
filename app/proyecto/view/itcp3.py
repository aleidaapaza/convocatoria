import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.utils import timezone
from solicitud.models import Postulacion

from proyecto.models import Idea_Proyecto, Objetivo_especifico, Beneficiario
from proyecto.forms import R_Idea_Proyecto, R_Objetivo_especifico, ObjetivoEspecificoForm, Beneficios_esperados


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
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
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
            return HttpResponseRedirect(reverse('convocatoria:Index', args=[]))
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
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
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
            'accion2_url': reverse('convocatoria:Index'),
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
            objetivo.fecha_actualizacion = timezone.now()
            objetivo.save()

        # Comprobar si se han agregado nuevos objetivos
        return redirect(reverse('convocatoria:Index'))

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
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
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
        return HttpResponseRedirect(reverse('proyecto:registro_Beneficiarios', args=[slug]))
    
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
        context['titulo'] = 'ITCP-JUSTIFICACION DE LA INICIATIVA DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-JUSTIFICACION DE LA INICIATIVA DEL PROYECTO'
        context['entity3'] = 'BENEFICIOS ESPERADOS DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
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
            return HttpResponseRedirect(reverse('proyecto:registro_Beneficiarios', args=[postulacion_pr.slug]))
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
        return self.render_form(slug)

    def render_form(self, slug):
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
            'accion2_url': reverse('convocatoria:Index'),
        }
        return render(self.request, self.template_name, context)

    
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
        return redirect('proyecto:registro_ModeloActa', slug=slug)

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
            'accion2_url': reverse('convocatoria:Index'),            
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
        objetivos.fecha_actualizacion = timezone.now()
        objetivos.save()

        # Comprobar si se han agregado nuevos objetivos
        return redirect('proyecto:registro_DerechoPropietario', slug=slug)