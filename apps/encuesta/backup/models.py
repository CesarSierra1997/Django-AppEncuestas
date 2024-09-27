from django.db import models
from apps.usuario.models import Usuario

# MODELOS PARA EL ADMINISTRADOR QUE CREA ENCUESTAS
#ENCUESTA
class Encuesta(models.Model):
    titulo = models.CharField('Titulo de la encuesta', max_length=200, blank=False, null=False)
    TIPO_ENCUESTA = [
        ('Publica', 'Encuesta pública'),
        ('Privada', 'Encuesta privada'),
    ]
    tipoEncuesta = models.CharField('Tipo de Encuesta', max_length=50, choices=TIPO_ENCUESTA, default=False)
#TIPOS DE PREGUNTAS:
class PreguntaGeneral(models.Model):
    texto_pre = models.CharField('Digite la pregunta general', max_length=200, blank=False, null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

class PreguntaSelectMultiple(models.Model):
    texto_pre = models.CharField('Digite la pregunta de selección multiple', max_length=200, blank=False, null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

class OpcionPreguntaSelectMultiple(models.Model):
    opcion = models.CharField('Opción', max_length=255)
    pregunta = models.ForeignKey(PreguntaSelectMultiple, on_delete=models.CASCADE, related_name='opciones')

class PreguntaSiONo(models.Model):
    texto_pre = models.CharField('Digite la pregunta de sí o no', max_length=200, blank=False, null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

class PreguntaNumerica(models.Model):
    texto_pre = models.CharField('Digite la pregunta numérica', max_length=200, blank=False, null=False)
    rango = models.IntegerField('Rango de la encuesta: mínimo 1 rango, maximo 10', default=1)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

#RESPUESTA ENCUESTA
#Tipo de encuestas
class RespuestaEncuestaPublica(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cedula de Ciudadania'),
        ('TI', 'Tarjeta de Identidad'),
        ('PASAPORTE', 'Pasaporte'),
        ('REGISTRO CIVIL', 'Registro civil'),
    ]
    tipoDocumento = models.CharField('Tipo de Documento', max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    numeroDocumento = models.IntegerField('Digite su numero de documento', blank=False, null=False)
    nombre = models.CharField('Digite su nombre completo', max_length=200, blank=False, null=False)
    email = models.EmailField('Correo Electrónico', max_length=254)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_preguntas')

class RespuestaEncuestaPrivada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='usuario_encuesta')
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_preguntas_privada')

#RESPUESTAS DE TIPOS DE PREGUNTAS
#Tipos de respuestas
class RespuestaPreguntaGeneral(models.Model):
    pregunta = models.ForeignKey(PreguntaGeneral, on_delete=models.CASCADE, related_name='respuesta_pregunta_general')
    respuesta =  models.CharField('Digite su respuesta', max_length=200, blank=False, null=False)

class RespuestaPreguntaSelectMultiple(models.Model):
    pregunta = models.ForeignKey(PreguntaSelectMultiple, on_delete=models.CASCADE, related_name='respuesta_pregunta_selectMultiple')
    respuesta =  models.ForeignKey(OpcionPreguntaSelectMultiple, on_delete=models.CASCADE, related_name='opcion_respuesta_pregunta_selectMultiple')

class RespuestaPreguntaSiONo(models.Model):
    pregunta = models.ForeignKey(PreguntaSiONo, on_delete=models.CASCADE, related_name='respuesta_pregunta_siOno')
    respuesta =  models.BooleanField('Seleccione Si o No', max_length=200, blank=False, null=False)

class RespuestaPreguntaNumerica(models.Model):
    pregunta = models.ForeignKey(PreguntaNumerica, on_delete=models.CASCADE, related_name='respuesta_pregunta_numerica')
    respuesta =  models.IntegerField('Digite un numero de respuesta', blank=False, null=False)

