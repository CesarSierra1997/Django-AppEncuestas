import json
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from ..usuario.forms import FormularioLogin
from django.urls import reverse_lazy
from django.utils.decorators import  method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.usuario.models import Usuario
from apps.usuario.forms import *
from apps.usuario.mixin import *

class Inicio(TemplateView): #vista basada en clases para una sola vista
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class Login(FormView):
    template_name = "login.html"
    form_class = FormularioLogin
    success_url = reverse_lazy('encuesta:encuestaHome')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    #redefinir método dispatch() 
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            usuario = request.user
            print(f"*************El usuario id: {usuario.id} - nombre: {usuario}, ya Inicio Sesión****************")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
    
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/encuesta/encuestaHome/')


class InicioUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')
    template_name = 'usuario/listar_usuarios.html'

class ListadoUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, ListView):
    model = Usuario
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')

    def get_queryset(self):
        return self.model.objects.filter(is_active=True) 
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('usuario:inicio_usuarios')
        


#ERROR AL REGISTRAR USUARIO Y MOSTRAR ERRORES EN SWEIT ALERT
class RegistrarUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = "usuario/registrar_usuario.html"
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                # Verificar el rol seleccionado
                rol = form.cleaned_data.get('rol')
                nombres = form.cleaned_data.get('nombres')
                apellidos = form.cleaned_data.get('apellidos')
                email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                tipoDocumento = form.cleaned_data.get('tipoDocumento')
                numeroDocumento = form.cleaned_data.get('numeroDocumento')
                password = form.cleaned_data.get('password1')

                # DEBUG: Print para verificar el rol
                print(f"Rol seleccionado: {rol.rol}")

                # Si el rol es 'Administrador', usar create_superuser
                if rol.rol == 'administrador':
                    print("Creando superusuario...")  # DEBUG
                    nuevo_usuario = Usuario.objects.create_superuser(
                        username=username,
                        email=email,
                        nombres=nombres,
                        apellidos=apellidos,
                        tipoDocumento=tipoDocumento,
                        numeroDocumento=numeroDocumento,
                        password=password,
                        rol=rol
                    )
                    print(f"Superusuario creado: {nuevo_usuario}")  # DEBUG
                    mensaje = f'¡{self.model.__name__} Administrador registrado correctamente en el sistema!'
                else:
                    # Para otros roles, usar create_user
                    print("Creando usuario normal...")  # DEBUG
                    nuevo_usuario = Usuario.objects.create_user(
                        username=username,
                        email=email,
                        nombres=nombres,
                        apellidos=apellidos,
                        tipoDocumento=tipoDocumento,
                        numeroDocumento=numeroDocumento,
                        password=password,
                        rol=rol
                    )
                    print(f"Usuario creado: {nuevo_usuario}")  # DEBUG
                    mensaje = f'¡{self.model.__name__} registrado correctamente!'

                error = 'no hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuarios')


class EditarUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = "usuario/editar_usuario.html"
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')


    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'¡{self.model.__name__} actualizado correctamente!'
                error = f'no hay error'
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuarios')
        
class EliminarUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    model = Usuario
    template_name = "usuario/eliminar_usuario.html"
    success_url = reverse_lazy('usuario:inicio_usuarios')
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')


    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            usuario = self.get_object()
            usuario.is_active = False
            usuario.save()
            mensaje = f'¡{self.model.__name__} eliminado correctamente!'
            error = f'no hay error'
            response = JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code = 201
            return response
        else:
            return redirect('usuario:inicio_usuarios')

        
