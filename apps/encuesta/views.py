from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Encuesta
from .forms import EncuestaForm


class InicioEncuestasView(LoginRequiredMixin, TemplateView):
    model = Encuesta
    template_name = 'encuestas/listado_encuestas.html'

class CrearEncuestaView(LoginRequiredMixin, CreateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'crear_encuesta.html'  # Cambia esto por el nombre de tu template
    success_url = reverse_lazy('listado_encuestas')  # Cambia esto por el nombre de la vista de éxito

    def form_valid(self, form):
        form.instance.administrador = self.request.user  # Asignar el administrador actual
        return super().form_valid(form)
