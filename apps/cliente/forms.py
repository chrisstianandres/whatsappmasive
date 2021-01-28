from datetime import *

from django import forms
from django.forms import TextInput

from .models import Cliente, Filexls


class ClienteForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombres'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos nombres', 'class': 'form-control form-rounded'})

            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de telefono', 'class': 'form-control form-rounded'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Cliente
        fields = ['nombres', 'telefono']
        labels = {'nombres': 'Nombres', 'Telefono': 'Celular'}
        widgets = {'nombres': forms.TextInput(), 'telefono': forms.TextInput()}


class FileForm(forms.ModelForm):

    class Meta:
        model = Filexls
        fields = ['archivo']
        labels = {'archivo': 'Archivo'}

