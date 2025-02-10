from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.utils import timezone

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
from convocatoria.models import Convocatoria

from user.form import Reg_EncargadoMAE, Reg_ResponsableP, Reg_Persona_Res, Reg_Persona_MAE, User_Reg, Update_MAE
from solicitud.form import Update_Postulacion, update_Post
from solicitud.choices import departamento_s, entidad_s, financiamiento_s

class departamento(TemplateView):
    template_name = 'homepage/departamento.html'
    def get_context_data(self, **kwargs):
        context = super(departamento, self).get_context_data(**kwargs)
        financiamiento = self.kwargs.get('financiamiento', 0)
        financiamiento_d = financiamiento_s(financiamiento)
        context['fin'] = financiamiento
        context['fin_d'] = financiamiento_d
        context['entity'] = 'DEPARTAMENTO'
        fecha = Convocatoria.objects.get(estado=True)
        context['convocatoria']=fecha
        fechaHoy = datetime.now()
        print(fechaHoy, 'fecha actual')
        fechalanzamiento = datetime.combine(fecha.fechaLanzamiento, fecha.horaLanzamiento)
        fechaCierre = datetime.combine(fecha.fechaCierre, fecha.horaCierre)
        context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
        return context

class entidad(TemplateView):
    template_name = 'homepage/entidadTerritorial.html'
    def get_context_data(self, **kwargs):
        context = super(entidad, self).get_context_data(**kwargs)
        financiamiento = self.kwargs.get('financiamiento', 0)
        departamento = self.kwargs.get('departamento', 0)
        financiamiento_d = financiamiento_s(financiamiento)
        context['fin'] = financiamiento
        context['fin_d'] = financiamiento_d
        departamentos = departamento_s(departamento)
        context['dep'] = departamento
        context['dep_d'] = departamentos
        context['entity'] = 'ENTIDAD TERRITORIAL'
        fecha = Convocatoria.objects.get(estado=True)
        context['convocatoria']=fecha
        fechaHoy = datetime.now()
        print(fechaHoy, 'fecha actual')
        fechalanzamiento = datetime.combine(fecha.fechaLanzamiento, fecha.horaLanzamiento)
        fechaCierre = datetime.combine(fecha.fechaCierre, fecha.horaCierre)
        context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
        return context

class municipio(ListView):
    model = Municipios
    template_name = 'homepage/municipio.html'
    def get_context_data(self, **kwargs):
        context = super(municipio, self).get_context_data(**kwargs)
        n_financiamiento = self.kwargs.get('financiamiento', 0)
        n_departamento = self.kwargs.get('departamento', 0)
        n_entidad = self.kwargs.get('entidad',0)
        financiamiento = financiamiento_s(n_financiamiento)
        departamentos = departamento_s(n_departamento)
        entidades = entidad_s(n_entidad)
        if n_entidad <3:
            municipios_f = Municipios.objects.filter(
                            departamento=departamentos,
                            entidad_territorial=entidades,
                            estado='NINGUNO'
                        ).order_by('nombre_municipio')
        else:
            municipios_f = Municipios.objects.filter(
                            departamento=departamentos, 
                            entidad_territorial='GOBIERNO AUTÓNOMO MUNICIPAL'
                        ).order_by('nombre_municipio')
        fecha = Convocatoria.objects.get(estado=True)
        context['convocatoria']=fecha
        fechaCierre = datetime.combine(fecha.fechaCierre, fecha.horaCierre)
        context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
        contarMun = municipios_f.acount()
        if  contarMun == 0:
            context['object_list'] = 0
        else:
            context['object_list'] = municipios_f
        context['dep'] = departamentos
        context['ent'] = entidades
        context['fin'] = financiamiento
        context['n_ent'] = n_entidad
        context['n_fin'] = n_financiamiento
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
        n_financiamiento = self.kwargs.get('financiamiento', 0)        
        aux_municipio = Municipios.objects.get(id=n_municipio)
        if n_entidad < 3:
            context['aux_entidad'] = aux_municipio.entidad_territorial
        else:
            context['aux_entidad'] = entidad_s(n_entidad)
        context['aux_financiamiento'] = financiamiento_s(n_financiamiento)
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
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        fecha = Convocatoria.objects.get(estado=True)
        context['convocatoria']=fecha
        fechaHoy = datetime.now()
        print(fechaHoy, 'fecha actual')
        fechalanzamiento = datetime.combine(fecha.fechaLanzamiento, fecha.horaLanzamiento)
        fechaCierre = datetime.combine(fecha.fechaCierre, fecha.horaCierre)
        context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        municipio_pk = kwargs['pk']
        n_entidad = kwargs['entidad']
        n_financiamiento = self.kwargs.get('financiamiento', 0)        
        financiamiento = financiamiento_s(n_financiamiento)
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
            if carnet_file.size > max_size or asignacion_file.size > max_size or not carnet_file.name.endswith('.pdf') or not asignacion_file.name.endswith('.pdf'):
                if carnet_file.size > max_size:
                    form.add_error('carnet', 'El archivo carnet no debe superar los 2 MB.')
                if asignacion_file.size > max_size:
                    form.add_error('asignacion', 'El archivo de asignacion no debe superar los 2 MB.')                    
                if not carnet_file.name.endswith('.pdf'):
                    form.add_error('carnet', 'El archivo carnet debe ser en formato PDF.')
                if not asignacion_file.name.endswith('.pdf'):
                    form.add_error('asignacion', 'El archivo de asignación debe ser en formato PDF.')           
                return self.render_to_response(self.get_context_data(form=form, form2=form2))
            municipiobj.estado = 'SOLICITUD'
            municipiobj.save()
            encar_Mae = form.save(commit=False)
            persona_mae = form2.save()
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
            convocatoria = Convocatoria.objects.get(estado=True)
            postulacion_f = self.model.objects.create(
                municipio=municipiobj,
                mae=encar_Mae,
                responsable=responsablePr,
                convocatoria=convocatoria,
                tipo_financiamiento = n_financiamiento,
                creador = None,
            )
            id_post = postulacion_f.slug
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
        n_financiamiento = financiamiento_s(postulacion_p.tipo_financiamiento)
        context['financiamiento'] = n_financiamiento
        context['postulacion'] = postulacion_p
        context['titulo'] = 'Registro de encargado del proyecto'
        context['entity'] = 'Registro de encargado del proyecto'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        fecha = Convocatoria.objects.get(estado=True)
        context['convocatoria']=fecha
        fechaHoy = datetime.now()
        print(fechaHoy, 'fecha actual')
        fechalanzamiento = datetime.combine(fecha.fechaLanzamiento, fecha.horaLanzamiento)
        fechaCierre = datetime.combine(fecha.fechaCierre, fecha.horaCierre)
        context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
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
            postulacion_pr.fecha_ultimaconexion =  timezone.now()
            postulacion_pr.save()
            return HttpResponseRedirect(reverse('solicitud:Confirmacion_solicitud', args=[slug]))
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
        context['n_financiamiento'] = financiamiento_s(postulacion.tipo_financiamiento)
        fecha = Convocatoria.objects.get(estado=True)
        context['convocatoria']=fecha
        fechaHoy = datetime.now()
        print(fechaHoy, 'fecha actual')
        fechalanzamiento = datetime.combine(fecha.fechaLanzamiento, fecha.horaLanzamiento)
        fechaCierre = datetime.combine(fecha.fechaCierre, fecha.horaCierre)
        context['fecha_expiracion'] = fechaCierre.isoformat() if fechaCierre else None
        return context
    
class ListaCompleta(ListView):
    model = Postulacion
    template_name = 'Postulaciones/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA COMPLETA'
        context['activate'] = True
        context['entity'] = 'LISTA COMPLETA'
        context['object_list'] = self.model.objects.all()
        return context

class ListaSolicitudes(ListView):
    model = Postulacion
    template_name = 'Postulaciones/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA DE SOLICITUDES - ITCP'
        context['activate'] = True
        context['entity'] = 'LISTA DE SOLICITUDES - ITCP'
        context['object_list'] = self.model.objects.filter(estado=None).filter(tipo_financiamiento=1)
        return context

class ListaSolicitudesEJEC(ListView):
    model = Postulacion
    template_name = 'Postulaciones/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA DE SOLICITUDES - EDTP'
        context['activate'] = True
        context['entity'] = 'LISTA DE SOLICITUDES - EDTP'
        context['object_list'] = self.model.objects.filter(estado=None).filter(tipo_financiamiento=2)
        return context
    
class ListaRechazados(ListView):
    model = Postulacion
    template_name = 'Postulaciones/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA NO APROBADOS - ITCP'
        context['activate'] = True
        context['entity'] = 'LISTA NO APROBADOS - ITCP'
        context['object_list'] = self.model.objects.filter(estado=False).filter(tipo_financiamiento=1)
        return context
    
class ListaRechazadosEJEC(ListView):
    model = Postulacion
    template_name = 'Postulaciones/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA NO APROBADOS - EDTP'
        context['activate'] = True
        context['entity'] = 'LISTA NO APROBADOS - EDTP'
        context['object_list'] = self.model.objects.filter(estado=False).filter(tipo_financiamiento=2)
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
            else:
                context['password'] = 'La contraseña se generara automaticamente la cual sera: nombre de usuario + codigo'
        n_financiamiento = financiamiento_s(postulacion_p.tipo_financiamiento)
        context['financiamiento'] = n_financiamiento
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
        encargado = self.request.user
        responsable_pr = self.second_model.objects.get(slug = postulacion_pr.mae.slug)
        form = self.form_class(request.POST, instance = postulacion_pr)
        form2 = self.second_form_class(request.POST, request.FILES, instance = responsable_pr)
        form3 = self.third_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            carnet_file = form2.cleaned_data.get('carnet')
            asignacion_file = form2.cleaned_data.get('asignacion')
            max_size = 2 * 1024 * 1024
            if carnet_file.size > max_size or asignacion_file.size > max_size or not carnet_file.name.endswith('.pdf') or not asignacion_file.name.endswith('.pdf'):
                if carnet_file.size > max_size:
                    form2.add_error('carnet', 'El archivo carnet no debe superar los 2 MB.')
                if asignacion_file.size > max_size:
                    form2.add_error('asignacion', 'El archivo de asignacion no debe superar los 2 MB.')                    
                if not carnet_file.name.endswith('.pdf'):
                    form2.add_error('carnet', 'El archivo carnet debe ser en formato PDF.')
                if not asignacion_file.name.endswith('.pdf'):
                    form2.add_error('asignacion', 'El archivo de asignación debe ser en formato PDF.')           
                return self.render_to_response(self.get_context_data(form=form, form2=form2))
            form2.save()
            estado_post = form.cleaned_data.get('estado')
            if estado_post:
                postulacion = form.save(commit=False)
                postulacion.creador = encargado
                postulacion.save()
                if  form3.is_valid():
                    user_Pr = form3.save(commit=False)
                    user_Pr.password = '{}{}'.format(user_Pr.username, slug)
                    user_Pr.set_password(user_Pr.password)
                    user_Pr.is_municipio = True
                    user_Pr.save()
                    datos_proyecto = self.four_model.objects.create(
                        slug = slug,
                        user = user_Pr,
                        nombre = 'NOMBRE DEL PROYECTO',
                        comunidades = 'NOMBRE DE LAS COMUNIDADES',
                        tipologia_proy = False,
                        periodo_ejecu = '0'
                    )
                    postulacion_c = Postulacion.objects.get(slug=slug)
                    municipio_c = Municipios.objects.get(id=postulacion_c.municipio.id)
                    municipio_c.estado="APROBADO"
                    municipio_c.p_a=True
                    municipio_c.save()
                    if postulacion_c.tipo_financiamiento == 1:
                        return HttpResponseRedirect(reverse('proyecto:lista_inicio', args=[]))
                    else:
                        return HttpResponseRedirect(reverse('proyecto:lista_inicioEjec', args=[]))
                else:
                    return self.render_to_response(self.get_context_data(form=form, form2=form2 ))
            else:   
                postulacion = form.save(commit=False)
                postulacion.creador = encargado
                postulacion.save()
                postulacion_c = Postulacion.objects.get(slug=slug)
                municipio_c = Municipios.objects.get(id=postulacion_c.municipio.id)
                municipio_c.estado="NINGUNO"
                municipio_c.p_a=True
                municipio_c.save()
                return HttpResponseRedirect(reverse('solicitud:ListaRechazados', args=[]))
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
            return redirect('convocatoria:Index')

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
        context['entity_url'] = reverse_lazy('convocatoria:Index') 
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
            carnet_file = form2.cleaned_data.get('carnet')
            asignacion_file = form2.cleaned_data.get('asignacion')
            max_size = 2 * 1024 * 1024
            if carnet_file.size > max_size or asignacion_file.size > max_size or not carnet_file.name.endswith('.pdf') or not asignacion_file.name.endswith('.pdf'):
                if carnet_file.size > max_size:
                    form2.add_error('carnet', 'El archivo carnet no debe superar los 2 MB.')
                if asignacion_file.size > max_size:
                    form2.add_error('asignacion', 'El archivo de asignacion no debe superar los 2 MB.')                    
                if not carnet_file.name.endswith('.pdf'):
                    form2.add_error('carnet', 'El archivo carnet debe ser en formato PDF.')
                if not asignacion_file.name.endswith('.pdf'):
                    form2.add_error('asignacion', 'El archivo de asignación debe ser en formato PDF.')           
                return self.render_to_response(self.get_context_data(form=form, form2=form2))
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
        context['entity_url'] = reverse_lazy('convocatoria:Index') 
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
            form2.save()
            form3.save()
            postulacion_pr.modificacion = True
            postulacion_pr.save()
            return HttpResponseRedirect(reverse('solicitud:Confirmacion_solicitud', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))

    

