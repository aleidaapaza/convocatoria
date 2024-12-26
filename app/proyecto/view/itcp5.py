import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.utils import timezone
from django.conf import settings
from solicitud.models import Postulacion
from proyecto.models import Derecho_propietario
from django.contrib import messages


class R_Derecho_propietario(View):
    model = Derecho_propietario
    template_name = 'Proyecto/R_DerechoPropietario.html'
    
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if self.model.objects.filter(slug=slug).exists():
            return redirect('proyecto:actualizar_DerechoPropietario', slug=slug)
        return self.render_form(slug)

    def render_form(self, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        context = {
            'proyecto': proyecto_p,
            'titulo': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
            'accion': 'Registrar',
            'accion2': 'Cancelar',
            'accion2_url': reverse_lazy('convocatoria:Index'),
            'error_messages': []  # Inicializa una lista vacía para los mensajes de error
        }
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Obtener el slug de los argumentos de la URL
        slug = self.kwargs.get('slug', None)
        
        error_messages = []
        index = 0

        # Iterar a través de los datos enviados por el formulario
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

        # Si hubo errores, retornar al formulario con los mensajes de error
        if error_messages:
            context = self.render_form(slug)
            context['error_messages'] = error_messages
            return context

        # Si no hubo errores, redirigir al usuario a la página de actualización
        return HttpResponseRedirect(reverse('proyecto:registro_ImpactoAmbiental', args=[slug]))

class A_Derecho_propietario(View):
    model = Derecho_propietario
    template_name = 'Proyecto/A_DerechoPropietario.html'

    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        objetivos = Derecho_propietario.objects.filter(slug=slug)  # Objetivos de DerechoPropietario

        # Formatear easting y northing para mostrar con 3 decimales
        for objetivo in objetivos:
            if objetivo.easting is not None:
                objetivo.easting = f"{objetivo.easting:.3f}"  # Formato con 3 decimales
            if objetivo.northing is not None:
                objetivo.northing = f"{objetivo.northing:.3f}"  # Formato con 3 decimales

        context = {
            'proyecto': proyecto_p,
            'derecho': objetivos,
            'titulo': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
            'entity': 'REGISTRO DATOS DEL PROYECTO',
            'entity2': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
            'accion': 'Actualizar',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'entity_registro': reverse_lazy('proyecto:registro_DerechoPropietario_R', args=[slug]),
            'entity_registro_nom': 'Registrar',
            'error_messages': [],  # Inicializa los mensajes de error
        }
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
        return render(request, self.template_name, context)

    def post(self, request, slug):
        print('Ingreso de post')
        descripcion_list = []
        si_registro_files = []
        no_registro_texts = []
        zone_list = []
        easting_list = []
        northing_list = []
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
                break  # No hay más datos, salimos del ciclo

            # Almacenar los datos del formulario para su posterior procesamiento
            descripcion_list.append(descripcion)
            si_registro_files.append(si_registro)
            no_registro_texts.append(no_registro)
            zone_list.append(zone)
            easting_list.append(easting)
            northing_list.append(northing)

            index += 1

        # Validación de tamaño de archivo
        for si_acta in si_registro_files:
            if si_acta and si_acta.size > 2 * 1024 * 1024:  # 2 MB
                error_messages.append('El archivo no debe superar los 2 MB.')

        if error_messages:
            # Si hay errores, re-renderizar el formulario con los mensajes de error
            proyecto_p = get_object_or_404(Postulacion, slug=slug)
            objetivos = Derecho_propietario.objects.filter(slug=slug)
            context = {
                'proyecto': proyecto_p,
                'derecho': objetivos,
                'titulo': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
                'entity': 'REGISTRO DATOS DEL PROYECTO',
                'entity2': 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES)',
                'accion': 'Actualizar',
                'accion2': 'Cancelar',
                'accion2_url': reverse('convocatoria:Index'),
                'entity_registro': reverse_lazy('proyecto:registro_DerechoPropietario_R', args=[slug]),
                'entity_registro_nom': 'Registrar',
                'error_messages': error_messages,  # Pasar los mensajes de error al contexto
            }
            return render(request, self.template_name, context)

        # Actualizar los registros en la base de datos
        for i in range(len(descripcion_list)):
            descripcion = descripcion_list[i]
            si_registro = si_registro_files[i]
            no_registro = no_registro_texts[i]
            zone = zone_list[i]
            easting = easting_list[i]
            northing = northing_list[i]

            # Validar los valores de georreferencia
            try:
                zone = int(zone)  # Asegúrate de que zone sea un entero
                easting = float(easting)  # Asegúrate de que easting sea un número flotante
                northing = float(northing)  # Asegúrate de que northing sea un número flotante
            except ValueError:
                error_messages.append("Los valores de georreferencia (ZONA, ESTE, NORTE) no son válidos.")
                continue  # Salta al siguiente ciclo si los valores no son válidos

            if descripcion:
                # Usar update_or_create para actualizar o crear nuevos objetos
                acta_instance, created = Derecho_propietario.objects.update_or_create(
                    slug=slug,
                    descripcion=descripcion,
                    defaults={
                        'si_registro': si_registro,
                        'no_registro': no_registro,
                        'zone': zone,
                        'easting': easting,
                        'northing': northing,
                        'fecha_actualizacion': timezone.now(),
                    }
                )

                if not created:
                    # Si la instancia ya existía, actualizar los campos
                    if si_registro:
                        print("eliminar", si_registro)
                        # Eliminar el archivo anterior si existe
                        if acta_instance.si_registro:
                            file_path = os.path.join(settings.MEDIA_ROOT, str(acta_instance.si_registro))
                            if os.path.isfile(file_path):
                                os.remove(file_path)  # Eliminar el archivo antiguo

                        acta_instance.si_registro = si_registro  # Asignar el nuevo archivo

                    if no_registro is not None:  # Permitir actualizar no_registro incluso si está vacío
                        acta_instance.no_registro = no_registro

                    # Actualizar los campos de georreferencia
                    acta_instance.zone = zone
                    acta_instance.easting = easting
                    acta_instance.northing = northing

                acta_instance.save()

        # Redirigir después de actualizar
        messages.success(request, 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES) - se actualizo correctamente.')
        return redirect('proyecto:registro_ImpactoAmbiental', slug=slug)
    
def descargar_archivo_der(request, slug, id):
    #documento = get_object_or_404(Modelo_Acta, slug=slug)
    documento = Derecho_propietario.objects.get(id=id)
    response = HttpResponse(documento.si_registro, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{documento.si_registro.name}"'
    return response

def eliminar_Derecho(request, objetivo_id):
    if request.method == 'POST':
        objeto = Derecho_propietario.objects.get(id=objetivo_id)
        slug = objeto.slug
        objetivo = get_object_or_404(Derecho_propietario, id=objetivo_id)
        objetivo.delete()
        return redirect('proyecto:actualizar_DerechoPropietario', slug=slug)

class R_Derecho_propietario_R(View):
    model = Derecho_propietario
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
            'accion2_url': reverse_lazy('convocatoria:Index'),
            'error_messages': []  # Inicializa una lista vacía para los mensajes de error
        }
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
        # Renderiza el template con el contexto
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Obtener el slug de los argumentos de la URL
        slug = self.kwargs.get('slug', None)
        
        error_messages = []
        index = 0

        # Iterar a través de los datos enviados por el formulario
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

        # Si hubo errores, retornar al formulario con los mensajes de error
        if error_messages:
            context = self.render_form(slug)
            context['error_messages'] = error_messages
            return context
        messages.success(request, 'ITCP-ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO Y/O TITULO EJECUTORIAL (MANEJO INTEGRAL SUSTENTABLE DE BOSQUES) - se añadio correctamente.')
        # Si no hubo errores, redirigir al usuario a la página de actualización
        return HttpResponseRedirect(reverse('proyecto:actualizar_DerechoPropietario', args=[slug]))
