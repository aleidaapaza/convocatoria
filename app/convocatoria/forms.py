from django.forms import *
from django import forms

from convocatoria.models import Convocatoria

class R_Convocatoria(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['estado'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'

    fechaLanzamiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Definir formato de entrada
        label="FECHA DE LANZAMIENTO DE LA CONVOCATORIA",
        required=True
    )
    fechaCierre = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Definir formato de entrada
        label="FECHA DE CIERRE DE LA CONVOCATORIA",
        required=True
    )
    horaLanzamiento = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE LANZAMIENTO DE LA CONVOCATORIA",
        required=True
    )
    horaCierre = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE CIERRE DE LA CONVOCATORIA",
        required=True
    )
    montoElabEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO POR PARTE DEL FONABOSQUE PARA LA ELABORACION DEL EDTP",
        required=True
    )
    montoEjecEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO POR PARTE DEL FONABOSQUE PARA LA EJECUCION DEL EDTP",
        required=True
    )
    class Meta:
        model = Convocatoria
        fields = '__all__'
        exclude = ['slug', 'fecha_registro']
        labels = {
            'nombre': 'NOMBRE DE LA CONVOCATORIA',
            'estado': 'ESTADO DE LA CONVOCATORIA (VIGENTE/NO VIGENTE)',
        }

class A_Convocatoria(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['estado'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'

    horaLanzamiento = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE LANZAMIENTO DE LA CONVOCATORIA",
        required=True
    )
    horaCierre = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE CIERRE DE LA CONVOCATORIA",
        required=True
    )
    montoElabEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO POR PARTE DEL FONABOSQUE PARA LA ELABORACION DEL EDTP",
        required=True
    )
    montoEjecEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO POR PARTE DEL FONABOSQUE PARA LA EJECUCION DEL EDTP",
        required=True
    )
    '''
    estado = forms.BooleanField(
        label="ESTADO DE LA CONVOCATORIA (VIGENTE/NO VIGENTE)",  # Etiqueta del campo
        initial=False,  # Valor inicial (el checkbox estará desmarcado por defecto)
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'})  # Usamos un widget tipo checkbox
    )
    '''
    
    class Meta:
        model = Convocatoria
        fields = '__all__'
        exclude = ['slug', 'fecha_registro']
        labels = {
            'nombre': 'NOMBRE DE LA CONVOCATORIA',
            'fechaLanzamiento': 'FECHA DE LANZAMIENTO DE LA CONVOCATORIA',
            'fechaCierre': 'FECHA DE CIERRE DE LA CONVOCATORIA',
            'estado': 'ESTADO DE LA CONVOCATORIA (VIGENTE/NO VIGENTE)',
        }
    