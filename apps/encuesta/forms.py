from django import forms
from django.utils import timezone
from .models import *

class EncuestaForm(forms.ModelForm):

    class Meta:
        model = Encuesta
        fields = ['titulo', 'tipoEncuesta', 'fechaInicio', 'fechaFinal', 'estado']
        labels = {
            'titulo': 'Título de la encuesta',
            'tipoEncuesta': 'Seleccione el tipo de encuesta',
            'fechaInicio': 'Fecha de inicio',
            'fechaFinal': 'Fecha de finalización',
            'estado': '¿Encuesta activada?',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el titulo de la encuesta'}),
            'tipoEncuesta': forms.Select(attrs={'class': 'form-control'}),
            'fechaInicio': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'fechaFinal': forms.SelectDateWidget(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fechaInicio')
        fecha_final = cleaned_data.get('fechaFinal')

        # Validar que la fecha de inicio es anterior a la fecha final
        if fecha_inicio and fecha_final and fecha_inicio >= fecha_final:
            raise forms.ValidationError("La fecha de finalización debe ser posterior a la de incio.")

        return cleaned_data
    

# class EncuestaModificarForm(forms.ModelForm):

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['tipoPregunta', 'texto_pregunta']  
        labels = {
            'tipoPregunta': 'Seleccione el tipo de pregunta',
            'texto_pregunta': 'Ingrese el texto de la pregunta',
        }
        widgets = {
            'tipoPregunta': forms.Select(attrs={'class': 'form-control'}),
            'texto_pregunta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el texto de la pregunta'}),
        }

    def __init__(self, *args, **kwargs):
        self.encuesta_id = kwargs.pop('encuesta_id', None)  # Obtener el id de la encuesta
        super().__init__(*args, **kwargs)

    def clean_texto_pregunta(self):
        cleaned_data = super().clean()
        texto_pregunta = cleaned_data.get('texto_pregunta')
        # Validar que la longitud del texto de la pregunta sea mayor a 10
        if len(texto_pregunta) < 10:
            raise forms.ValidationError("El texto de la pregunta debe tener al menos 10 caracteres.")
        return texto_pregunta
    
    # def clean_tipoPregunta(self):
    #     cleaned_data = super().clean()
    #     tipoPregunta = cleaned_data.get('tipoPregunta')
    #     # Validar que la pregunta sea de tipo selección múltiple
    #     if tipoPregunta!= '4':
    #         raise forms.ValidationError("La pregunta debe ser de tipo selección múltiple.")
    #     return tipoPregunta
