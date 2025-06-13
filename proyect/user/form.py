from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Persona, EncargadoMAE, ResponsableP, User, Revisor

class Reg_Persona_Rev(ModelForm):
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
            'nombre': 'Nombre(s)',
            'apellido': 'Apellido(s)',
            'cargo': 'Cargo',
            'celular': 'Carnet',
        }
        
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
            'apellido': 'Apellido(s) de la MAE',
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
            'apellido': 'Apellido(s) del Responsable',
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
            'carnet': 'Carnet de Indentidad MAE',
            'asignacion': 'Documento de Designación y NIT del GAM',
            'correo': 'Correo Electrónico Domicilio Legal para notificación'
        }

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
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
        self.fields['vl_revisores'].widget.attrs['class'] = 'form-check-input'
        self.fields['vl_convocatoria'].widget.attrs['class'] = 'form-check-input'
        self.fields['v_registrarMun'].widget.attrs['class'] = 'form-check-input'
        self.fields['v_habilitarMun'].widget.attrs['class'] = 'form-check-input'
        self.fields['v_revSolicitud'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = User
        fields = ['username','is_active','vl_revisores', 'vl_convocatoria', 'v_registrarMun', 'v_habilitarMun', 'v_revSolicitud']
        labels = {
            'username': 'Nombre de Usuario',
            'is_active': 'Usuario Activo',
            'vl_revisores': 'Ver lista de revisores',
            'vl_convocatoria': 'Ver informacion de las convocatorias',
            'v_registrarMun': 'Registrar usuario/contraseña a municipios',
            'v_habilitarMun': 'Habilitar el acceso a municipio(s)',
            'v_revSolicitud': 'Revision de las solicitudes de postulacion',
        }

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    username = forms.CharField(max_length=150, label='Nombre de Usuario', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}))
    password = forms.CharField(max_length=255, label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))

class Update_MAE(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['carnet'].required = False
        self.fields['asignacion'].required = False

    class Meta:
        model = EncargadoMAE
        fields = '__all__'
        exclude = ['slug', 'persona', 'correo']
        labels = {
            'carnet': 'Carnet de Indentidad MAE (escaneado en pdf y tamaño máximo 2 megas)',
            'asignacion': 'Documento de Designación y NIT del GAM (escaneado en pdf y tamaño máximo 2 megas)',
        }
        

class User_Reg(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Nombre de Usuario',
        }

        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Nombre de Usuario',
                }
            ),
        }

class update_Revisor(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Revisor
        exclude = '__all__'
        