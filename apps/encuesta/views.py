from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from ..usuario.mixin import *
from .models import *
from .forms import *

#Muestra la vista principal de la app encuesta publica y opcion de login
class EncuestaHomeApp(TemplateView):
    model = Encuesta
    template_name = 'encuestaHome.html'

#Vistas de encuestas - administration
class InicioEncuestas(LoginSuperStaffMixin, ValidarPermisosMixin, ListView):
    permission_required = ('encuesta.view_encuesta', 'encuesta.add_encuesta', 'encuesta.delete_encuesta', 'encuesta.change_encuesta')
    model = Encuesta
    context_object_name = 'encuestas'
    template_name = 'encuesta/listado_encuestas.html'  # El template que muestra la lista de encuestas

    def get_queryset(self):
        """ Retorna todas las encuestas con sus preguntas pre-cargadas."""
        return self.model.objects.prefetch_related('pregunta_set').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hoy'] = timezone.now()  # Añadimos la fecha y hora actual al contexto
        return context
    

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

#Vistas de preguntas - administration
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

#Vistas de encuestas - publica(publico general) y privada(usuarios registrados)
#Vistas de encuestas - administration
class VerEncuestasPublicas(ListView):
    model = Encuesta
    context_object_name = 'encuestas'
    template_name = 'encuesta/lista_encuestas/encuestasPublicas.html' 

    def get_queryset(self):
        """ Retorna todas las encuestas con sus preguntas pre-cargadas."""
        return self.model.objects.filter(estado=True, publicarEncuesta=True, tipoEncuesta="Publica")

    def get_context_data(self, **kwargs):
        """ Añade encuestas y sus preguntas al contexto del template."""
        context = super().get_context_data(**kwargs)
        return context
    
class VerEncuestasPrivadas(LoginRequiredMixin, ListView):
    model = Encuesta
    context_object_name = 'encuestas'
    template_name = 'ecnuesta/lista_encuestas/encuestasPrivadas.html' 

    def get_queryset(self):
        """ Retorna todas las encuestas con sus preguntas pre-cargadas."""
        return self.model.objects.filter(estado=True, publicarEncuesta=True, tipoEncuesta="Privada")

    def get_context_data(self, **kwargs):
        """ Añade encuestas y sus preguntas al contexto del template."""
        context = super().get_context_data(**kwargs)
        return context

class ResponderEncuestaPublica(FormView):
    model = Respuesta
    template_name = 'respuesta/responder_encuesta/responder_publica.html'
    form_class = EncuestaPublicaForm
    success_url = reverse_lazy('encuesta:ver_encuestas_publicas')
    pk_url_kwarg = 'encuesta_id'

    def get_queryset(self):
        # Filtrar por una encuesta específica, no por un conjunto
        encuesta_id = self.kwargs['encuesta_id']
        try:
            encuesta = Encuesta.objects.get(id=encuesta_id, publicarEncuesta=True, tipoEncuesta = "Publica")
        except Encuesta.DoesNotExist:
            raise Http404('Encuesta no encontrada.')
        # Retorna las preguntas asociadas a esa encuesta        
        return self.model.objects.filter(encuesta=encuesta)
        
    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta ya fue publicada."""
        try:
            encuesta = Encuesta.objects.get(id=self.kwargs['encuesta_id'])
            if encuesta.publicarEncuesta == False:
                messages.warning(self.request, 'La encuesta no está publicada.')
                return redirect('encuesta:encuestaHome')
            if encuesta.tipoEncuesta == "Privada":
                messages.warning(self.request, 'Encuesta Privada, debe iniciar sesión para responder.')
                return redirect('encuesta:encuestaHome')
        except Encuesta.DoesNotExist:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect('encuesta:encuestaHome')
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encuesta = get_object_or_404(Encuesta, id=self.kwargs['encuesta_id'])
        preguntas = Pregunta.objects.filter(encuesta=encuesta)
        context['preguntas'] = preguntas
        context['encuesta'] = encuesta
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        encuesta = get_object_or_404(Encuesta, id=self.kwargs['encuesta_id'])

        # Crear el registro de la encuesta pública
        encuesta_publica = RespuestaEncuestaPublica.objects.create(
            tipoUsuario=form.cleaned_data['tipoUsuario'],
            tipoDocumento=form.cleaned_data['tipoDocumento'],
            numeroDocumento=form.cleaned_data['numeroDocumento'],
            nombre=form.cleaned_data['nombre'],
            email=form.cleaned_data['email'],
            encuesta=encuesta
        )

        preguntas = Pregunta.objects.filter(encuesta=encuesta)
        respuestas_incompletas = False  # Bandera para rastrear si falta alguna respuesta

        for pregunta in preguntas:
            if pregunta.tipoPregunta == '4':  # Pregunta de Selección múltiple
                respuesta = self.request.POST.get(f"respuesta_{pregunta.id}")
            else:
                respuesta = self.request.POST.get(f"respuesta_{pregunta.id}")

            if not respuesta:  # Si no se ha respondido una pregunta
                respuestas_incompletas = True  # Marca que hay una respuesta incompleta
                break  # No es necesario seguir, ya que falta una respuesta

            # Guardar la respuesta si se proporcionó
            Respuesta.objects.create(
                texto_respuesta=respuesta,
                pregunta=pregunta,
                respuestaEncuestaPublica=encuesta_publica
            )

        # Si falta alguna respuesta, mostrar un mensaje de error y no guardar nada
        if respuestas_incompletas:
            messages.error(self.request, 'Debe responder todas las preguntas antes de enviar la encuesta.')
            encuesta_publica.delete()  # Elimina el registro de la encuesta pública creado
            return self.form_invalid(form)  # Retorna el formulario inválido

        return super().form_valid(form)

class ResponderEncuestaPrivada(LoginRequiredMixin, FormView):
    model = RespuestaEncuestaPrivada
    template_name = 'respuesta/responder_encuesta/responder_privada.html'
    form_class = EncuestaPrivadaForm
    success_url = reverse_lazy('encuesta:inicio_encuestas')

    def dispatch(self, request, *args, **kwargs):
        # Verifica que el usuario esté autenticado
        if not request.user.is_authenticated:
            messages.warning(request, "Debes estar autenticado para responder esta encuesta.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        encuesta_id = self.kwargs['encuesta_id']
        encuesta = get_object_or_404(Encuesta, id=encuesta_id, tipoEncuesta='Privada', publicarEncuesta=True)
        return Pregunta.objects.filter(encuesta=encuesta)
    

    def get(self, request, *args, **kwargs):
        """Maneja el flujo de redirección si la encuesta ya fue publicada."""
        try:
            encuesta = Encuesta.objects.get(id=self.kwargs['encuesta_id'])
            if encuesta.publicarEncuesta == False:
                messages.warning(self.request, 'La encuesta no está publicada.')
                return redirect('encuesta:encuestaHome')
            if encuesta.tipoEncuesta == "Publica":
                messages.warning(self.request, 'Esta es una encuesta publica, accede desde encuestaHome.')
                return redirect('encuesta:encuestaHome')
        except Encuesta.DoesNotExist:
            messages.error(self.request, 'No se encontró ninguna encuesta coincidente con la consulta.')
            return redirect('encuesta:inicio_encuestas')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encuesta = get_object_or_404(Encuesta, id=self.kwargs['encuesta_id'])
        preguntas = Pregunta.objects.filter(encuesta=encuesta)
        context['preguntas'] = preguntas
        context['encuesta'] = encuesta
        return context

    def form_valid(self, form):
        encuesta = get_object_or_404(Encuesta, id=self.kwargs['encuesta_id'])

        # Crea el registro de la encuesta privada
        respuesta_encuesta_privada = RespuestaEncuestaPrivada.objects.create(
            usuario=self.request.user,
            encuesta=encuesta
        )

        # Itera sobre las preguntas y guarda las respuestas
        preguntas = Pregunta.objects.filter(encuesta=encuesta)
        for pregunta in preguntas:
            respuesta = self.request.POST.get(f"respuesta_{pregunta.id}")
            if respuesta:
                Respuesta.objects.create(
                    texto_respuesta=respuesta,
                    pregunta=pregunta,
                    respuestaEncuestaPrivada=respuesta_encuesta_privada
                )

        messages.success(self.request, "Encuesta completada con éxito.")
        return super().form_valid(form)

class VerRespuestas(LoginRequiredMixin, ListView):
    template_name = 'respuesta/ver_respuestas.html'
    context_object_name = 'respuestas'

    def get_queryset(self):
        # Obtener todas las respuestas públicas y privadas
        respuestas_publicas = Respuesta.objects.filter(respuestaEncuestaPublica__isnull=False)
        respuestas_privadas = Respuesta.objects.filter(respuestaEncuestaPrivada__isnull=False)
        
        # Unir ambas consultas y ordenarlas por encuesta
        return respuestas_publicas | respuestas_privadas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todas las respuestas públicas y privadas, y pasar encuestas
        context['respuestas_publicas'] = Respuesta.objects.filter(respuestaEncuestaPublica__isnull=False)
        context['respuestas_privadas'] = Respuesta.objects.filter(respuestaEncuestaPrivada__isnull=False)
        
        return context
