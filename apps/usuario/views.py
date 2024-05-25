from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import  method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from .models import Usuario
from .forms import FormularioUsuario, FormularioLogin
from django.conf import settings

class Login(FormView):
    template_name = "login.html"
    form_class = FormularioLogin
    success_url = reverse_lazy('encuestaHome')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    #redefinir metodo dispatch() 
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
    return HttpResponseRedirect('/encuestas/home/')

class ListadoUsuario(View):
    model = Usuario
    template_name = "usuario/usuario/listar_usuario.html"
    form_class = FormularioUsuario

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo=True)
    
    def get_context_data(self, **kwargs):
        context = {}
        context["usuarios"] = self.get_queryset() 
        context["form"] = self.form_class() 
        return context
    
    def get(self, request, *args, **kwargs):
            return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuario:listar_usuario')
        else:
            form = self
            return render(request, self.template_name, self.get_context_data()) 

class RegistrarUsuario(CreateView):
    model = Usuario
    template_name = "usuario/usuario/crear_usuario.html"
    form_class = FormularioUsuario
    success_url = reverse_lazy('usuario:listar_usuario')

    def form_valid(self, form):
        # Antes de guardar el formulario, necesitas asignar el rol seleccionado
        usuario = form.save(commit=False)
        # Obtener el rol seleccionado en el formulario
        rol_seleccionado = form.cleaned_data['rol']
        
        # Verificar si el rol seleccionado es "Administrador"
        if rol_seleccionado.rol == 'administrador':
            usuario.usuario_administrador = True
        else:
            usuario.usuario_administrador = False
        usuario.save()
        return super().form_valid(form)

class ActualizarUsuario(UpdateView):
    model = Usuario
    template_name = "usuario/usuario/usuario.html"
    form_class = FormularioUsuario
    success_url = reverse_lazy('usuario:listar_usuario')

class EliminarUsuario(DeleteView):
    model = Usuario
    queryset = Usuario.objects.all()

    def post(self, request, pk, *args, **kwargs):
        object = Usuario.objects.get(id = pk)
        object.usuario_activo = False
        object.save()
        return redirect("usuario:listar_usuario")

