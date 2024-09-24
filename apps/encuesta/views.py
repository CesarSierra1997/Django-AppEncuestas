from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .mixin import login_super_staff_required, validar_permisos_required

#BUSQUEDA EN MODELOS
def buscar(request):
    if 'q' in request.GET:
        query = request.GET['q']
        encuestas = Encuesta.objects.filter(titulo__icontains=query)
        preguntas_generales = PreguntaGeneral.objects.filter(texto_pre__icontains=query)
        preguntas_select_multiple = PreguntaSelectMultiple.objects.filter(texto_pre__icontains=query)
        preguntas_si_o_no = PreguntaSiONo.objects.filter(texto_pre__icontains=query)
        preguntas_numericas = PreguntaNumerica.objects.filter(texto_pre__icontains=query)
        respuestas_generales = RespuestaPreguntaGeneral.objects.filter(respuesta__icontains=query)
        return render(request, 'busqueda_resultados.html', {'encuestas': encuestas, 'preguntas_generales': preguntas_generales,
                                                            'preguntas_select_multiple': preguntas_select_multiple,
                                                            'preguntas_si_o_no': preguntas_si_o_no,
                                                            'preguntas_numericas': preguntas_numericas,
                                                            'respuestas_generales':respuestas_generales,
                                                            'query': query})
    else:
        return render(request, 'busqueda_resultados.html')

def obtener_direccion_ip(request):
    # Si tu aplicación se ejecuta detrás de un proxy, la dirección IP puede estar en otro encabezado
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip_address:
        # Si hay múltiples direcciones IP (debido a proxies anidados), toma la primera
        ip_address = ip_address.split(',')[0]
    else:
        # Si no hay proxy, obtén la dirección IP del cliente normalmente
        ip_address = request.META.get('REMOTE_ADDR', None)
    return ip_address

#INDEX FABRICA DE SOFTWARE 
# def inicio(request):
#     ip_address = obtener_direccion_ip(request)
#     print("su direccion ip: ",ip_address)
#     return render(request, 'index.html',{'ip_address': ip_address})

#CRUD ENCUESTA
@login_super_staff_required
@validar_permisos_required(permission_required='app_encuesta.add_encuesta')
def crear_encuesta(request):
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('encuesta', encuesta_id=form.instance.id)
    else:
        form = EncuestaForm()
    return render(request, 'encuesta/crear_encuesta.html', {'form': form})

@login_super_staff_required
@validar_permisos_required(permission_required='app_encuesta.view_encuesta')
def encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    preguntas = []
    # Recorremos cada tipo de pregunta y las agregamos a la lista de preguntas
    for tipo_pregunta in ['general', 'select_multiple', 'si_o_no', 'numerica']:
        preguntas_tipo = None
        if tipo_pregunta == 'general':
            preguntas_tipo = PreguntaGeneral.objects.filter(encuesta=encuesta)
        elif tipo_pregunta == 'select_multiple':
            preguntas_tipo = PreguntaSelectMultiple.objects.filter(encuesta=encuesta)
        elif tipo_pregunta == 'si_o_no':
            preguntas_tipo = PreguntaSiONo.objects.filter(encuesta=encuesta)
        elif tipo_pregunta == 'numerica':
            preguntas_tipo = PreguntaNumerica.objects.filter(encuesta=encuesta)
        # Agregamos las preguntas de este tipo a la lista general de preguntas
        for pregunta in preguntas_tipo:
            preguntas.append((tipo_pregunta, pregunta))

    return render(request, 'encuesta/encuesta.html', {'encuesta': encuesta, 'preguntas': preguntas})

def eliminar_encuesta(request, encuesta_id):
    try:
        encuesta = Encuesta.objects.get(pk=encuesta_id)
        if request.method == "POST":
            encuesta.delete()
            messages.success(request, 'Encuesta eliminada correctamente')
            return redirect('encuestaHome')
    except Encuesta.DoesNotExist:
        messages.error(request, 'La encuesta que intenta eliminar no existe')
    except Exception as e:
        messages.error(request, f'Error al eliminar la encuesta: {e}')
    return redirect('encuestaHome')

def editar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encuesta editada correctamente')
            return redirect('encuestaHome')
    else:
        form = EncuestaForm(instance=encuesta)
    return render(request, 'encuesta/editar_encuesta.html', {'form': form})

#CRUD PREGUNTA - TIPO PREGUNTA
class PreguntaFactory:
    @staticmethod
    def crear_pregunta(tipo, *args, **kwargs):
        if tipo == 'general':
            return PreguntaGeneralForm(*args, **kwargs)
        elif tipo == 'select_multiple':
            pregunta_form = PreguntaSelectMultipleForm(*args, **kwargs)
            opcion_form = OpcionPreguntaSelectMultipleForm()
            return pregunta_form, opcion_form
        elif tipo == 'si_o_no':
            return PreguntaSiONoForm(*args, **kwargs)
        elif tipo == 'numerica':
            return PreguntaNumericaForm(*args, **kwargs)
        else:
            raise ValueError('Tipo de pregunta no válido: {}'.format(tipo))

def agregar_pregunta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    tipo_pregunta = request.GET.get('tipo_pregunta')
    opcion_form = None

    if request.method == 'POST':
        tipo_pregunta = request.POST.get('tipo_pregunta')
        if tipo_pregunta not in ['general', 'select_multiple', 'si_o_no', 'numerica']:
            messages.error(request, 'Tipo de pregunta no válido')
            return render(request,'pregunta/agregar_pregunta.html',{'encuesta_id':encuesta_id})

        if tipo_pregunta == 'select_multiple':
            pregunta_form, opcion_form = PreguntaFactory.crear_pregunta(tipo_pregunta, request.POST)
            if pregunta_form.is_valid():
                pregunta = pregunta_form.save(commit=False)
                pregunta.encuesta = encuesta
                pregunta.save()
                # Guardar las opciones
                opciones = request.POST.getlist('opciones')
                for opcion_texto in opciones:
                    if opcion_texto:  # Guardar solo si no está vacío
                        OpcionPreguntaSelectMultiple.objects.create(pregunta=pregunta, opcion=opcion_texto)
                messages.success(request, 'Pregunta de selección múltiple agregada correctamente a la encuesta')
                return redirect('encuesta', encuesta_id=encuesta_id)
            else:
                form = pregunta_form  # En caso de error, definir 'form' para renderizado
                messages.error(request, 'Hubo un error al agregar la pregunta. Por favor, verifica los datos ingresados.')
        else:
            form = PreguntaFactory.crear_pregunta(tipo_pregunta, request.POST)
            if form.is_valid():
                pregunta = form.save(commit=False)
                pregunta.encuesta = encuesta
                pregunta.save()
                messages.success(request, 'Pregunta agregada correctamente a la encuesta')
                return redirect('encuesta', encuesta_id=encuesta_id)
            else:
                messages.error(request, 'Hubo un error al agregar la pregunta. Por favor, verifica los datos ingresados.')
    else:
        if tipo_pregunta == 'select_multiple':
            form, opcion_form = PreguntaFactory.crear_pregunta(tipo_pregunta)
        elif tipo_pregunta in ['general', 'si_o_no', 'numerica']:
            form = PreguntaFactory.crear_pregunta(tipo_pregunta)
        else:
            form = None
            messages.error(request, 'Tipo de pregunta no válido')

    return render(request, 'pregunta/agregar_pregunta.html', {
        'form': form, 
        'opcion_form': opcion_form, 
        'tipo_pregunta': tipo_pregunta, 
        'encuesta_id': encuesta_id,
        'encuesta': encuesta
    })

def editar_pregunta(request, encuesta_id, pregunta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    pregunta = None
    tipo_pregunta = request.GET.get('type', '')  # Obtener el tipo de pregunta
    try:
        if tipo_pregunta == 'general':
            pregunta = PreguntaGeneral.objects.get(pk=pregunta_id, encuesta=encuesta)
        elif tipo_pregunta == 'select_multiple':
            pregunta = PreguntaSelectMultiple.objects.get(pk=pregunta_id, encuesta=encuesta)
        elif tipo_pregunta == 'si_o_no':
            pregunta = PreguntaSiONo.objects.get(pk=pregunta_id, encuesta=encuesta)
        elif tipo_pregunta == 'numerica':
            pregunta = PreguntaNumerica.objects.get(pk=pregunta_id, encuesta=encuesta)
    except (PreguntaGeneral.DoesNotExist, PreguntaSelectMultiple.DoesNotExist, PreguntaSiONo.DoesNotExist, PreguntaNumerica.DoesNotExist):
        messages.error(request, 'La pregunta que intenta editar no existe.')
        return redirect('encuestaHome')

    form = PreguntaFactory.crear_pregunta(tipo_pregunta, instance=pregunta)

    if request.method == 'POST':
        form = PreguntaFactory.crear_pregunta(tipo_pregunta, request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pregunta editada correctamente')
            return redirect('encuesta', encuesta_id=encuesta_id)
        else:
            messages.error(request, 'Hubo un error al editar la pregunta. Por favor, verifica los datos ingresados.')
    
    return render(request, 'pregunta/editar_pregunta.html', {'form': form, 'encuesta_id': encuesta_id})

def eliminar_pregunta(request, encuesta_id, pregunta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    tipo_pregunta = request.GET.get('type', '')  # Obtener el tipo de pregunta
    try:
        if tipo_pregunta == 'general':
            pregunta = PreguntaGeneral.objects.get(pk=pregunta_id, encuesta=encuesta)
        elif tipo_pregunta == 'select_multiple':
            pregunta = PreguntaSelectMultiple.objects.get(pk=pregunta_id, encuesta=encuesta)
        elif tipo_pregunta == 'si_o_no':
            pregunta = PreguntaSiONo.objects.get(pk=pregunta_id, encuesta=encuesta)
        elif tipo_pregunta == 'numerica':
            pregunta = PreguntaNumerica.objects.get(pk=pregunta_id, encuesta=encuesta)
    except (PreguntaGeneral.DoesNotExist, PreguntaSelectMultiple.DoesNotExist, PreguntaSiONo.DoesNotExist, PreguntaNumerica.DoesNotExist):
        messages.error(request, 'La pregunta que intenta eliminar no existe.')
        return redirect('pagina_de_error')

    pregunta.delete()
    messages.success(request, 'Pregunta eliminada correctamente')
    return redirect('encuesta', encuesta_id=encuesta_id)

#INICIO APP ENCUESTAS - LISTA DE ENCUESTAS
def encuestaHome(request):
    return render(request, 'encuestaHome.html')

def encuestasPublicas(request):
    encuestas = Encuesta.objects.filter(tipoEncuesta='Publica')
    preguntas_por_encuesta = []
    for encuesta in encuestas:
        cantidad_preguntas = 0
        cantidad_respuestas = 0
        cantidad_respuestas += RespuestaEncuestaPublica.objects.filter(encuesta=encuesta).count()
        # Contar la cantidad de preguntas de cada tipo para esta encuesta
        cantidad_preguntas += PreguntaGeneral.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaSelectMultiple.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaSiONo.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaNumerica.objects.filter(encuesta=encuesta).count()
        preguntas_por_encuesta.append((encuesta, cantidad_preguntas, cantidad_respuestas))
        
    if not request.user.is_authenticated:
        return render(request, 'encuesta/lista_encuestas/encuestasPublicas.html', {'encuestas': encuestas, 'preguntas_por_encuesta': preguntas_por_encuesta})
    else:
        return render(request, 'encuesta/lista_encuestas/encuestasPublicas.html')

@login_super_staff_required
@validar_permisos_required(permission_required='app_encuesta.view_encuesta')
def encuestasPrivadas(request):
    encuestas = Encuesta.objects.filter(tipoEncuesta='Privada')
    preguntas_por_encuesta = []
    for encuesta in encuestas:
        cantidad_preguntas = 0
        cantidad_respuestas = 0
        cantidad_respuestas += RespuestaEncuestaPublica.objects.filter(encuesta=encuesta).count()
        # Contar la cantidad de preguntas de cada tipo para esta encuesta
        cantidad_preguntas += PreguntaGeneral.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaSelectMultiple.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaSiONo.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaNumerica.objects.filter(encuesta=encuesta).count()
        preguntas_por_encuesta.append((encuesta, cantidad_preguntas, cantidad_respuestas))

    if request.user.is_authenticated:
        return render(request, 'encuesta/lista_encuestas/encuestasPrivadas.html', {'encuestas': encuestas, 'preguntas_por_encuesta': preguntas_por_encuesta})
    else:
        return render(request, 'encuesta/lista_encuestas/encuestasPrivadas.html')

        
#CRUD RESPUESTA DE ENCUESTA
def responder_encuesta(request, encuesta_id):
    encuesta = Encuesta.objects.get(pk=encuesta_id)
    preguntas = []

    # Obtener todas las preguntas de la encuesta
    preguntas_general = PreguntaGeneral.objects.filter(encuesta=encuesta)
    preguntas_select_multiple = PreguntaSelectMultiple.objects.filter(encuesta=encuesta)
    preguntas_si_o_no = PreguntaSiONo.objects.filter(encuesta=encuesta)
    preguntas_numerica = PreguntaNumerica.objects.filter(encuesta=encuesta)

    # Manejar el envío del formulario
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipoDocumento = request.POST.get('tipoDocumento')
        numeroDocumento = request.POST.get('numeroDocumento')

        # Crear una instancia de RespuestaEncuesta y guardarla
        respuesta_encuesta = RespuestaEncuestaPublica(nombre=nombre, tipoDocumento=tipoDocumento, numeroDocumento=numeroDocumento, encuesta=encuesta)
        respuesta_encuesta.save()

        # Guardar las respuestas para cada tipo de pregunta
        for pregunta_general in preguntas_general:
            respuesta_texto = request.POST.get(f"respuesta_general_{pregunta_general.id}")
            respuesta_pregunta_general = RespuestaPreguntaGeneral(pregunta=pregunta_general, respuesta=respuesta_texto)
            respuesta_pregunta_general.save()

        for pregunta_select_multiple in preguntas_select_multiple:
            respuesta_opcion = request.POST.get(f"respuesta_select_multiple_{pregunta_select_multiple.id}")
            respuesta_pregunta_select_multiple = RespuestaPreguntaSelectMultiple(pregunta=pregunta_select_multiple, respuesta=respuesta_opcion)
            respuesta_pregunta_select_multiple.save()

        for pregunta_si_o_no in preguntas_si_o_no:
            respuesta_opcion = request.POST.get(f"respuesta_si_o_no_{pregunta_si_o_no.id}")
            respuesta_pregunta_si_o_no = RespuestaPreguntaSiONo(pregunta=pregunta_si_o_no, respuesta=respuesta_opcion)
            respuesta_pregunta_si_o_no.save()

        for pregunta_numerica in preguntas_numerica:
            respuesta_numero = request.POST.get(f"respuesta_numerica_{pregunta_numerica.id}")
            respuesta_pregunta_numerica = RespuestaPreguntaNumerica(pregunta=pregunta_numerica, respuesta=respuesta_numero)
            respuesta_pregunta_numerica.save()

        messages.success(request, 'Respuestas guardadas correctamente')
        return redirect('encuestaHome')

    # Preparar los datos para enviar a la plantilla
    for pregunta in preguntas_general:
        preguntas.append({'tipo_pregunta': 'general', 'pregunta': pregunta})

    for pregunta in preguntas_select_multiple:
        preguntas.append({'tipo_pregunta': 'select_multiple', 'pregunta': pregunta})

    for pregunta in preguntas_si_o_no:
        preguntas.append({'tipo_pregunta': 'si_o_no', 'pregunta': pregunta})

    for pregunta in preguntas_numerica:
        preguntas.append({'tipo_pregunta': 'numerica', 'pregunta': pregunta})

    return render(request, 'respuesta/responder_encuesta.html', {'encuesta': encuesta, 'preguntas': preguntas})

def ver_respuestas(request):
    encuestas = Encuesta.objects.all()
    return render(request, 'respuesta/ver_respuestas.html', {'encuestas': encuestas})
