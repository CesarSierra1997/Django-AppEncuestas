from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, DeleteView, UpdateView, FormView
from django.shortcuts import get_object_or_404
from django.contrib import messages

from .models import *
from .forms import *

# Vista para la página de inicio
class InicioView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['ip_address'] = obtener_direccion_ip(self.request)
        return context

# Vista para crear encuestas
class CrearEncuestaView(CreateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuesta/crear_encuesta.html'

    def get_success_url(self):
        return reverse_lazy('encuesta', kwargs={'encuesta_id': self.object.id})

# Vista para ver el detalle de una encuesta
class EncuestaDetailView(DetailView):
    model = Encuesta
    template_name = 'encuesta/encuesta.html'
    context_object_name = 'encuesta'
    pk_url_kwarg = 'encuesta_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encuesta = self.object

        preguntas = []
        for tipo_pregunta in ['general', 'select_multiple', 'si_o_no', 'numerica']:
            if tipo_pregunta == 'general':
                preguntas_tipo = PreguntaGeneral.objects.filter(encuesta=encuesta)
            elif tipo_pregunta == 'select_multiple':
                preguntas_tipo = PreguntaSelectMultiple.objects.filter(encuesta=encuesta)
            elif tipo_pregunta == 'si_o_no':
                preguntas_tipo = PreguntaSiONo.objects.filter(encuesta=encuesta)
            elif tipo_pregunta == 'numerica':
                preguntas_tipo = PreguntaNumerica.objects.filter(encuesta=encuesta)

            for pregunta in preguntas_tipo:
                preguntas.append((tipo_pregunta, pregunta))

        context['preguntas'] = preguntas
        return context

# Vista para eliminar encuestas
class EliminarEncuestaView(DeleteView):
    model = Encuesta
    template_name = 'encuesta/eliminar_encuesta.html'
    pk_url_kwarg = 'encuesta_id'
    success_url = reverse_lazy('encuestaHome')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Encuesta eliminada correctamente')
        return super().delete(request, *args, **kwargs)

# Vista para editar encuestas
class EditarEncuestaView(UpdateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuesta/editar_encuesta.html'
    pk_url_kwarg = 'encuesta_id'
    success_url = reverse_lazy('encuestaHome')

    def form_valid(self, form):
        messages.success(self.request, 'Encuesta editada correctamente')
        return super().form_valid(form)

# Clase PreguntaFactory para manejar formularios según el tipo de pregunta
class PreguntaFactory:
    @staticmethod
    def crear_pregunta(tipo_pregunta):
        if tipo_pregunta == 'general':
            return PreguntaGeneralForm()
        elif tipo_pregunta == 'select_multiple':
            return PreguntaSelectMultipleForm(), OpcionPreguntaSelectMultipleForm()
        elif tipo_pregunta == 'si_o_no':
            return PreguntaSiONoForm()
        elif tipo_pregunta == 'numerica':
            return PreguntaNumericaForm()
        else:
            return None

# Vista para agregar preguntas a la encuesta
class AgregarPreguntaView(FormView):
    template_name = 'pregunta/agregar_pregunta.html'

    def get_form(self, form_class=None):
        tipo_pregunta = self.request.GET.get('tipo_pregunta')
        form = PreguntaFactory.crear_pregunta(tipo_pregunta)
        return form

    def form_valid(self, form):
        tipo_pregunta = self.request.POST.get('tipo_pregunta')
        encuesta = get_object_or_404(Encuesta, pk=self.kwargs['encuesta_id'])
        
        if tipo_pregunta == 'select_multiple':
            pregunta_form, opcion_form = form
            pregunta = pregunta_form.save(commit=False)
            pregunta.encuesta = encuesta
            pregunta.save()

            opciones = self.request.POST.getlist('opciones')
            for opcion_texto in opciones:
                if opcion_texto:
                    OpcionPreguntaSelectMultiple.objects.create(pregunta=pregunta, opcion=opcion_texto)
        else:
            pregunta = form.save(commit=False)
            pregunta.encuesta = encuesta
            pregunta.save()

        messages.success(self.request, 'Pregunta agregada correctamente a la encuesta')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('encuesta', kwargs={'encuesta_id': self.kwargs['encuesta_id']})
