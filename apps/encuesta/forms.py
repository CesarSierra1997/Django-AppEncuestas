from django import forms
from .models import *

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['titulo']
        labels = {
            'titulo': 'Título de la encuesta',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el titulo de la encuesta'}),
        }

class PreguntaGeneralForm(forms.ModelForm):
    class Meta:
        model = PreguntaGeneral
        fields = ['texto_pre']
        labels = {
            'texto_pre': 'Digite la pregunta General',
        }
        widgets = {
            'texto_pre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la pregunta aquí'}),
        }

class PreguntaSelectMultipleForm(forms.ModelForm):
    class Meta:
        model = PreguntaSelectMultiple
        fields = ['texto_pre', 'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d']
        labels = {
            'texto_pre': 'Digite la pregunta de selección múltiple',
            'opcion_a': 'Opción A',
            'opcion_b': 'Opción B',
            'opcion_c': 'Opción C',
            'opcion_d': 'Opción D',
        }
        widgets = {
            'texto_pre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la pregunta aquí'}),
            'opcion_a': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opción A'}),
            'opcion_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opción B'}),
            'opcion_c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opción C'}),
            'opcion_d': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opción D'}),
        }

class PreguntaSiONoForm(forms.ModelForm):
    class Meta:
        model = PreguntaSiONo
        fields = ['texto_pre', 'opcion']
        labels = {
            'texto_pre': 'Digite la pregunta de sí o no',
            'opcion': 'Digite el texto de la opción',
        }
        widgets = {'texto_pre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la pregunta de sí o no'}),
            'opcion': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-control'}),
        }

class PreguntaNumericaForm(forms.ModelForm):
    class Meta:
        model = PreguntaNumerica
        fields = ['texto_pre', 'rango']
        labels = {
            'texto_pre': 'Digite la pregunta numérica',
            'rango': 'Rango (mínimo 1, máximo 10)',
        }
        widgets = {
            'texto_pre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la pregunta aquí'}),
            'rango': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rango'}),
        }

class RespuestaEncuestaForm(forms.ModelForm):
    class Meta:
        model = RespuestaEncuesta  
        fields = ['tipoDocumento','numeroDocumento','nombreUsuario']
        widgets = {
            'tipoDocumento': forms.Select(attrs={'class': 'form-control','placeholder': 'Slecione el tipo de documento'}),
            'numeroDocumento': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese el numero de documento'}),
            'nombreUsuario': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese el nombre de usuario'}),
        }

class RespuestaPreguntaGeneralForm(forms.ModelForm):
    class Meta:
        model = RespuestaPreguntaGeneral
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RespuestaPreguntaSelectMultipleForm(forms.ModelForm):
    class Meta:
        model = RespuestaPreguntaSelectMultiple
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Select(attrs={'class': 'form-control'}),
        }

class RespuestaPreguntaSiONoForm(forms.ModelForm):
    class Meta:
        model = RespuestaPreguntaSiONo
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Select(choices=[(True, 'Si'), (False, 'No')], attrs={'class': 'form-control'}),
        }

class RespuestaPreguntaNumericaForm(forms.ModelForm):
    class Meta:
        model = RespuestaPreguntaNumerica
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.NumberInput(attrs={'class': 'form-control'}),
        }
