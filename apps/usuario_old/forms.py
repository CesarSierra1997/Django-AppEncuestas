from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class FormularioLogin(AuthenticationForm):    
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Nombre de usuario'
        self.fields['password'].widget.attrs['class']='form-control'
        self.fields['password'].widget.attrs['placeholder']='Contraseña'

class FormularioUsuario(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su Contraseña',
            'id':'password1',
            'required':'required'
        }
    ))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Confirme la contraseña ingresada',
            'id':'password2',
            'required':'required'
        }
    ))
    class Meta:
        model = Usuario
        fields = ['tipoDocumento','numeroDocumento','nombres', 'apellidos','email','rol','username' ]
        widgets = {
            'tipoDocumento': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Slecione el tipo de documento'
                }),
            'numeroDocumento': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Ingrese el numero de documento'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo electrónico'
                }),
            'nombres': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Digite su nombre'
                }),
            'apellidos': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Digite sus apellidos'
                }),
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre de usuario - caractéres permitidos ( /, *, +, -, ., _ )'
                }),
            'rol': forms.Select(
                attrs={
                    'class':'form-control'
                })}
    def clean_nombres(self):
        mail = self.cleaned_data.get('mail')
        if mail.is_valid():
            mail = mail.lower()   
        return mail

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not nombres.replace(" ", "").isalpha():
            raise ValidationError(_('El nombre solo debe contener letras.'))
        return nombres.lower()   

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos.replace(" ", "").isalpha():
            raise ValidationError(_('Los apellidos solo deben contener letras.'))
        return apellidos.lower()    
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.replace(" ", "_")
        caracteres_permitidos = set("/-*+._1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if not all(char in caracteres_permitidos for char in username):
            raise ValidationError(_('Se permiten solo caracteres alfanuméricos y los siguientes especiales: /, *, -, +, ., _'))
        return username

    def clean_password2(self):
        print(self.cleaned_data)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')
            caracteres_permitidos = set("/-*+._1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            if not all(char in caracteres_permitidos for char in password2):
                raise ValidationError(_('Se permiten solo caracteres alfanuméricos y los siguientes especiales: /, *, -, +, ., _'))
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



# class FormularioEstudiante(forms.ModelForm):
#     class Meta:
#         model = Estudiante
#         fields = ['usuario_id']
#         widgets = {

#             'usuario_id': forms.Select(
#                 attrs={
#                     'class':'form-control'
#                 }
#             )}
        
# class FormularioProfesor(forms.ModelForm):
#     class Meta:
#         model = Profesor
#         fields = ['usuario_id']
#         widgets = {

#             'usuario_id': forms.Select(
#                 attrs={
#                     'class':'form-control'
#                 }
#             )}