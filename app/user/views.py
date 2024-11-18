# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, View, ListView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from user.form import UsuarioRev, Reg_Persona_MAE, LoginForm, update_Revisor
from user.models import Revisor, User, Persona


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        activate = True
        entity = 'Inicio de sesion'
        return render(request, 'login/login.html', {'form': form, 'activate':activate, 'entity':entity})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ''
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! inicio sesion'
                return redirect('convocatoria:Index')
            else:
                message = 'Error al iniciar sesion. Verificar que el usuario y la contraseña hayan sido introducidas de la manera correcta'

        return render(request, 'login/login.html', context={'form': form, 'message': message})

def cierreSesion(request):
    logout(request)
    messages.success(request, 'sesion finalizada exitosamente')
    return redirect('convocatoria:Index')

class ListaRevisores(ListView):
    model = Revisor
    template_name = 'perfil/listaRevisores.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTA DE REVISORES'
        context['activate'] = True
        context['entity'] = 'LISTA DE REVISORES'
        context['object_list'] = self.model.objects.all()
        context['entity_registro'] = reverse_lazy('user:Registro_Revisor', args=[])
        context['entity_registro_nom'] = 'REGISTRAR REVISORES'
        return context

class RegistroRev(CreateView):
    model = Revisor
    template_name = 'login/registerRev.html'
    form_class = UsuarioRev
    second_form_class = Reg_Persona_MAE
    success_url = reverse_lazy('user:lista_revisor')

    def get_context_data(self, **kwargs):
        context = super(RegistroRev, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)

        context['form'] = self.form_class(self.request.GET)
        context['form2'] = self.second_form_class(self.request.GET)      
        context['titulo'] = 'REGISTRO DE REVISORES'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        context['activate'] = True
        context['entity'] = 'REGISTRO DE REVISORES'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            usuario = form.save(commit=False)
            usuario.is_revisor = True
            usuario.password = '{}{}'.format(usuario.username[:5], 'RV2024')
            usuario.set_password(usuario.password)
            usuario.save()
            persona = form2.save()
            Revisor.objects.create(
                persona=persona,
                user=usuario,
            )
            return HttpResponseRedirect(reverse('user:lista_revisor', args=[]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2,))

class ActualizacionRev(UpdateView):
    model = Revisor
    second_model = User 
    third_model = Persona
    template_name = 'perfil/act_revisor.html'
    form_class = update_Revisor
    second_form_class = UsuarioRev
    third_form_class = Reg_Persona_MAE

    def get_context_data(self, **kwargs):
        context = super(ActualizacionRev, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)        
        revisor_p = self.model.objects.get(slug=slug)
        user_p = self.second_model.objects.get(id=revisor_p.user.pk)
        persona_p = self.third_model.objects.get(id=revisor_p.persona.pk)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=user_p)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(instance=persona_p)

        context['rol'] = revisor_p
        context['titulo'] = 'ACTUALIZAR DATOS DEL REVISOR'
        context['activate'] = False
        context['entity'] = 'ACTUALIZAR DATOS DEL REVISOR'
        context['accion2'] = 'Cancelar'
        context['accion2_url'] = reverse_lazy('convocatoria:Index')
        context['entity'] = 'REGISTRO DE REVISORES'
        context['entity_url'] = reverse_lazy('convocatoria:Index') 
        return context 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get('slug', None)
        revisor_p = self.model.objects.get(slug=slug)
        user_p = self.second_model.objects.get(id=revisor_p.user.pk)
        persona_p = self.third_model.objects.get(id=revisor_p.persona.pk)
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, request.FILES, instance=user_p)
        form3 = self.third_form_class(request.POST, instance=persona_p)

        if form2.is_valid() and form3.is_valid():          
            form2.save()
            form3.save()
            return HttpResponseRedirect(reverse('solicitud:Actualizar_Ficha_eNC', args=[slug]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))