from django.db import models

# MODELOS PARA EL ADMINISTRADOR QUE CREA ENCUESTAS
#ENCUESTA
class Encuesta(models.Model):
    titulo = models.CharField('Titulo de la encuesta', max_length=200, blank=False, null=False)

#TIPOS DE PREGUNTAS:
class PreguntaGeneral(models.Model):
    texto_pre = models.CharField('Digite la pregunta general', max_length=200, blank=False, null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

class PreguntaSelectMultiple(models.Model):
    texto_pre = models.CharField('Digite la pregunta de selección multiple', max_length=200, blank=False, null=False)
    opcion_a = models.CharField('Opción a', max_length=255)
    opcion_b = models.CharField('Opción b', max_length=255)
    opcion_c = models.CharField('Opción c', max_length=255)
    opcion_d = models.CharField('Opción d', max_length=255)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

class PreguntaSiONo(models.Model):
    texto_pre = models.CharField('Digite la pregunta de sí o no', max_length=200, blank=False, null=False)
    opcion = models.BooleanField('Seleccione una opción', max_length=200, blank=False, null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

class PreguntaNumerica(models.Model):
    texto_pre = models.CharField('Digite la pregunta numérica', max_length=200, blank=False, null=False)
    rango = models.IntegerField('Rango mínimo 1 rango maximo 10', default=1)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

#RESPUESTA ENCUESTA
class RespuestaEncuesta(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cedula de Ciudadania'),
        ('TI', 'Tarjeta de Identidad'),
        ('PASAPORTE', 'Pasaporte'),
        ('REGISTRO CIVIL', 'Registro civil'),
    ]
    tipoDocumento = models.CharField('Tipo de Documento', max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    numeroDocumento = models.CharField('Digite su numero de documento', max_length=12)
    nombreUsuario = models.CharField('Digite su nombre', max_length=200, blank=False, null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_preguntas')

#RESPUESTAS DE TIPOS DE PREGUNTAS
class RespuestaPreguntaGeneral(models.Model):
    pregunta = models.ForeignKey(PreguntaGeneral, on_delete=models.CASCADE, related_name='respuesta_pregunta_general')
    respuesta =  models.CharField('Digite su respuesta', max_length=200, blank=False, null=False)

class RespuestaPreguntaSelectMultiple(models.Model):
    pregunta = models.ForeignKey(PreguntaSelectMultiple, on_delete=models.CASCADE, related_name='respuesta_pregunta_selectMultiple')
    respuesta =  models.CharField('Seleccione una opción', max_length=200, blank=False, null=False)

class RespuestaPreguntaSiONo(models.Model):
    pregunta = models.ForeignKey(PreguntaSiONo, on_delete=models.CASCADE, related_name='respuesta_pregunta_siOno')
    respuesta =  models.BooleanField('Seleccione Si o No', max_length=200, blank=False, null=False)

class RespuestaPreguntaNumerica(models.Model):
    pregunta = models.ForeignKey(PreguntaNumerica, on_delete=models.CASCADE, related_name='respuesta_pregunta_numerica')
    respuesta =  models.IntegerField('Digite un numero de respuesta', blank=False, null=False)

