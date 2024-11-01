from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from solicitud.models import Postulacion

from proyecto.models import DatosProyectoBase, Justificacion
from proyecto.forms import Reg_DatosBase, Reg_Justificacion

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
    second_model = Postulacion
    template_name = 'Proyecto/R_DatosProyecto.html'
    form_class = Reg_DatosBase

    def get_context_data(self, **kwargs):
        context = super(RegistroDatosBasicos, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = self.model.objects.get(slug=slug)
        context['postulacion'] = proyecto_p
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
        postulacion_pr = self.model.objects.get(slug=slug)        
        form = self.form_class(request.POST, instance = postulacion_pr)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('proyecto:registro_justificacion', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form ))

class Reg_Justificaciones(CreateView):
    model=Justificacion
    second_model=DatosProyectoBase
    template_name = 'Proyecto/R_Justificacion.html'
    form_class = Reg_Justificacion
    def get_context_data(self, **kwargs):
        context = super(Reg_Justificaciones, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = self.second_model.objects.get(slug=slug)
        context['postulacion'] = proyecto_p
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
            return HttpResponseRedirect(reverse('solicitud:ResponsableProyecto', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form))


