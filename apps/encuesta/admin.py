from django.contrib import admin
from .models import Encuesta, Pregunta, OpcionesPregunta

# Inline para agregar preguntas relacionadas a la Encuesta
class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1  # Muestra un formulario vacío adicional para agregar preguntas

# Inline para agregar opciones relacionadas a la Pregunta
class OpcionesPreguntaInline(admin.TabularInline):
    model = OpcionesPregunta
    extra = 1  # Muestra un formulario adicional para agregar opciones

# Admin personalizado para el modelo Encuesta
@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'tipoEncuesta', 'fechaCreacion')  # Campos mostrados en la lista
    list_filter = ('estado', 'fechaCreacion')  # Filtros por estado y fecha de creación
    search_fields = ('titulo','tipoEncuesta')  # Búsqueda por título
    inlines = [PreguntaInline]  # Muestra preguntas relacionadas directamente en la encuesta

# Admin personalizado para el modelo Pregunta
@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto_pregunta', 'tipoPregunta', 'encuesta')  # Campos mostrados en la lista
    list_filter = ('tipoPregunta', 'encuesta')  # Filtros por tipo de pregunta y encuesta
    search_fields = ('texto_pregunta',)  # Búsqueda por el texto de la pregunta

# Admin personalizado para el modelo OpcionesPregunta
@admin.register(OpcionesPregunta)
class OpcionesPreguntaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'opcion_1', 'opcion_2', 'opcion_3', 'opcion_4')  # Campos mostrados en la lista
    search_fields = ('pregunta__texto_pregunta',)  # Búsqueda por el texto de la pregunta asociada
