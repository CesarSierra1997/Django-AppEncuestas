#Importarmos libreria para las urls
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #Usuario
    path('listar_usuario/', login_required(ListadoUsuario.as_view()), name='listar_usuario'),
    path('registrar_usuario/', login_required(RegistrarUsuario.as_view()), name='registrar_usuario'),
    path('editar_usuario/<int:pk>/', login_required(ActualizarUsuario.as_view()), name='editar_usuario'),
    path('eliminar_usuario/<int:pk>/', login_required(EliminarUsuario.as_view()), name='eliminar_usuario'),
]  