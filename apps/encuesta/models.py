from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.usuario.models import Usuario


# ENCUESTA
class Encuesta(models.Model):
    titulo = models.CharField('Título de la encuesta', max_length=50, blank=False, null=False)
    TIPO_ENCUESTA = [
        ('Publica', 'Encuesta pública'),
        ('Privada', 'Encuesta privada'),
    ]
    tipoEncuesta = models.CharField('Tipo de Encuesta', max_length=50, choices=TIPO_ENCUESTA, default='Publica')
    administrador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(null=False)
    fechaFinal = models.DateTimeField(null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    @property
    def esta_activa(self):
        """Determina si la encuesta está activa en función de las fechas."""
        now = timezone.now()
        return self.fechaInicio <= now <= self.fechaFinal

# PREGUNTA
class Pregunta(models.Model):
    TIPO_PREGUNTA_CHOICES = [
        ('1', 'Pregunta general'),
        ('2', 'Pregunta tipo sí o no'),
        ('3', 'Pregunta numérica'),
        ('4', 'Pregunta tipo selección múltiple'),
    ]
    tipoPregunta = models.CharField('Seleccione el tipo de pregunta', max_length=30, choices=TIPO_PREGUNTA_CHOICES)
    texto_pregunta = models.CharField('Digite la pregunta', max_length=200, blank=False, null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    def tiene_opciones(self):
        """Verifica que las preguntas de selección múltiple tengan opciones."""
        if self.tipoPregunta == '4':
            return self.opciones.all().exists()
        return True

# OPCION DE PREGUNTA
class OpcionPregunta(models.Model):
    texto_opcion = models.CharField('Digite la opción', max_length=100, blank=False, null=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="opciones")

# RESPUESTA ENCUESTA PÚBLICA
class RespuestaEncuestaPublica(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('PASAPORTE', 'Pasaporte'),
        ('REGISTRO_CIVIL', 'Registro civil'),
    ]
    tipoDocumento = models.CharField('Tipo de Documento', max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    numeroDocumento = models.CharField('Digite su número de documento', max_length=20, blank=False, null=False, unique=True)
    nombre = models.CharField('Digite su nombre completo', max_length=50, blank=False, null=False)
    email = models.EmailField('Correo Electrónico', max_length=254)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_preguntas_publica')

# RESPUESTA ENCUESTA PRIVADA
class RespuestaEncuestaPrivada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='usuario_encuesta')
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_preguntas_privada')

# RESPUESTA A PREGUNTAS
class Respuesta(models.Model):
    texto_respuesta = models.CharField('Digite su respuesta', max_length=200, blank=False, null=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuesta_pregunta')
    respuestaEncuestaPublica = models.ForeignKey(RespuestaEncuestaPublica, on_delete=models.CASCADE, related_name='respuesta_encuesta_publica', null=True, blank=True)
    respuestaEncuestaPrivada = models.ForeignKey(RespuestaEncuestaPrivada, on_delete=models.CASCADE, related_name='respuesta_encuesta_privada', null=True, blank=True)

    def clean(self):
        """Valida que una respuesta pertenezca solo a una encuesta pública o privada."""
        if self.respuestaEncuestaPublica and self.respuestaEncuestaPrivada:
            raise ValidationError("Una respuesta solo puede estar vinculada a una encuesta pública o privada, no a ambas.")
