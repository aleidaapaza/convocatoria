# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, View
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from user.form import UsuarioRev, Reg_Persona_MAE, LoginForm
from user.models import Revisor

class RegistroRev(CreateView):
    model = Revisor
    template_name = 'login/registerRev.html'
    form_class = UsuarioRev
    second_form_class = Reg_Persona_MAE
    success_url = reverse_lazy('solicitud:Index')

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
        context['accion2_url'] = reverse_lazy('solicitud:Index')
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
            return HttpResponseRedirect(reverse('solicitud:Index', args=[]))
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2,))
        
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
                return redirect('solicitud:Index')
            else:
                message = 'Error al iniciar sesion. Verificar que el usuario y la contraseña hayan sido introducidas de la manera correcta'

        return render(request, 'login/login.html', context={'form': form, 'message': message})

def cierreSesion(request):
    logout(request)
    messages.success(request, 'sesion finalizada exitosamente')
    return redirect('solicitud:Index')
