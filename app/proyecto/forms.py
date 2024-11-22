from django.forms import *
from django import forms

from proyecto.models import (DatosProyectoBase, Justificacion, Idea_Proyecto, Objetivo_especifico, Beneficiario,
                             Modelo_Acta, Impacto_ambiental, Riesgo_desastre, Detalle_POA,
                             Conclusion_recomendacion, Declaracion_jurada)

from proyecto.choices import riesgos, nivel

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
        exclude = ['slug','fecha_registro', 'fecha_actualizacion']
        labels = {
            'justificacion1': '¿EL PROYECTO ESTA ACORDE A LOS PRINCIPIOS Y DERECHOS ESTABLECIDOS EN CONSTITUCIÓN POLÍTICA DEL ESTADO?',
            'justificacion2': '¿EL PROYECTO ESTA ACORDE A LOS LINEAMIENTOS DE LA AGENDA PATRIÓTICA 2025 Y LA LEY N° 300 MARCO DE LA MADRE TIERRA Y DESARROLLO INTEGRAL PARA VIVIR BIEN?',
            'justificacion3': '¿EL PROYECTO ESTA ACORDE A LA NORMATIVA DEL PLAN SECTORIAL DE DESARROLLO INTEGRAL DEL MINISTERIO DE MEDIO AMBIENTE Y AGUA?',
            'justificacion4': '¿EL PROYECTO ESTA ACORDE A LA NORMATIVA DE LA LEY DE AUTONOMÍAS Y DESCENTRALIZACIÓN "ANDRES IBAÑEZ"?',
            'justificacion5': '¿EL PROYECTO ESTA ACORDE A LA NORMATIVA DE LA LEY FORESTAL?',
            'justificacion6': '¿EL PROYECTO ESTA ACORDE AL PLAN TERRITORIAL DE DESARROLLO INTEGRAL (PTDI)?',
            'justificacion7': '¿EL PROYECTO ESTÁ DENTRO DE LA NORMATIVA DE LOS PLANES DE GESTIÓN TERRITORIAL COMUNITARIA (PGTC)?',
        }

class R_Idea_Proyecto(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        
    class Meta:
        model = Idea_Proyecto
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion', 'beneficios_alter']
        labels = {
            'antecedente': 'ANTECEDENTES',
            'diagnostico': 'DIAGNOSTICO DEL PROYECTO',
            'planteamiento_problema': 'PLANTEAMIENTO DEL PROBLEMA / NECESIDADES A RESOLVER CON EL PROYECTO',
            'actores_involucrados': 'ACTORES INVOLUCRADOS',
            'alternativa_1': 'ALTERNATIVA DE SOLUCIÓN 1',
            'alternativa_2': 'ALTERNATIVA DE SOLUCIÓN 2',
            'elige_alternativa': '¿ALTERNATIVA QUE SE ELIGE?',
            'justificacion_alter': 'JUSTIFICACIÓN DE LA ALTERNATIVA ELEGIDA',
            'objetivo_general': 'OBJETIVO GENERAL DEL PROYECTO',
        }

class R_Objetivo_especifico(ModelForm):
    class Meta:
        model = Objetivo_especifico
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']
        labels = {
            'objetivo': 'OBJETIVO ESPECÍFICO',
            'componente': 'COMPONENTE',
            'linea_base': 'SITUACIÓN ACTUAL/LÍNEA DE BASE',
            'indicador': 'INDICADOR',
            'meta': 'META',
        }

class ObjetivoEspecificoForm(ModelForm):
    class Meta:
        model = Objetivo_especifico
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']
        labels = {
            'objetivo': 'OBJETIVO ESPECÍFICO',
            'componente': 'COMPONENTE',
            'linea_base': 'SITUACIÓN ACTUAL/LÍNEA DE BASE',
            'indicador': 'INDICADOR',
            'meta': 'META',
        }

class Beneficios_esperados(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'
        
    class Meta:
        model = Idea_Proyecto
        fields = ['beneficios_alter']
        labels = {
            'beneficios_alter': 'BENEFICIOS ESPERADOS DEL PROYECTO (AMBIENTAL, SOCIAL Y ECONÓMICO)',
        }

class A_Beneficiarios(ModelForm):
    class Meta:
        model = Beneficiario
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']
        labels = {
            'hombre_directo': 'Hombres Directos',
            'mujer_directo': 'Mujeres Directos',
            'hombre_indirecto': 'Hombres Indirectos',
            'mujer_indirecto': 'Mujeres Indirectos',
            'familia': 'Familias',

        }

class R_ModeloActa(ModelForm):
    class Meta:
        model = Modelo_Acta
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']
        labels = {
            'comunidades': 'Comunidades',
            'si_acta': 'Ingresar el acta',
            'no_acta': 'Si no se tiene, Justificar',
        }

class R_Impacto_Ambiental(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Impacto_ambiental
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']

class Rg_RiesgoDesastre(forms.ModelForm):    
    class Meta:
        model = Riesgo_desastre
        fields = ['riesgo', 'nivel']  # Usaremos estos campos

    # Agregamos los selects con las opciones disponibles
    riesgo = forms.ChoiceField(choices=riesgos)
    nivel = forms.ChoiceField(choices=nivel)

class R_DetallePOA(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
        self.fields['descripcion'].widget.attrs['rows'] = '3'

    class Meta:
        model = Detalle_POA
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']
        labels = {
            'descripcion': 'DETALLE',
        }

class R_ConclusionRecomen(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['conclusion'].widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
        self.fields['conclusion'].widget.attrs['rows'] = '8'
        self.fields['recomendacion'].widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
        self.fields['recomendacion'].widget.attrs['rows'] = '8'

    class Meta:
        model = Conclusion_recomendacion
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']
        labels = {
            'conclusion': 'CONCLUSION',
            'recomendacion': 'RECOMENDACION',
        }

class R_Declaracion_jurada(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Declaracion_jurada
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion', 'itcp']

class R_Declaracion_juradaTotal(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Declaracion_jurada
        fields = '__all__'
        exclude = ['slug', 'fecha_registro', 'fecha_actualizacion']

class R_Declaracion_ITCP(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Declaracion_jurada
        fields = ['itcp']



