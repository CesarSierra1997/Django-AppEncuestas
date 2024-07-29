from django import forms
from .models import *

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['titulo','tipoEncuesta']
        labels = {
            'titulo': 'Título de la encuesta',
            'tipoEncuesta': 'Seleccione el tipo de encuesta',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el titulo de la encuesta'}),
            'tipoEncuesta': forms.Select(attrs={'class': 'form-control'}),
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
        fields = ['texto_pre']
        labels = {
            'texto_pre': 'Digite la pregunta de selección múltiple',
        }
        widgets = {
            'texto_pre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la pregunta aquí'}),
        }

class OpcionPreguntaSelectMultipleForm(forms.ModelForm):
    class Meta:
        model = OpcionPreguntaSelectMultiple
        fields = ['opcion']
        labels = {
            'opcion': 'Digite la opcion para la pregunta',
        }
        widgets = {
            'opcion':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la opcion'}),
        }

class PreguntaSiONoForm(forms.ModelForm):
    class Meta:
        model = PreguntaSiONo
        fields = ['texto_pre',]
        labels = {
            'texto_pre': 'Digite la pregunta de sí o no',
        }
        widgets = {'texto_pre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la pregunta de sí o no'}),
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

class RespuestaEncuestaPublicaForm(forms.ModelForm):
    class Meta:
        model = RespuestaEncuestaPublica  
        fields = ['tipoDocumento','numeroDocumento','nombre','email']
        labels = {
            'tipoDocumento': 'Digite el tipo de documento',
            'numeroDocumento': 'Digite el numero de documento',
            'nombre': 'Digite el nombre completo',
            'email': 'Digite su direccion de email',
        }
        widgets = {
            'tipoDocumento': forms.Select(attrs={'class': 'form-control','placeholder': 'Tipo de documento'}),
            'numeroDocumento': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Numero de documento'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombres y apellidos'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo electrónico'}),
        }

class RespuestaEncuestaPrivadaForm(forms.ModelForm):
    class Meta:
        model = RespuestaEncuestaPrivada 
        fields = ['usuario','encuesta']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control','placeholder': 'Selecione el usuario'}),
            'encuesta': forms.Select(attrs={'class': 'form-control','placeholder': 'Selecione la encuesta'}),
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
