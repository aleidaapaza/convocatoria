from django.forms import *
from django import forms

from proyecto.models import DatosProyectoBase, Justificacion

class Reg_DatosBase(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['tipologia_proy'].widget.attrs['class'] = 'form-check-input'
        self.fields['solicitud_financ'].widget.attrs['class'] = 'form-check-input'
        
    class Meta:
        model = DatosProyectoBase
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'user']
        labels = {
            'nombre': 'NOMBRE DEL PROYECTO',
            'n_comunidades': 'N° DE COMUNIDADES BENEFICIARIAS DEL PROYECTO',
            'comunidades': 'COMUNIDADES BENEFICIARIAS DEL PROYECTO',
            'tipologia_proy': 'TIPOLOGIA DEL PROYECTO',
            'periodo_ejecu': 'PERIODO DE EJECUCION DEL PROYECTO (EN AÑOS)',
            'solicitud_financ': 'SOLICITUD DE FINANCIAMIENTO PARA LA FORMULACION DEL EDTP',
        }

class Reg_Justificacion(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-check-input border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Justificacion
        fields = '__all__'
        exclude = ['slug','fecha_registro']
        labels = {
            'justificacion1': '¿EL PROYECTO ESTA ACORDE A LOS PRINCIPIOS Y DERECHOS ESTABLECIDOS EN CONSTITUCIÓN POLÍTICA DEL ESTADO?',
            'justificacion2': '¿EL PROYECTO ESTA ACORDE A LOS LINEAMIENTOS DE LA AGENDA PATRIÓTICA 2025 Y LA LEY N° 300 MARCO DE LA MADRE TIERRA Y DESARROLLO INTEGRAL PARA VIVIR BIEN?',
            'justificacion3': '¿EL PROYECTO ESTA ACORDE A LA NORMATIVA DEL PLAN SECTORIAL DE DESARROLLO INTEGRAL DEL MINISTERIO DE MEDIO AMBIENTE Y AGUA?',
            'justificacion4': '¿EL PROYECTO ESTA ACORDE A LA NORMATIVA DE LA LEY DE AUTONOMÍAS Y DESCENTRALIZACIÓN "ANDRES IBAÑEZ"?',
            'justificacion5': '¿EL PROYECTO ESTA ACORDE A LA NORMATIVA DE LA LEY FORESTAL?',
            'justificacion6': '¿EL PROYECTO ESTA ACORDE AL PLAN TERRITORIAL DE DESARROLLO INTEGRAL (PTDI)?',
            'justificacion7': '¿EL PROYECTO ESTÁ DENTRO DE LA NORMATIVA DE LOS PLANES DE GESTIÓN TERRITORIAL COMUNITARIA (PGTC)?',
        }