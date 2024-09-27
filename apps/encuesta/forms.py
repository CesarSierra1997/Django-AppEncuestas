from django import forms
from django.utils import timezone
from .models import Encuesta

class EncuestaForm(forms.ModelForm):
    esta_activa = forms.BooleanField(required=False, label='¿Está activa?', disabled=True)

    class Meta:
        model = Encuesta
        fields = ['titulo', 'tipoEncuesta', 'administrador', 'fechaInicio', 'fechaFinal']
        labels = {
            'titulo': 'Título de la encuesta',
            'tipoEncuesta': 'Seleccione el tipo de encuesta',
            'fechaInicio': 'Fecha de inicio',
            'fechaFinal': 'Fecha de finalización',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el titulo de la encuesta'}),
            'tipoEncuesta': forms.Select(attrs={'class': 'form-control'}),
            'fechaInicio': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'fechaFinal': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Si ya existe, establecer el valor de esta_activa
            self.fields['esta_activa'].initial = self.instance.esta_activa

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fechaInicio')
        fecha_final = cleaned_data.get('fechaFinal')

        # Validar que la fecha de inicio es anterior a la fecha final
        if fecha_inicio and fecha_final and fecha_inicio >= fecha_final:
            raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha final.")

        # Calcular si la encuesta estará activa
        if fecha_inicio and fecha_final:
            now = timezone.now()
            esta_activa = fecha_inicio <= now <= fecha_final
            cleaned_data['esta_activa'] = esta_activa  # Establecer el estado en cleaned_data

        return cleaned_data
