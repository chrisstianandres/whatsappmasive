from datetime import *

from django import forms
from django.forms import TextInput, Textarea

from .models import Mensaje


class MensajeForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['mensaje'].widget = Textarea(
                attrs={'placeholder': 'Ingrese el mensaje que desea enviar', 'class': 'form-control form-rounded',
                       'col': 120})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Mensaje
        fields = ['mensaje', 'numero_veces']
        labels = {'mensaje': 'Mensaje a enviar', 'numero_veces': 'Cantidad de veces a enviar el mensaje'}
        widgets = {'mensaje': forms.Textarea(attrs={'col': 120}), 'numero_veces': forms.TextInput()}


