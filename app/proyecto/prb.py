
class R_Modelo_Acta(CreateView):
    model=Modelo_Acta
    template_name = 'Proyecto/R_Modelo_acta01.html'
    form_class = R_ModeloActa

    def get_context_data(self, **kwargs):
        context = super(R_Modelo_Acta, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        proyecto_p = Postulacion.objects.get(slug=slug)
        context['proyecto'] = proyecto_p
        context['titulo'] = 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO'
        context['entity'] = 'REGISTRO DATOS DEL PROYECTO'
        context['entity2'] = 'ITCP-MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO'
        context['accion'] = 'Registrar'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        slug = self.kwargs.get('slug', None)
        comunidades_list = request.POST.getlist('comunidades')  
        si_acta_files = request.FILES.getlist('si_acta')  
        no_acta_texts = request.POST.getlist('no_acta')    # Lista de justificaciones

        print("Comunidades:", comunidades_list)
        print("Actas:", si_acta_files)
        print("No Actas:", no_acta_texts)

        # Verifica que las listas de comunidades y no_acta tengan la misma longitud
        for index in range(len(comunidades_list)):
            print('index', index)
            comunidad = comunidades_list[index]
            si_acta = si_acta_files[index] if index < len(si_acta_files) else None
            no_acta = no_acta_texts[index] if index < len(no_acta_texts) else None

            print('Ingreso al for para la comunidad:', comunidad)

            # Validación: si se sube un archivo, no se puede añadir justificación
            '''
            if si_acta and no_acta:
                print('Error: no se puede tener justificación si se ha subido un acta.')
                return self.form_invalid(form=None)  # Maneja el error de forma adecuada           
            '''
            if comunidad:
                print('Creando objeto para:', comunidad)
                # Crea el objeto solo si la comunidad no está vacía
                self.model.objects.create(
                    slug=slug,
                    comunidades=comunidad,
                    si_acta=si_acta if si_acta else None,
                    no_acta=no_acta if not si_acta else no_acta  # Asigna no_acta si no hay si_acta
                )

        print('Finalizado')
        return HttpResponseRedirect(reverse('proyecto:actualizar_obj_especifico', args=[slug]))