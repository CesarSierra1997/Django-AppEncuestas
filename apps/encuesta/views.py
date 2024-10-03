from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from ..usuario.mixin import *
from .models import *
from .forms import *
from datetime import datetime

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
        messages.success(self.request, '¡Encuesta creada correctamente!')
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
        """Retorna todas las encuestas activas disponibles en la base de datos."""
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta no está activa."""
        try:
            pass
        except Http404:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect(self.success_url)

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las preguntas relacionadas con la encuesta actual
        preguntas = Pregunta.objects.filter(encuesta=self.get_object())

        # Obtener la fecha de hoy y pasarla al contexto
        hoy = datetime.now()
        context['hoy'] = hoy

        # Para cada pregunta, busca las opciones si es una pregunta de selección múltiple
        preguntas_con_opciones = []
        for pregunta in preguntas:
            opciones = None
            if pregunta.tipoPregunta == '4':  # '4' es la selección múltiple en tu modelo
                opciones = OpcionesPregunta.objects.filter(pregunta=pregunta).first()
            preguntas_con_opciones.append({
                'pregunta': pregunta,
                'opciones': opciones
            })
        
        context['preguntas_con_opciones'] = preguntas_con_opciones
        return context

class EditarEncuesta(LoginSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    template_name = 'encuesta/editar_encuesta.html'
    form_class = ActualizarEncuestaForm
    success_url = reverse_lazy('encuesta:inicio_encuestas')
    pk_url_kwarg = 'encuesta_id'

    def get_queryset(self):
        """Retorna todas las encuestas activas disponibles en la base de datos."""
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta no está activa."""
        try:
            pass
        except Http404:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect('encuesta:inicio_encuestas')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.administrador == self.request.user
        form.instance.fechaModificacion = timezone.now()
        messages.success(self.request, 'Encuesta actualizada exitosamente')
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
        encuesta.delete()
        messages.success(request,'Encuesta eliminada correctamente')
        return redirect('encuesta:inicio_encuestas')

class AgregarPregunta(LoginSuperStaffMixin, ValidarPermisosMixin, CreateView):
    permission_required = ('pregunta.add_pregunta', 'pregunta.view_pregunta', 'pregunta.change_pregunta', 'pregunta.delete_pregunta')
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'pregunta/agregar_pregunta.html'
    pk_url_kwarg = 'encuesta_id'
    
    def get_queryset(self):
        # Filtrar por una encuesta específica, no por un conjunto
        encuesta_id = self.kwargs['encuesta_id']
        try:
            encuesta = Encuesta.objects.get(id=encuesta_id, publicarEncuesta=False)
        except Encuesta.DoesNotExist:
            raise Http404('Encuesta no encontrada o ya publicada.')
        # Retorna las preguntas asociadas a esa encuesta
        return self.model.objects.filter(encuesta=encuesta)

    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta ya fue publicada."""
        encuesta_id = self.kwargs.get('encuesta_id')

        try:
            encuesta = Encuesta.objects.get(id=encuesta_id)
            if encuesta.publicarEncuesta:
                messages.warning(self.request, 'La encuesta ya fue publicada no puede agregar más preguntas.')
                return redirect('encuesta:encuesta_detail', encuesta_id=encuesta_id)
        except Encuesta.DoesNotExist:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect('encuesta:inicio_encuestas')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Asocia la pregunta con la encuesta correspondiente
        form.instance.encuesta = get_object_or_404(Encuesta, pk=self.kwargs['encuesta_id'])
        response = super().form_valid(form)

        # Si la pregunta es de tipo "Selección múltiple", guardar las opciones en un único objeto
        if form.instance.tipoPregunta == '4':  # Ajusta según tu choice para "Selección múltiple"
            opcion_1 = self.request.POST.get('opcion_1')
            opcion_2 = self.request.POST.get('opcion_2')
            opcion_3 = self.request.POST.get('opcion_3')
            opcion_4 = self.request.POST.get('opcion_4')
            
            # Verificar que las 4 opciones estén presentes
            if not all([opcion_1, opcion_2, opcion_3, opcion_4]):
                messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
                form.add_error(None, "Debe completar todas las opciones para una pregunta de selección múltiple.")
                return self.form_invalid(form)
            
            # Crear un solo objeto de OpcionesPregunta con las 4 opciones
            OpcionesPregunta.objects.create(
                pregunta=form.instance,
                opcion_1=opcion_1,
                opcion_2=opcion_2,
                opcion_3=opcion_3,
                opcion_4=opcion_4
            )
        
        return response

    def get_success_url(self):
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.object.encuesta.pk})
    

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['encuesta'] = get_object_or_404(Encuesta, pk=self.kwargs['encuesta_id'])
            return context

class EditarPregunta(LoginSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    permission_required = ('pregunta.add_pregunta', 'pregunta.view_pregunta', 'pregunta.change_pregunta', 'pregunta.delete_pregunta')
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'pregunta/editar_pregunta.html'
    pk_url_kwarg = 'pregunta_id'

    """" Validar si la encuesta ya esta publicada """
    def get_queryset(self):
        # Filtrar por una encuesta específica, no por un conjunto
        encuesta_id = self.kwargs['encuesta_id']
        try:
            encuesta = Encuesta.objects.get(id=encuesta_id, publicarEncuesta=False)
        except Encuesta.DoesNotExist:
            raise Http404('Encuesta no encontrada o ya publicada.')
        # Retorna las preguntas asociadas a esa encuesta
        return self.model.objects.filter(encuesta=encuesta)

    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta ya fue publicada."""
        encuesta_id = self.kwargs.get('encuesta_id')

        try:
            encuesta = Encuesta.objects.get(id=encuesta_id)
            if encuesta.publicarEncuesta:
                messages.warning(self.request, 'La encuesta ya fue publicada no puede editar preguntas.')
                return redirect('encuesta:encuesta_detail', encuesta_id=encuesta_id)
        except Encuesta.DoesNotExist:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect('encuesta:inicio_encuestas')

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Verificar si la pregunta es de tipo selección múltiple
        pregunta = self.get_object()
        if pregunta.tipoPregunta == '4':  # Ajusta según el valor que usas para "Selección múltiple"
            opciones = OpcionesPregunta.objects.filter(pregunta=pregunta).first()
            context['opciones'] = opciones
        return context

    def form_valid(self, form):
        # Si es una pregunta de selección múltiple, actualizar las opciones también
        if form.instance.tipoPregunta == '4':  # '4' corresponde a selección múltiple
            opcion_1 = self.request.POST.get('opcion_1')
            opcion_2 = self.request.POST.get('opcion_2')
            opcion_3 = self.request.POST.get('opcion_3')
            opcion_4 = self.request.POST.get('opcion_4')
            
            # Verificar que las 4 opciones estén presentes
            if not all([opcion_1, opcion_2, opcion_3, opcion_4]):
                form.add_error(None, "Debe completar todas las opciones para una pregunta de selección múltiple.")
                return self.form_invalid(form)
            
            # Actualizar las opciones si ya existen
            opciones_pregunta = OpcionesPregunta.objects.filter(pregunta=form.instance).first()
            if opciones_pregunta:
                opciones_pregunta.opcion_1 = opcion_1
                opciones_pregunta.opcion_2 = opcion_2
                opciones_pregunta.opcion_3 = opcion_3
                opciones_pregunta.opcion_4 = opcion_4
                opciones_pregunta.save()
            else:
                # Si no existen, crear nuevas opciones
                OpcionesPregunta.objects.create(
                    pregunta=form.instance,
                    opcion_1=opcion_1,
                    opcion_2=opcion_2,
                    opcion_3=opcion_3,
                    opcion_4=opcion_4
                )

        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al detalle de la encuesta
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.kwargs['encuesta_id']})

class OpcionPregunta_SelectMultiple(LoginSuperStaffMixin, ValidarPermisosMixin, CreateView):
    permission_required = ('opcion_pregunta.add_opcion_pregunta', 'opcion_pregunta.view_opcion_pregunta', 'opcion_pregunta.change_opcion_pregunta', 'opcion_pregunta.delete_opcion_pregunta')
    model = OpcionesPregunta
    form_class = OpcionPreguntaForm  # Este formulario debe manejar las cuatro opciones
    template_name = 'pregunta/agregar_pregunta.html'
    pk_url_kwarg = 'pregunta_id'

    def form_valid(self, form):
        # Asociar las opciones con la pregunta correspondiente
        form.instance.pregunta = get_object_or_404(Pregunta, pk=self.kwargs['pregunta_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redireccionar al detalle de la encuesta una vez que las opciones sean guardadas
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.object.pregunta.encuesta.pk})
    
    def get_context_data(self, **kwargs):
        # Añadir la pregunta al contexto para que el template tenga acceso a ella
        context = super().get_context_data(**kwargs)
        context['pregunta'] = get_object_or_404(Pregunta, pk=self.kwargs['pregunta_id'])
        return context
    
    def get_form_kwargs(self):
        # Pasar el `pregunta_id` al formulario si es necesario para usarlo en la lógica del formulario
        kwargs = super().get_form_kwargs()
        kwargs['pregunta_id'] = self.kwargs['pregunta_id']
        return kwargs

class EliminarPregunta(LoginSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    permission_required = ('pregunta.add_pregunta', 'pregunta.view_pregunta', 'pregunta.change_pregunta', 'pregunta.delete_pregunta')
    model = Pregunta
    template_name = 'pregunta/confirmar_eliminar.html'
    pk_url_kwarg = 'pregunta_id'

    def get_queryset(self):
        # Filtrar por una encuesta específica, no por un conjunto
        encuesta_id = self.kwargs['encuesta_id']
        try:
            encuesta = Encuesta.objects.get(id=encuesta_id, publicarEncuesta=False)
        except Encuesta.DoesNotExist:
            raise Http404('Encuesta no encontrada o ya publicada.')
        # Retorna las preguntas asociadas a esa encuesta
        return self.model.objects.filter(encuesta=encuesta)

    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta ya fue publicada."""
        encuesta_id = self.kwargs.get('encuesta_id')

        try:
            encuesta = Encuesta.objects.get(id=encuesta_id)
            if encuesta.publicarEncuesta:
                messages.warning(self.request, 'La encuesta ya fue publicada no puede eliminar preguntas.')
                return redirect('encuesta:encuesta_detail', encuesta_id=encuesta_id)
        except Encuesta.DoesNotExist:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect('encuesta:inicio_encuestas')

        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Obtenemos la pregunta y el id de la encuesta antes de eliminarla
        pregunta = self.get_object()
        encuesta_id = pregunta.encuesta.pk
        pregunta.delete()
        # Mostramos un mensaje de éxito
        messages.success(self.request, 'Pregunta eliminada correctamente')
        # Redirigimos al detalle de la encuesta
        return redirect('encuesta:encuesta_detail', encuesta_id=encuesta_id)

    def get_success_url(self):
        # Definimos la URL de éxito tras eliminar la pregunta
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.object.encuesta.pk})
    
    def get_context_data(self, **kwargs):
        # Añadir la pregunta al contexto para que el template tenga acceso a ella
        context = super().get_context_data(**kwargs)
        context['encuesta'] = get_object_or_404(Encuesta, pk=self.kwargs['encuesta_id'])
        context['pregunta'] = self.get_object()
        return context
  
class PublicarEncuesta(LoginSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuesta/publicar_encuesta.html'
    pk_url_kwarg = 'encuesta_id'
    success_url = reverse_lazy('encuesta:inicio_encuestas')

    def get_queryset(self):
        """Retorna todas las encuestas no publicadas."""
        return self.model.objects.filter(publicarEncuesta=False)

    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta no está activa."""
        try:
            encuesta = Encuesta.objects.get(id=self.kwargs['encuesta_id'])
            if encuesta.publicarEncuesta:
                messages.warning(self.request, 'La encuesta ya fue publicada.')
                return redirect('encuesta:encuesta_detail', encuesta_id=encuesta.id)
        except Http404:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect('encuesta:inicio_encuestas')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        encuesta = self.get_object()
        
        # Validar si la encuesta tiene al menos una pregunta
        if encuesta.pregunta_set.count() == 0:
            messages.error(self.request, 'La encuesta debe tener al menos una pregunta antes de publicarse.')
            return redirect('encuesta:encuesta_detail', encuesta_id=encuesta.id)

        # Publicar encuesta
        encuesta.publicarEncuesta = True
        encuesta.save()
        messages.success(self.request, '¡ENCUESTA PUBLICADA EXITOSAMENTE!.')
        
        return redirect('encuesta:encuesta_detail', encuesta_id=encuesta.id)


    def get_success_url(self):
        return reverse('encuesta:encuesta_detail', kwargs={'encuesta_id': self.object.pk})


class EncuestaPublica():
    pass
    
class EncuestaPrivada():
    pass
