from django.forms import ValidationError
from django.shortcuts import render

# Create your views here.

from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, ListView, UpdateView
from solicitud.models import Municipios, Postulacion
from user.models import EncargadoMAE, ResponsableP, Persona, User
from proyecto.models import DatosProyectoBase

from user.form import Reg_EncargadoMAE, Reg_ResponsableP, Reg_Persona_Res, Reg_Persona_MAE, User_Reg, Update_MAE
from solicitud.form import Update_Postulacion
from solicitud.choices import departamento_s, entidad_s


class solicitud(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(solicitud, self).get_context_data(**kwargs)
        return context

class entidad(TemplateView):
    template_name = 'homepage/entidadTerritorial.html'
    def get_context_data(self, **kwargs):
        context = super(entidad, self).get_context_data(**kwargs)
        departamento = self.kwargs.get('departamento', 0)
        context['dep'] = departamento
        context['entity'] = 'ENTIDAD TERRITORIAL'
        return context

class municipio(ListView):
    model = Municipios
    template_name = 'homepage/municipio.html'
    def get_context_data(self, **kwargs):
        context = super(municipio, self).get_context_data(**kwargs)
        n_departamento = self.kwargs.get('departamento', 0)
        print(n_departamento)
        departamentos = departamento_s(n_departamento)
        print(departamentos)
        n_entidad = self.kwargs.get('entidad',0)
        print(n_entidad)
        entidades = entidad_s(n_entidad)
        print(entidades)
        if n_entidad <3:
            municipios_f = Municipios.objects.filter(departamento=departamentos).filter(entidad_territorial=entidades).filter(estado='NINGUNO').order_by('-nombre_municipio')
        else:
            municipios_f = Municipios.objects.filter(departamento=departamentos).filter(entidad_territorial='GOBIERNO AUTÓNOMO MUNICIPAL').filter(estado='NINGUNO').order_by('-nombre_municipio')
        print(municipios_f)       
        if municipios_f.acount() == 0:
            context['object_list'] = 0
        else:
            context['object_list'] = municipios_f
        print(municipios_f)
        context['dep'] = departamentos
        context['ent'] = entidades
        context['n_ent'] = n_entidad        
        context['entity'] = 'ENTIDAD TERRITORIAL'
        return context

def validate_file_size(archivo):
    limit = 2*1024*1024
    if archivo.size > limit:
        raise ValidationError('El tamaño del archivo no puede exceder los 2 MB')

class MAE(CreateView):
    model = Postulacion
    template_name = 'homepage/MAE.html'
    form_class = Reg_EncargadoMAE
    second_form_class = Reg_Persona_MAE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        n_municipio = self.kwargs.get('pk', 0)
        n_entidad = self.kwargs.get('entidad', 0)
        aux_municipio = Municipios.objects.get(id=n_municipio)
        if n_entidad < 3:
            context['aux_entidad'] = aux_municipio.entidad_territorial
        else:
            context['aux_entidad'] = entidad_s(n_entidad)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET, self.request.FILES)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)

        context['aux_departamento'] = aux_municipio.departamento
        context['aux_municipio'] = aux_municipio.nombre_municipio
        context['titulo'] = 'Registro de encargado de la MAE'
        context['entity'] = 'Registro de encargado de la MAE'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        municipio_pk = kwargs['pk']
        n_entidad = kwargs['entidad']
        if n_entidad < 3:
            municipiobj = Municipios.objects.get(id=municipio_pk)
        else:
            municipio_aux = Municipios.objects.get(id=municipio_pk)
            municipiobj = Municipios.objects.create(
                departamento = municipio_aux.departamento,
                entidad_territorial = n_entidad,
                nombre_municipio = municipio_aux.nombre_municipio,
                estado = 'SOLICITUD',
                p_a = False,
            )

        form = self.form_class(request.POST, request.FILES)
        form2 = self.second_form_class(request.POST)

        if form.is_valid() and form2.is_valid():
            carnet_file = form.cleaned_data.get('carnet')
            asignacion_file = form.cleaned_data.get('asignacion')
            max_size = 2 * 1024 * 1024
            if carnet_file.size > max_size or asignacion_file.size > max_size:
                if carnet_file.size > max_size:
                    form.add_error('carnet', 'El archivo carnet no debe superar los 2 MB.')
                if asignacion_file.size > max_size:
                    form.add_error('asignacion', 'El archivo de asignacion no debe superar los 2 MB.')                    
                return self.render_to_response(self.get_context_data(form=form, form2=form2))
            
            municipiobj.estado = 'SOLICITUD'
            municipiobj.save()

            encar_Mae = form.save(commit=False)
            persona_mae = form2.save()
            print('personaMAE',persona_mae)
            encar_Mae.persona = persona_mae
            encar_Mae.save()
            personaResp = Persona.objects.create(
                nombre = 'Responsable',
                apellido = 'proyecto',
                cargo = 'cargo resp PR',
                celular = '00000',
            )
            responsablePr = ResponsableP.objects.create(
                persona = personaResp,
                correo = 'correo@gn.com'
            )
            postulacion_f = self.model.objects.create(
                municipio=municipiobj,
                mae=encar_Mae,
                responsable=responsablePr,
            )
            id_post = postulacion_f.slug
            print(id_post,"esto es el id de la postulacion")
            return HttpResponseRedirect(reverse('solicitud:ResponsableProyecto', args=[id_post]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class ResponsableProy(UpdateView):
    model = Postulacion
    second_model = ResponsableP
    three_model = Persona
    template_name = 'homepage/Responsable.html'
    form_class = Reg_ResponsableP
    second_form_class = Reg_Persona_Res

    def get_context_data(self, **kwargs):
        context = super(ResponsableProy, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        postulacion_p = self.model.objects.get(slug=slug)
        context['postulacion'] = postulacion_p
        context['titulo'] = 'Registro de encargado del proyecto'
        context['entity'] = 'Registro de encargado del proyecto'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = self.model.objects.get(slug=slug)
        responsable_pr = self.second_model.objects.get(slug = postulacion_pr.responsable.slug)
        persona_resp = self.three_model.objects.get(id = responsable_pr.persona.id)

        form = self.form_class(request.POST, instance = responsable_pr)
        form2 = self.second_form_class(request.POST, instance = persona_resp)

        if form.is_valid() and form2.is_valid():
            form2.save()
            form.save()          
            slug_post = postulacion_pr.slug
            print(slug_post,"esto es el id de la postulacion")
            return HttpResponseRedirect(reverse('solicitud:Confirmacion_solicitud', args=[slug_post]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class Confirmacion(TemplateView):
    template_name = 'homepage/confirmacionRegistro.html'
    def get_context_data(self, **kwargs):
        context = super(Confirmacion, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        postulacion = Postulacion.objects.get(slug=slug)
        context['entity'] = 'confirmacion solicitud'
        context['postulacion'] = postulacion
        return context
    
class ListaSolicitudes(ListView):
    model = Postulacion
    template_name = 'Postulaciones/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA DE SOLICITUDES'
        context['activate'] = True
        context['entity'] = 'LISTA DE SOLICITUDES'
        context['object_list'] = self.model.objects.all()
        return context

class fichaSolicitud(UpdateView):
    model = Postulacion
    second_module = EncargadoMAE
    third_module = User
    four_module = DatosProyectoBase
    template_name = 'Postulaciones/ficha.html'
    form_class = Update_Postulacion
    second_form_class = Update_MAE
    third_form_class = User_Reg

    def get_context_data(self, **kwargs):
        context = super(fichaSolicitud, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET, self.request.FILES)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)

        postulacion_p = self.model.objects.get(slug=slug)        
        context['postulacion'] = postulacion_p
        context['titulo'] = 'Registro de encargado del proyecto'
        context['activate'] = False
        context['entity'] = 'LISTADO DE SOLICITUDES'
        context['entity_url'] = reverse_lazy('solicitud:ListaSolicitud')
        context['activate2'] = True
        context['entity2'] = 'FICHA SOLICITUD'  
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = self.model.objects.get(slug=slug)
        responsable_pr = self.second_model.objects.get(slug = postulacion_pr.responsable.slug)

        form = self.form_class(request.POST, instance = responsable_pr)
        form2 = self.second_form_class(request.POST, instance = responsable_pr)
        form3 = self.third_form_class(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            carnet_file = form2.cleaned_data.get('carnet')
            asignacion_file = form2.cleaned_data.get('asignacion')
            max_size = 2 * 1024 * 1024
            if carnet_file.size > max_size or asignacion_file.size > max_size:
                if carnet_file.size > max_size:
                    form2.add_error('carnet', 'El archivo carnet no debe superar los 2 MB.')
                if asignacion_file.size > max_size:
                    form2.add_error('asignacion', 'El archivo de asignacion no debe superar los 2 MB.')                    
                return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))
            form2.save()
            estado_post = form2.cleaned_data.get('estado')
            if estado_post:
                form.save()
                user_Pr = form3.save()
                datos_proyecto = self.four_module.objects.create(
                    slug = slug,
                    user = user_Pr,
                    nombre = 'PRY',
                    n_comunidades = '0',
                    comunidades = 'comunidades',
                    tipologia_proy = False,
                    periodo_ejecu = '0',
                )
                slug_pry = datos_proyecto.slug
                postulacion_pr.municipio.estado = 'APROBADO'
            else:
                form.save()
                postulacion_pr.municipio.estado ='NINGUNO'
            form.save()          
            slug_post = postulacion_pr.slug
            print(slug_post,"esto es el id de la postulacion")
            return HttpResponseRedirect(reverse('solicitud:Confirmacion_solicitud', args=[slug_post]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

