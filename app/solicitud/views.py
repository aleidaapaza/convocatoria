from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, ListView, UpdateView
from solicitud.models import Municipios, Postulacion
from user.models import EncargadoMAE, ResponsableP, Persona, User, Revisor, SuperUser
from proyecto.models import DatosProyectoBase

from user.form import Reg_EncargadoMAE, Reg_ResponsableP, Reg_Persona_Res, Reg_Persona_MAE, User_Reg, Update_MAE
from solicitud.form import Update_Postulacion, update_Post
from solicitud.choices import departamento_s, entidad_s


class solicitud(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(solicitud, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.is_municipio:
                user_sl = self.request.user.username_proyecto.slug
                context['slug']=user_sl
                print(user_sl)
                postulacion_p = Postulacion.objects.get(slug = user_sl)
                print(postulacion_p)
                context['postulacion'] = postulacion_p
            elif self.request.user.is_revisor:
                user_sl = self.request.user.revisor_perfil.slug
                context['slug']=user_sl
                print(user_sl)
                postulacion_p = Revisor.objects.get(slug = user_sl)
                print(postulacion_p)
                context['postulacion'] = postulacion_p
            elif self.request.user.is_superuser:
                user_sl = self.request.user.superuser_perfil.slug
                context['slug']=user_sl
                print(user_sl)
                postulacion_p = SuperUser.objects.get(slug = user_sl)
                print(postulacion_p)
                context['postulacion'] = postulacion_p
        
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

class mae_r(CreateView):
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
            nn_entidad = entidad_s(n_entidad)
            municipiobj = Municipios.objects.create(
                departamento = municipio_aux.departamento,
                entidad_territorial = nn_entidad,
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
    second_model = EncargadoMAE
    third_model = User
    four_model = DatosProyectoBase
    template_name = 'Postulaciones/ficha.html'
    form_class = Update_Postulacion
    second_form_class = Update_MAE
    third_form_class = User_Reg

    def get_context_data(self, **kwargs):
        context = super(fichaSolicitud, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        postulacion_p = self.model.objects.get(slug=slug)        
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET, self.request.FILES)
        if postulacion_p.estado: 
            if 'form3' not in context:
                context['form3'] = self.third_form_class(self.request.GET)
            if self.four_model.objects.filter(slug=slug).exists():
                datosP = self.four_model.objects.get(slug=slug)
                user = self.third_model.objects.get(id=datosP.user.id)
                context['userMun'] = user
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
        print(postulacion_pr,'propuesta')
        print(postulacion_pr.responsable.slug,'propuesta')
        responsable_pr = self.second_model.objects.get(slug = postulacion_pr.mae.slug)
        form = self.form_class(request.POST, instance = postulacion_pr)
        form2 = self.second_form_class(request.POST, request.FILES, instance = responsable_pr)
        form3 = self.third_form_class(request.POST)

        if form.is_valid() and form2.is_valid():
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
            estado_post = form.cleaned_data.get('estado')
            print('estado', estado_post)
            if estado_post:
                form.save()
                if  form3.is_valid():
                    user_Pr = form3.save(commit=False)
                    user_Pr.is_municipio = True
                    user_Pr.save()
                    datos_proyecto = self.four_model.objects.create(
                        slug = slug,
                        user = user_Pr,
                        nombre = 'PRY',
                        n_comunidades = '0',
                        comunidades = 'comunidades',
                        tipologia_proy = False,
                        periodo_ejecu = '0',
                    )
                    print(datos_proyecto)
                    postulacion_c = Postulacion.objects.get(slug=slug)
                    municipio_c = Municipios.objects.get(id=postulacion_c.municipio.id)
                    municipio_c.estado="APROBADO"
                    municipio_c.p_a=True
                    municipio_c.save()
                    return HttpResponseRedirect(reverse('proyecto:lista_inicio', args=[]))
                else:
                    return self.render_to_response(self.get_context_data(form=form, form2=form2 ))
            else:                
                postulacion_c = Postulacion.objects.get(slug=slug)
                municipio_c = Municipios.objects.get(id=postulacion_c.municipio.id)
                municipio_c.estado="NINGUNO"
                municipio_c.p_a=True
                municipio_c.save()
                return HttpResponseRedirect(reverse('solicitud:ListaSolicitud', args=[]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class Act_Ficha_MAE(UpdateView):
    model = Postulacion
    second_model = EncargadoMAE
    third_model = Persona
    template_name='Postulaciones/actualizar.html'
    form_class=update_Post
    second_form_class=Reg_EncargadoMAE
    third_form_class = Reg_Persona_MAE

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        postulacion_p = get_object_or_404(self.model, slug=slug)

        if postulacion_p.modificacion:
            return redirect('solicitud:Index')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug', None)        
        postulacion_p = self.model.objects.get(slug=slug)
        context = super(Act_Ficha_MAE, self).get_context_data(**kwargs)
        mae_p = self.second_model.objects.get(id=postulacion_p.mae.id)
        persona_mae = self.third_model.objects.get(id=mae_p.persona.id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=mae_p)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(instance=persona_mae)
        context['postulacion'] = postulacion_p
        context['titulo'] = 'ACTUALIZAR DATOS DE LA SOLICITUD'
        context['activate'] = False
        context['entity'] = 'ACTUALIZAR DATOS DE LA SOLICITUD'
        context['entity2'] = 'DATOS MAE'
        context['entity_url'] = reverse_lazy('solicitud:Index') 
        return context 
    
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = Postulacion.objects.get(slug=slug)
        mae_p = self.second_model.objects.get(id=postulacion_pr.mae.pk)
        persona_mae = self.third_model.objects.get(id=mae_p.persona.pk)
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, request.FILES, instance=mae_p)
        form3 = self.third_form_class(request.POST, instance=persona_mae)

        if form2.is_valid() and form3.is_valid():
            mae_R = EncargadoMAE.objects.get(id = postulacion_pr.mae.pk)
            per_mae = Persona.objects.get(id=mae_R.persona.pk)
            print(mae_R)
            print(per_mae)
            print('responsable')            
            form2.save()
            form3.save()
            postulacion_pr.modificacion = True
            postulacion_pr.save()
            return HttpResponseRedirect(reverse('solicitud:Actualizar_Ficha_eNC', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))



class Act_ficha_Resp(UpdateView):
    model=Postulacion 
    second_model= ResponsableP
    third_model= Persona
    template_name='Postulaciones/actualizar.html'
    form_class=update_Post
    second_form_class=Reg_ResponsableP
    third_form_class = Reg_Persona_Res

    def get_context_data(self, **kwargs):
        context = super(Act_ficha_Resp, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        postulacion_p = self.model.objects.get(slug=slug)
        responsable_p = self.second_model.objects.get(id=postulacion_p.responsable.pk)
        persona_responsable = self.third_model.objects.get(id=responsable_p.persona.pk)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=responsable_p)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(instance=persona_responsable)

        context['postulacion'] = postulacion_p
        context['titulo'] = 'ACTUALIZAR DATOS DE LA SOLICITUD'
        context['activate'] = False
        context['entity'] = 'ACTUALIZAR DATOS DE LA SOLICITUD'
        context['entity2'] = 'DATOS RESPONSABLE DEL PROYECTO'
        context['entity_url'] = reverse_lazy('solicitud:Index') 
        return context 
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        postulacion_pr = Postulacion.objects.get(slug=slug)
        responsable_p = self.second_model.objects.get(id=postulacion_pr.responsable.pk)
        persona_responsable = self.third_model.objects.get(id=responsable_p.persona.pk)
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, request.FILES, instance=responsable_p)
        form3 = self.third_form_class(request.POST, instance=persona_responsable)

        if form2.is_valid() and form3.is_valid():
            mae_R = EncargadoMAE.objects.get(id = postulacion_pr.responsable.pk)
            per_mae = Persona.objects.get(id=mae_R.persona.pk)
            print(mae_R)
            print(per_mae)
            print('responsable')
            form2.save()
            form3.save()
            postulacion_pr.modificacion = True
            postulacion_pr.save()
            return HttpResponseRedirect(reverse('solicitud:Confirmacion_solicitud', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))

    

