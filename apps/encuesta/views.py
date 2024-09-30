from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from ..usuario.mixin import *
from .models import *
from .forms import *


#Muestra la vista principal de la app encuesta publica y opcion de login
class EncuestaHomeApp(TemplateView):
    model = Encuesta
    template_name = 'encuestaHome.html'

#Muestra la lista de encuestas publicas y privasas, vista explusiva para el administrador
class InicioEncuestas(LoginSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    template_name = 'encuesta/listado_encuestas.html'
    
    def get_context_data(self, **kwargs):
        """ Añade todas las encuestas al contexto del template. """
        context = super().get_context_data(**kwargs)
        context['encuestas'] = Encuesta.objects.all()
        return context

class ListaEncuestas(LoginSuperStaffMixin, ValidarPermisosMixin, ListView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    context_object_name = 'encuestas'

    def get_queryset(self):
        """ Retorna todas las encuestas disponibles en la base de datos."""
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        """ Redirige al inicio de encuestas tras intentar acceder a la lista de encuestas."""
        return redirect('encuesta:inicio_encuestas')
        
class CrearEncuesta(LoginSuperStaffMixin, ValidarPermisosMixin, CreateView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuesta/crear_encuesta.html'
    success_url = reverse_lazy('encuesta_detail')
    pk_url_kwarg = 'encuesta_id'


    def form_valid(self, form):
        form.instance.administrador = self.request.user  # Asignar el administrador actual
        form.instance.fechaCreacion = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.object.pk})

class EncuestaDetail(LoginSuperStaffMixin, ValidarPermisosMixin, DetailView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    template_name = 'encuesta/detalle_encuesta.html'
    pk_url_kwarg = 'encuesta_id'
    success_url = reverse_lazy('encuesta:inicio_encuestas')

    def get_queryset(self):
        """ Retorna todas las encuestas disponibles en la base de datos."""
        return self.model.objects.filter(estado=True)
    
    def get_object(self, queryset=None):
        """Obtener la encuesta o lanzar un 404 si no está disponible."""
        try:
            encuesta = super().get_object(queryset)
            if not encuesta.estado:
                messages.info(self.request, 'La encuesta no se encuentra disponible.')
                raise Http404("La encuesta no está activa.")
            return encuesta
        except Http404:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class EditarEncuesta(LoginSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    template_name = 'encuesta/editar_encuesta.html'
    form_class = EncuestaForm
    success_url = reverse_lazy('encuesta_detail')
    pk_url_kwarg = 'encuesta_id'

    def form_valid(self, form):
        form.instance.administrador = self.request.user
        form.instance.fechaModificacion = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.object.pk})

class EliminarEncuesta(LoginSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    template_name = 'encuesta/confirmar_eliminar.html'
    pk_url_kwarg = 'encuesta_id'
    
    def post(self, request, *args, **kwargs):
        encuesta = self.get_object()
        encuesta.estado = False
        encuesta.save()
        messages.success(request,'Encuesta eliminada correctamente')
        return redirect('encuesta:inicio_encuestas')

class AgregarPregunta(LoginSuperStaffMixin, ValidarPermisosMixin, CreateView):
    permission_required = ('pregunta.add_pregunta', 'pregunta.view_pregunta', 'pregunta.change_pregunta', 'pregunta.delete_pregunta')
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'pregunta/agregar_pregunta.html'
    pk_url_kwarg = 'encuesta_id'

    def form_valid(self, form):
        form.instance.encuesta = get_object_or_404(Encuesta, pk=self.kwargs['encuesta_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.object.encuesta.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encuesta'] = get_object_or_404(Encuesta, pk=self.kwargs['encuesta_id'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['encuesta_id'] = self.kwargs['encuesta_id']
        return kwargs