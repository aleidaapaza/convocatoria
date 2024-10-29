from django.forms import *
from django import forms
from solicitud.models import Postulacion

class Update_Postulacion(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control form-control-sm font-weight-bold border border-info'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Postulacion
        fields = ['estado']
        labels = {
            'estado': '¿Aprobar el proyecto?',
        }