import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.utils import timezone

from django.conf import settings
from django.contrib import messages

from solicitud.models import Postulacion
from proyecto.models import ObjetivoGeneralEjec, ObjetivoEspecificoEjec
from proyecto.forms import R_ObjEjec, R_Hectarea, R_ObjetivoEsp

class R_ObjetivoGeneral(CreateView):
    model = ObjetivoGeneralEjec
    template_name = 'Proyecto/Ejec/ObjetivoGeneral.html'
    form_class = R_ObjEjec

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if ObjetivoGeneralEjec.objects.filter(slug=slug).exists():
            return redirect('proyecto:actualizar_ObjetivoGeneral', slug=slug)
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(R_ObjetivoGeneral, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'OBJETIVO GENERAL DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'OBJETIVO GENERAL DEL PROYECTO'
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
            return HttpResponseRedirect(reverse('proyecto:registro_ObjetivoEspecifico', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class A_ObjetivoGeneral(UpdateView):
    model = ObjetivoGeneralEjec
    template_name = 'Proyecto/Ejec/ObjetivoGeneral.html'
    form_class = R_ObjEjec

    def get_context_data(self, **kwargs):
        context = super(A_ObjetivoGeneral, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p  
        context['titulo'] = 'OBJETIVO GENERAL DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'OBJETIVO GENERAL DEL PROYECTO'
        context['accion'] = 'Actualizar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
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
            messages.success(request, 'OBJETIVO GENERAL DEL PROYECTO - se actualizo correctamente.')
            return redirect('proyecto:registro_ObjetivoEspecifico', slug=slug)
        else:
            messages.error(request, 'Hubo un error al actualizar los datos.')
            return self.render_to_response(self.get_context_data(form=form))

class R_ObjetivoEspecifico(UpdateView):
    model = ObjetivoGeneralEjec
    second_model = ObjetivoEspecificoEjec
    template_name = 'Proyecto/Ejec/ObjetivoEspecifico.html'
    form_class = R_Hectarea
    second_form_class = R_ObjetivoEsp

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if ObjetivoEspecificoEjec.objects.filter(slug=slug).exists():
            return redirect('proyecto:actualizar_ObjetivoEspecifico', slug=slug)
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(R_ObjetivoEspecifico, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'OBJETIVOS ESPECIFICOS, COMPONENTES Y METAS'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'OBJETIVOS ESPECIFICOS, COMPONENTES Y METAS'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse('proyecto:registro_ObjetivoEspecifico', args=[slug])
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        model = self.model.objects.get(slug=slug)        
        form = self.form_class(request.POST, instance = model)
        if form.is_valid():
            form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        objetivos = request.POST.getlist('objetivo')
        componentes = request.POST.getlist('componente')
        metas = request.POST.getlist('meta')
        for objetivo, componente, meta in zip(objetivos, componentes, metas):
            print(objetivo,componente,meta)
            if objetivo and componente and meta:
                self.second_model.objects.create(
                    slug=slug,
                    objetivo=objetivo,
                    componente=componente,
                    meta=meta
                )
            
        messages.success(request, "OBJETIVOS ESPECIFICOS, COMPONENTES Y METAS - se actualizo correctamente.")
        return redirect('proyecto:registro_Beneficiarios', slug=slug)

class A_ObjetivoEspecifico(UpdateView):
    model = ObjetivoGeneralEjec  # Modelo que vas a actualizar
    form_class = R_Hectarea  # El formulario asociado
    template_name = 'Proyecto/Ejec/A_ObjetivoEspecifico.html'  # La plantilla que renderiza el formulario
 
    # Método que se ejecuta al obtener la vista, para añadir datos adicionales al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        postulacion = get_object_or_404(Postulacion, slug=slug)
        objetivos = ObjetivoEspecificoEjec.objects.filter(slug=slug)
        acciones = {
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'entity_registro': reverse_lazy('proyecto:actualizar_ObjetivoEspecificoE', args=[slug]),
            'entity_registro_nom': 'Registrar Mas Objetivos'
        }
        context.update({
            'proyecto': postulacion,
            'objetivos_esp': objetivos,
            'titulo': 'OBJETIVOS ESPECIFICOS, COMPONENTES Y METAS',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'OBJETIVOS ESPECIFICOS, COMPONENTES Y METAS',
        })
        context.update(acciones)
        message_map = {
            'success': ('Actualización Exitosa', ''),
            'error': ('Error al Actualizar', ''),
            'warning': ('Advertencia', ''),
            'info': ('Información', ''),
        }
        for message in messages.get_messages(self.request):
            level_tag = message.level_tag
            if level_tag in message_map:
                context['message_title'], context['message_content'] = message_map[level_tag]
                context['message_content'] = message.message

        return context


    # Método que se ejecuta después de guardar el formulario
    def form_valid(self, form):
        # Llama a la implementación predeterminada de form_valid para guardar el formulario
        response = super().form_valid(form)
        
        # Actualizar los objetivos existentes
        for objetivo in ObjetivoEspecificoEjec.objects.filter(slug=self.kwargs['slug']):
            objetivo.objetivo = self.request.POST.get(f'objetivo_{objetivo.id}', objetivo.objetivo)
            objetivo.componente = self.request.POST.get(f'componente_{objetivo.id}', objetivo.componente)
            objetivo.meta = self.request.POST.get(f'meta_{objetivo.id}', objetivo.meta)
            objetivo.fecha_actualizacion = timezone.now()
            objetivo.save()

        # Mensaje de éxito después de la actualización
        messages.success(self.request, 'OBJETIVOS ESPECIFICOS, COMPONENTES Y METAS - se actualizó correctamente.')
        return response

    # Redirige a una URL después de una actualización exitosa
    def get_success_url(self):
        # Aquí puedes redirigir a donde desees después de la actualización
        return reverse_lazy('proyecto:registro_Beneficiarios', kwargs={'slug': self.kwargs['slug']})


def eliminar_objetivoEjec(request, objetivo_id):
    if request.method == 'POST':
        objeto = ObjetivoEspecificoEjec.objects.get(id=objetivo_id)
        slug = objeto.slug
        objetivo = get_object_or_404(ObjetivoEspecificoEjec, id=objetivo_id)
        objetivo.delete()
        return redirect('proyecto:actualizar_ObjetivoEspecifico', slug=slug)
    
class Reg_ObjetivoEsp(CreateView):
    model=ObjetivoEspecificoEjec
    template_name = 'Proyecto/Ejec/R_ObjetivoEspecifico.html'
    form_class = R_ObjetivoEsp

    def get_context_data(self, **kwargs):
        context = super(Reg_ObjetivoEsp, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'AGREGAR OBJETIVOS ESPECIFICOS'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'AGREGAR OBJETIVOS ESPECIFICOS'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse('proyecto:actualizar_ObjetivoEspecifico', args=[slug])
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        objetivos = request.POST.getlist('objetivo')
        componentes = request.POST.getlist('componente')
        metas = request.POST.getlist('meta')
        for objetivo, componente, meta in zip(objetivos, componentes, metas):
            if objetivo and componente and meta:
                self.model.objects.create(
                    slug=slug,
                    objetivo=objetivo,
                    componente=componente,
                    meta=meta
                )        
        return HttpResponseRedirect(reverse('proyecto:actualizar_ObjetivoEspecifico', args=[slug]))
    