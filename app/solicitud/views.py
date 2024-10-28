from django.forms import ValidationError
from django.shortcuts import render

# Create your views here.

from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, ListView
from solicitud.models import Municipios, Postulacion
from user.models import EncargadoMAE, ResponsableP, Persona
from user.form import Reg_EncargadoMAE, Reg_ResponsableP, Reg_Persona_Res, Reg_Persona_MAE
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

class Mae_Responsable(CreateView):
    model = Postulacion
    second_model = EncargadoMAE
    three_model = ResponsableP
    four_model = Persona
    template_name = 'homepage/MAE.html'
    form_class = Reg_EncargadoMAE
    second_form_class = Reg_Persona_MAE
    three_form_class = Reg_ResponsableP
    four_form_class = Reg_Persona_Res

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
        if 'form3' not in context:
            context['form3'] = self.three_form_class(self.request.GET)
        if 'form4' not in context:
            context['form4'] = self.four_form_class(self.request.GET)

        context['aux_departamento'] = aux_municipio.departamento
        context['aux_municipio'] = aux_municipio.nombre_municipio
        context['titulo'] = 'Registro de encargado de la MAE'
        context['entity'] = 'Registro de encargado de la MAE'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Index')
        return context

    def post(self, request, *args, **kwargs):
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
        form3 = self.three_form_class(request.POST)
        form4 = self.four_form_class(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            carnet_file = form.cleaned_data.get('carnet')
            asignacion_file = form.cleaned_data.get('asignacion')
            max_size = 2 * 1024 * 1024
            if carnet_file.size > max_size or asignacion_file.size > max_size:
                if carnet_file.size > max_size:
                    form2.add_error('carnet', 'El archivo carnet no debe superar los 2 MB.')
                if asignacion_file.size > max_size:
                    form2.add_error('asignacion', 'El archivo de asignacion no debe superar los 2 MB.')
                return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, form4=form4))
            
            if form2.errors:  # Si hay errores en form2, retornar
                return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, form4=form4))

            municipiobj.estado = 'SOLICITUD'
            municipiobj.save()

            encar_Mae = form.save(commit=False)
            persona_mae = form2.save()
            print('personaMAE',persona_mae)
            encar_Mae.persona = persona_mae
            encar_Mae.save()
            responsable_p = form3.save(commit=False)
            persona_Responsable = form4.save()            
            print('personaResponsable',persona_Responsable)
            responsable_p.persona = persona_Responsable
            responsable_p.save()
            postulacion_f = self.model.objects.create(
                municipio=municipiobj,
                mae=encar_Mae,
                responsable=responsable_p,
            )
            id_post = postulacion_f.slug
            print(id_post,"esto es el id de la postulacion")
            return HttpResponseRedirect(reverse('solicitud:Confirmacion_solicitud', args=[id_post]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, form4=form4))

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