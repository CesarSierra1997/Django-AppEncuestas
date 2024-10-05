from django.contrib import admin
from .models import *

class PreguntaGeneralInline(admin.TabularInline):
    model = PreguntaGeneral
    extra = 0

class PreguntaSelectMultipleInline(admin.TabularInline):
    model = PreguntaSelectMultiple
    extra = 0

class PreguntaSiONoInline(admin.TabularInline):
    model = PreguntaSiONo
    extra = 0

class PreguntaNumericaInline(admin.TabularInline):
    model = PreguntaNumerica
    extra = 0

class EncuestaAdmin(admin.ModelAdmin):
    inlines = [PreguntaGeneralInline, PreguntaSelectMultipleInline, PreguntaSiONoInline, PreguntaNumericaInline]

admin.site.register(Encuesta, EncuestaAdmin)
