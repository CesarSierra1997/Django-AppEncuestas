from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy


def login_super_staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
        return redirect('index')  # Redirige a 'index' si no es staff
    return wrapper



def validar_permisos_required(permission_required=''):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.has_perm(permission_required):
                return view_func(request, *args, **kwargs)
            messages.error(request, 'No tienes permisos para realizar esta acción.')
            return redirect(reverse_lazy('index'))  # Redirige a la URL de login
        return wrapper
    return decorator
