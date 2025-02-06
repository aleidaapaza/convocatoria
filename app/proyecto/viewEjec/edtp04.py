import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, UpdateView
from django.utils import timezone
from django.conf import settings
from django.contrib import messages

from solicitud.models import Postulacion
from proyecto.models import Derecho_propietario, UbicacionGeografica

from proyecto.forms import R_Ubicacion

class R_DerechoPropietarioE(View):
    model = UbicacionGeografica
    second_model = Derecho_propietario
    template_name = 'Proyecto/Ejec/R_DerechoPropietario.html'
    form = R_Ubicacion

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if self.model.objects.filter(slug=slug).exists():
            return redirect('proyecto:actualizar_DerechoPropietarioE', slug=slug)
        return self.render_form(slug)
    
    def render_form(self, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        form = self.form(self.request.GET)
        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'form' : form,
            'titulo': 'UBICACION POSICION GEOGRAFICA',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'UBICACION POSICION GEOGRAFICA',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse_lazy('convocatoria:Index'),
        }
        return render(self.request, self.template_name, context)
    
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
                break 
            if si_registro and si_registro.size > 2 * 1024 * 1024:  # 2 MB
                error_messages.append('El archivo no debe superar los 2 MB.')
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
            context = self.render_form(slug)
            context['error_messages'] = error_messages
            return context
        form = self.form(request.POST)
        if form.is_valid():
            ubicacion = form.save(commit=False)
            ubicacion.slug = slug
            ubicacion.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return HttpResponseRedirect(reverse('proyecto:registro_PresupuestoRef', args=[slug]))
    
class A_DerechoPropietarioE(UpdateView):
    model = UbicacionGeografica
    form_class = R_Ubicacion
    template_name = 'Proyecto/Ejec/A_DerechoPropietario.html'

    def get_object(self, queryset=None):
        return get_object_or_404(UbicacionGeografica, slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs): #Añadir datos adicionales al contexto para el template.
        context = super().get_context_data(**kwargs)
        proyecto_p = get_object_or_404(Postulacion, slug=self.kwargs['slug'])
        objetivos = Derecho_propietario.objects.filter(slug=self.kwargs['slug'])

        for objetivo in objetivos:
            if objetivo.easting is not None:
                objetivo.easting = f"{objetivo.easting:.3f}"  # Formato con 3 decimales
            if objetivo.northing is not None:
                objetivo.northing = f"{objetivo.northing:.3f}"  # Formato con 3 decimales

        context.update({
            'proyecto': proyecto_p,
            'postulacion': proyecto_p,
            'derecho': objetivos,
            'titulo': 'UBICACION POSICION GEOGRAFICA',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'UBICACION POSICION GEOGRAFICA',
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse_lazy('convocatoria:Index'),
            'entity_registro': reverse_lazy('proyecto:agregar_DerechoPropietarioE', args=[self.kwargs['slug']]),
            'entity_registro_nom': 'Registrar',
            'error_messages': [],  # Inicializa los mensajes de error
        })

        # Manejo de mensajes de Django
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
    
    def form_valid(self, form):
        print("Formulario válido")
        slug = self.kwargs['slug']
        ubicacion = form.save(commit=False)
        ubicacion.fecha_actualizacion = timezone.now()  # Actualizar la fecha de modificación
        ubicacion.save()
        # Guardar la información relacionada con Derecho_propietario
        error_messages = []

        id_list = []
        descripcion_list = []
        si_registro_files = []
        no_registro_texts = []
        zone_list = []
        easting_list = []
        northing_list = []

        index = 0
        while True:
            idn = self.request.POST.get(f'id_{index}')
            descripcion = self.request.POST.get(f'descripcion_{index}')
            si_registro = self.request.FILES.get(f'si_registro_{index}')
            no_registro = self.request.POST.get(f'no_registro_{index}')
            zone = self.request.POST.get(f'zone_{index}')
            easting = self.request.POST.get(f'easting_{index}')
            northing = self.request.POST.get(f'northing_{index}')

            if descripcion is None:
                break  # No hay más datos, salimos del ciclo

            # Almacenar los datos del formulario para su posterior procesamiento
            id_list.append(idn)
            descripcion_list.append(descripcion)
            si_registro_files.append(si_registro)
            no_registro_texts.append(no_registro)
            zone_list.append(zone)
            easting_list.append(easting)
            northing_list.append(northing)

            index += 1

        for si_acta in si_registro_files:
            if si_acta and si_acta.size > 2 * 1024 * 1024:  # 2 MB
                error_messages.append('El archivo no debe superar los 2 MB.')

        for i in range(len(id_list)):  # Recorrer todas las filas dinámicas
            idn = id_list[i]
            descripcion = descripcion_list[i]
            si_registro = si_registro_files[i]
            no_registro = no_registro_texts[i]
            zone = zone_list[i]
            easting = easting_list[i]
            northing = northing_list[i]

            try:
                zone = int(zone)
                easting = float(easting)
                northing = float(northing)
            except ValueError:
                error_messages.append("Los valores de georreferencia (ZONA, ESTE, NORTE) no son válidos.")
                continue
            if Derecho_propietario.objects.filter(id=idn).exists():
                derecho_obj = Derecho_propietario.objects.get(id=idn)
                derecho_obj.descripcion = descripcion
                derecho_obj.si_registro = si_registro if si_registro else derecho_obj.si_registro  # Si no se sube un nuevo archivo, conserva el actual
                derecho_obj.no_registro = no_registro
                derecho_obj.zone = zone
                derecho_obj.easting = easting
                derecho_obj.northing = northing
                derecho_obj.fecha_actualizacion = timezone.now()
                derecho_obj.save()  # Asegúrate de guardar el objeto después de asignar los campos
            else:
                # Si no existe, crea un nuevo objeto
                Derecho_propietario.objects.create(
                    descripcion=descripcion,
                    si_registro=si_registro,
                    no_registro=no_registro,
                    zone=zone,
                    easting=easting,
                    northing=northing,
                    fecha_actualizacion=timezone.now(),
                )


        # Si hay mensajes de error, manejarlos
        if error_messages:
            proyecto_p = get_object_or_404(Postulacion, slug=slug)
            objetivos = Derecho_propietario.objects.filter(slug=slug)
            context = {
                'proyecto': proyecto_p,
                'postulacion' : proyecto_p,
                'derecho': objetivos,
                'titulo': 'UBICACION POSICION GEOGRAFICA',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'UBICACION POSICION GEOGRAFICA',
                'accion': 'Actualizar',
                'accion2': 'Cancelar',
                'accion2_url': reverse('convocatoria:Index'),
                'entity_registro': reverse_lazy('proyecto:agregar_DerechoPropietarioE', args=[slug]),
                'entity_registro_nom': 'Registrar',
                'error_messages': error_messages,  # Pasar los mensajes de error al contexto
            }
            return render(self.request, self.template_name, context)
        else:
            messages.success(self.request, 'UBICACION POSICION GEOGRAFICA - se añadio correctamente.')
            return redirect('proyecto:registro_PresupuestoRef', slug=slug)

    def form_invalid(self, form):
        """
        Acción a realizar si el formulario es inválido.
        """
        messages.error(self.request, 'Ocurrió un error al actualizar la información.')
        return self.render_to_response(self.get_context_data(form=form))

def eliminar_DerechoE(request, objetivo_id):
    if request.method == 'POST':
        objeto = Derecho_propietario.objects.get(id=objetivo_id)
        slug = objeto.slug
        objetivo = get_object_or_404(Derecho_propietario, id=objetivo_id)
        objetivo.delete()
        return redirect('proyecto:actualizar_DerechoPropietarioE', slug=slug)
    
class R_DerechoPropietarioER(View):
    model = Derecho_propietario
    template_name = 'Proyecto/Ejec/R_DerechoPropietarioR.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        context = {
            'proyecto': proyecto_p,
            'postulacion' : proyecto_p,
            'titulo': 'UBICACION POSICION GEOGRAFICA',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'UBICACION POSICION GEOGRAFICA',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse_lazy('convocatoria:Index'),
        }
        return render(self.request, self.template_name, context)
    
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
                break 
            if si_registro and si_registro.size > 2 * 1024 * 1024:  # 2 MB
                error_messages.append('El archivo no debe superar los 2 MB.')
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
            context = self.render_form(slug)
            context['error_messages'] = error_messages
            return context
        
        return HttpResponseRedirect(reverse('proyecto:actualizar_DerechoPropietarioE', args=[slug]))
    