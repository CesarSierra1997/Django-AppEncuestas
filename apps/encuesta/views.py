from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

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

def inicio(request):
    return render(request, 'index.html')
#ENCUESTA
def crear_encuesta(request):
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('encuesta', encuesta_id=form.instance.id)
    else:
        form = EncuestaForm()
    return render(request, 'encuesta/crear_encuesta.html', {'form': form})

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

#PREGUNTAS
class PreguntaFactory: 
    @staticmethod
    def crear_pregunta(tipo, *args, **kwargs):
        if tipo == 'general':
            return PreguntaGeneralForm(*args, **kwargs)
        elif tipo == 'select_multiple':
            return PreguntaSelectMultipleForm(*args, **kwargs)
        elif tipo == 'si_o_no':
            return PreguntaSiONoForm(*args, **kwargs)
        elif tipo == 'numerica':
            return PreguntaNumericaForm(*args, **kwargs)
        else:
            raise ValueError('Tipo de pregunta no válido RAISE class - PreguntaFactory : {}'.format(tipo))

def agregar_pregunta(request, encuesta_id):
    encuesta = Encuesta.objects.get(pk=encuesta_id)
    if request.method == 'POST':
        tipo_pregunta = request.POST.get('tipo_pregunta')
        form = PreguntaFactory.crear_pregunta(tipo_pregunta, request.POST)
        print("El tipo de pergunta en el BACK",tipo_pregunta)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.encuesta = encuesta
            pregunta.save()
            messages.success(request, 'Pregunta agregada correctamente a la encuesta')
            return redirect('encuesta', encuesta_id=encuesta_id)
        else:
            messages.error(request, 'Hubo un error al agregar la pregunta. Por favor, verifica los datos ingresados.')
    else:
        form = PreguntaFactory.crear_pregunta('si_o_no')  # Formulario por defecto
    
    return render(request, 'pregunta/agregar_pregunta.html', {'form': form})

def pregunta(request, encuesta_id):#render tipo de pregunta
    tipo_pregunta = request.GET.get('type', '')  # Obtener el tipo de pregunta desde los parámetros GET
    form = PreguntaFactory.crear_pregunta(tipo_pregunta)
    return render(request, 'pregunta/pregunta.html', {'tipo_pregunta': tipo_pregunta, 'form':form, 'encuesta_id': encuesta_id,})

def encuestaHome(request):
    encuestas = Encuesta.objects.all()
    respuestaEncuesta = RespuestaEncuesta.objects.all()
    preguntas_por_encuesta = []
    respuestas_por_encuesta = []
    for encuesta in encuestas:
        cantidad_preguntas = 0
        cantidad_respuestas = 0
        cantidad_respuestas += RespuestaEncuesta.objects.filter(encuesta=encuesta).count()
        # Contar la cantidad de preguntas de cada tipo para esta encuesta
        cantidad_preguntas += PreguntaGeneral.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaSelectMultiple.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaSiONo.objects.filter(encuesta=encuesta).count()
        cantidad_preguntas += PreguntaNumerica.objects.filter(encuesta=encuesta).count()
        preguntas_por_encuesta.append((encuesta, cantidad_preguntas, cantidad_respuestas))
        
    return render(request, 'encuestaHome.html', {'encuestas': encuestas, 'preguntas_por_encuesta': preguntas_por_encuesta})

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
        nombreUsuario = request.POST.get('nombreUsuario')
        tipoDocumento = request.POST.get('tipoDocumento')
        numeroDocumento = request.POST.get('numeroDocumento')

        # Crear una instancia de RespuestaEncuesta y guardarla
        respuesta_encuesta = RespuestaEncuesta(nombreUsuario=nombreUsuario, tipoDocumento=tipoDocumento, numeroDocumento=numeroDocumento, encuesta=encuesta)
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
