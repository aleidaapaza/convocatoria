from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Persona, EncargadoMAE, ResponsableP, User, Revisor

class Reg_Persona_MAE(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['style'] = 'text-transform:uppercase'
        self.fields['apellido'].widget.attrs['style'] = 'text-transform:uppercase'
        self.fields['cargo'].widget.attrs['style'] = 'text-transform:uppercase'
    class Meta:
        model = Persona
        fields = '__all__'
        exclude = []
        labels = {
            'nombre': 'Nombre(s) de la MAE',
            'apellido': 'Apellido(s)',
            'cargo': 'Cargo',
            'celular': 'N° de Celular',
        }

class Reg_Persona_Res(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['style'] = 'text-transform:uppercase'
        self.fields['apellido'].widget.attrs['style'] = 'text-transform:uppercase'
        self.fields['cargo'].widget.attrs['style'] = 'text-transform:uppercase'
    class Meta:
        model = Persona
        fields = '__all__'
        exclude = []
        labels = {
            'nombre': 'Nombre(s) del Responsable',
            'apellido': 'Apellido(s)',
            'cargo': 'Cargo',
            'celular': 'N° de Celular',
        }

class Reg_EncargadoMAE(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
    class Meta:
        model = EncargadoMAE
        fields = '__all__'
        exclude = ['slug', 'persona']
        labels = {
            'carnet': 'Carnet de Indentidad MAE (escaneado en pdf y tamaño máximo 2 megas)',
            'asignacion': 'Documento de Designación y NIT del GAM (escaneado en pdf y tamaño máximo 2 megas)',
            'correo': 'Correo Electrónico Domicilio Legal para notificación'
        }
    def clean_documento(self):
        carnetd = self.cleaned_data.get('carnet')
        asignaciond = self.cleaned_data.get('asignacion')
        if carnetd:
            # Verifica el tamaño del archivo
            if carnetd.size > 2 * 1024 * 1024:  # 2 MB en bytes
                raise ValidationError("El archivo Carnet no puede exceder los 2 MB.")
        if asignaciond:
            # Verifica el tamaño del archivo
            if asignaciond.size > 2 * 1024 * 1024:  # 2 MB en bytes
                raise ValidationError("El archivo Asignacion no puede exceder los 2 MB.")

        return carnetd, asignaciond

class Reg_ResponsableP(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
    class Meta:
        model = ResponsableP
        fields = '__all__'
        exclude = ['slug', 'persona']
        labels = {
            'correo': 'Correo Electrónico',
            }

class UsuarioRev(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Nombre de Usuario',
        }

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    username = forms.CharField(max_length=150, label='Nombre de Usuario', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}))
    password = forms.CharField(max_length=255, label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))
