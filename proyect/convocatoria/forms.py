from django.forms import *
from django import forms
from tinymce.widgets import TinyMCE

from convocatoria.models import Convocatoria

class R_Convocatoria(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['estado'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'
        self.fields['elabEdtp'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'
        self.fields['EjecEdtp'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'
        self.fields['descripcion'].required = False
    fechaLanzamiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Definir formato de entrada
        label="FECHA DE LANZAMIENTO",
        required=True
    )
    fechaCierre = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Definir formato de entrada
        label="FECHA DE CIERRE",
        required=True
    )
    horaLanzamiento = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE LANZAMIENTO",
        required=True
    )
    horaCierre = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE CIERRE",
        required=True
    )
    montoElabEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO",
        required=False
    )
    montoEjecEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO",
        required=True
    )
    class Meta:
        model = Convocatoria
        fields = '__all__'
        exclude = ['slug', 'fecha_registro']
        labels = {
            'nombre': 'NOMBRE/TITULO',
            'descripcion': 'DESCRIPCION ADICIONAL',
            'estado': 'ESTADO (VIGENTE/NO VIGENTE)',
            'tamanoDoc' : 'TAMAÑO PERMITIDO POR DOCUMENTO',
            'extra' : 'SUBTITULO',
            'elabEdtp' : '¿HABILITAR?',
            'EjecEdtp' : '¿HABILITAR?',
            'documento' : 'DOCUMENTO DE LA CONVOCATORIA',
            'guia' : 'GUIA DE LLENADO',
            'guiaVideo' : 'VIDEO AYUDA',
            'banner' : 'BANNER DE LA CONVOCATORIA',
        }
        help_texts = {
            'tamanoDoc' : 'TAMAÑO PERMITIDO POR DOCUMENTO',
            'extra' : '(opcional) Ingrese alguna observacion/especificacion para la version de la convocatoria',
            'guiaVideo' : '(opcional) Ingrese la URL del video ayuda'
        }

    

class A_Convocatoria(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['estado'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'
        self.fields['elabEdtp'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'
        self.fields['EjecEdtp'].widget.attrs['class'] = 'form-check font-weight-bold border border-info'
        self.fields['descripcion'].required = False

    horaLanzamiento = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE LANZAMIENTO",
        required=True
    )
    horaCierre = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Usamos el tipo 'time' de HTML5
        label="HORA DE CIERRE",
        required=True
    )
    montoElabEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO",
        required=False,
        help_text="Ingrese el monto en caso de que se realice el financiamiento para la ELABORACION DEL ITCP <br>Introduce el monto máximo permitido por el FONABOSQUE. Ejemplo: 1000,00."
    )
    montoEjecEDTP = forms.DecimalField(
        max_digits=10,   # Total de dígitos
        decimal_places=2,  # Decimales
        widget=forms.NumberInput(attrs={'placeholder': '0.00'}),
        label="MONTO MAXIMO",
        required=True,
        help_text="Introduce el monto designado para la convocatoria (Ejemplo: 1000000,00)."
    )
    
    class Meta:
        model = Convocatoria
        fields = '__all__'
        exclude = ['slug', 'fecha_registro']
        labels = {
            'nombre': 'NOMBRE/TITULO',
            'descripcion': 'DESCRIPCION ADICIONAL',
            'fechaLanzamiento': 'FECHA DE LANZAMIENTO',
            'fechaCierre': 'FECHA DE CIERRE',
            'estado': 'ESTADO (VIGENTE/NO VIGENTE)',
            'tamanoDoc' : 'TAMAÑO PERMITIDO POR DOCUMENTO',
            'elabEdtp' : '¿HABILITAR?',
            'EjecEdtp' : '¿HABILITAR?',
            'documento' : 'DOCUMENTO DE LA CONVOCATORIA',
            'guia' : 'GUIA DE LLENADO',
            'guiaVideo' : 'VIDEO AYUDA',
            'banner' : 'BANNER DE LA CONVOCATORIA',
        }
        help_texts = {
            'tamanoDoc' : 'TAMAÑO PERMITIDO POR DOCUMENTO PARA EL ITCP-DECLARACION JURADA',
            'descripcion' : '(opcional) Ingrese alguna observacion/especificacion para la convocatoria',
            'guiaVideo' : '(opcional) Ingrese la URL del video ayuda'
        }
