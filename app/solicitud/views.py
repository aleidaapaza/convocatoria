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
from user.form import Reg_EncargadoMAE, Reg_ResponsableP, Reg_Persona_En, Reg_Persona_Res
from solicitud.choices import departamento_s, entidad_s


class solicitud(TemplateView):
    template_name = 'index.html'

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
        departamentos = departamento_s(n_departamento)
        n_entidad = self.kwargs.get('entidad',0)
        entidades = entidad_s(n_entidad)
        municipios_f = Municipios.objects.filter(departamento=departamentos).filter(entidad_territorial=entidades).filter(estado='NINGUNO').order_by('-nombre_municipio')        
        if municipios_f.acount() == 0:
            context['object_list'] = 0
        else:
            context['object_list'] = municipios_f
        print(municipios_f)
        context['dep'] = departamentos
        context['ent'] = entidades        
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
    template_name = 'homepage/responsable_MAE.html'
    form_class = Reg_Persona_En
    two_form = Reg_EncargadoMAE
    three_form = Reg_Persona_Res
    four_form = Reg_ResponsableP

    def get_context_data(self, **kwargs):
        context = super(Mae_Responsable, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form1' not in context:
            context['form1'] = self.two_form(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.three_form(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.four_form(self.request.GET)

        context['titulo'] = 'Registro de encargado de la MAE y Responsable de Proyecto'
        context['entity'] = 'Registro de encargado de la MAE y Responsable de Proyecto'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('solicitud:Departamento')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        municipio_pk = kwargs['pk']
        municipiobj = Municipios.objects.get(id=municipio_pk)
        form = self.form_class(request.POST)
        form1 = self.two_form(request.POST, request.FILES)
        form2 = self.three_form(request.POST)
        form3 = self.four_form(request.POST)
        if form.is_valid() and form1.is_valid() and form2.is_valid() and form3.is_valid():
            carnet_file = form1.cleaned_data.get('carnet')
            asignacion_file = form1.cleaned_data.get('asignacion')
            max_size = 2 * 1024 * 1024

            if carnet_file.size > max_size or asignacion_file.size > max_size:
                if carnet_file.size > max_size:
                    form1.add_error('carnet', 'El archivo carnet no debe superar los 2 MB.')
                if asignacion_file.size > max_size:
                    form1.add_error('asignacion', 'El archivo de asignacion no debe superar los 2 MB.')
                return self.render_to_response(self.get_context_data(form=form, form1=form1, form2=form2, form3=form3))
            
            persona_mae = form.save()
            persona_Responsable = form2.save()            
            encar_Mae = form1.save(commit=False)
            encar_Mae.persona = persona_mae
            encar_Mae.save()
            responsable_p = form3.save(commit=False)
            responsable_p.persona = persona_Responsable
            responsable_p.save()
            postulacion_f = self.model.objects.create(
                municipio=municipiobj,
                mae=encar_Mae,
                responsable=responsable_p,
            )
            id_post = postulacion_f.pk
            print(id_post,"esto es el id de la postulacion")
            return HttpResponseRedirect(reverse('solicitud:Confirmacion_solicitud', args=[id_post]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form1=form1, form2=form2, form3=form3))


class Confirmacion(TemplateView):
    template_name = 'homepage/confirmacionRegistro.html'
    def get_context_data(self, **kwargs):
        context = super(Confirmacion, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        postulacion = Postulacion.objects.get(slug=slug)
        context['entity'] = 'confirmacion solicitud'
        context['postulacion'] = postulacion
        return context