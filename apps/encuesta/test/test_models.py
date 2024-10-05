from django.test import TestCase
from ..models import Encuesta, Pregunta, OpcionesPregunta, RespuestaEncuestaPublica, RespuestaEncuestaPrivada, Respuesta
from apps.usuario.models import Usuario
from django.utils import timezone
from django.test import TestCase
from django.utils import timezone
from apps.usuario.models import Usuario

class EncuestaModelTests(TestCase):

    def setUp(self):
        self.administrador = Usuario.objects.create(username="admin", password="admin")
        self.encuesta = Encuesta.objects.create(
            titulo="Encuesta de Prueba",
            tipoEncuesta="Publica",
            administrador=self.administrador,
            fechaInicio=timezone.now(), 
            fechaFinal=timezone.now() + timezone.timedelta(days=5)
        )

    def test_encuesta_str(self):
        self.assertEqual(str(self.encuesta), "Encuesta de Prueba - tipo Publica")

    def test_fecha_inicio_no_nula(self):
        self.assertIsNotNone(self.encuesta.fechaInicio)

    def test_tipo_encuesta_default(self):
        # Crear una encuesta sin especificar tipoEncuesta
        encuesta_default = Encuesta.objects.create(
            titulo="Encuesta por Defecto",
            administrador=self.administrador,
            fechaInicio=timezone.now(),
            fechaFinal=timezone.now() + timezone.timedelta(days=5)
        )
        self.assertEqual(encuesta_default.tipoEncuesta, 'Publica')  # Asegúrate de que el valor por defecto sea el correcto


class PreguntaModelTests(TestCase):

    def setUp(self):
        self.administrador = Usuario.objects.create(username="admin", password="admin")
        self.encuesta = Encuesta.objects.create(
            titulo="Encuesta de Prueba",
            tipoEncuesta="Publica",
            administrador=self.administrador,
            fechaInicio=timezone.now(),
            fechaFinal=timezone.now() + timezone.timedelta(days=5)
        )
        self.pregunta = Pregunta.objects.create(
            tipoPregunta="1",
            texto_pregunta="¿Cómo calificarías nuestro servicio?",
            encuesta=self.encuesta
        )

    def test_pregunta_str(self):
        self.assertEqual(str(self.pregunta), "¿Cómo calificarías nuestro servicio?")

class OpcionesPreguntaModelTests(TestCase):

    def setUp(self):
        self.administrador = Usuario.objects.create(username="admin", password="admin")
        self.encuesta = Encuesta.objects.create(
            titulo="Encuesta de Prueba",
            tipoEncuesta="Publica",
            administrador=self.administrador,
            fechaInicio=timezone.now(),
            fechaFinal=timezone.now() + timezone.timedelta(days=5)
        )
        self.pregunta = Pregunta.objects.create(
            tipoPregunta="1",
            texto_pregunta="¿Cómo calificarías nuestro servicio?",
            encuesta=self.encuesta
        )
        self.opciones = OpcionesPregunta.objects.create(
            opcion_1="Excelente",
            opcion_2="Bueno",
            opcion_3="Regular",
            opcion_4="Malo",
            pregunta=self.pregunta
        )

    def test_opciones_str(self):
        self.assertEqual(str(self.opciones), f"Opciones para la pregunta: {self.pregunta.texto_pregunta}")

class RespuestaEncuestaPublicaModelTests(TestCase):

    def setUp(self):
        self.administrador = Usuario.objects.create(username="admin", password="admin")
        self.encuesta = Encuesta.objects.create(
            titulo="Encuesta de Prueba",
            tipoEncuesta="Publica",
            administrador=self.administrador,
            fechaInicio=timezone.now(),
            fechaFinal=timezone.now() + timezone.timedelta(days=5)
        )
        self.respuesta_publica = RespuestaEncuestaPublica.objects.create(
            tipoUsuario='1',
            tipoDocumento='CC',
            numeroDocumento='123456789',
            nombre='Juan Pérez',
            email='juan@example.com',
            encuesta=self.encuesta
        )

    def test_respuesta_publica_str(self):
        self.assertEqual(str(self.respuesta_publica), f"{self.respuesta_publica.nombre} - {self.respuesta_publica.numeroDocumento}")

class RespuestaModelTests(TestCase):

    def setUp(self):
        self.administrador = Usuario.objects.create(username="admin", password="admin")
        self.encuesta = Encuesta.objects.create(
            titulo="Encuesta de Prueba",
            tipoEncuesta="Publica",
            administrador=self.administrador,
            fechaInicio=timezone.now(),
            fechaFinal=timezone.now() + timezone.timedelta(days=5)
        )
        self.pregunta = Pregunta.objects.create(
            tipoPregunta="1",
            texto_pregunta="¿Cómo calificarías nuestro servicio?",
            encuesta=self.encuesta
        )
        self.respuesta_publica = RespuestaEncuestaPublica.objects.create(
            tipoUsuario='1',
            tipoDocumento='CC',
            numeroDocumento='123456789',
            nombre='Juan Pérez',
            email='juan@example.com',
            encuesta=self.encuesta
        )
        self.respuesta = Respuesta.objects.create(
            texto_respuesta="Excelente",
            pregunta=self.pregunta,
            respuestaEncuestaPublica=self.respuesta_publica
        )

    def test_respuesta_str(self):
        self.assertEqual(str(self.respuesta), f"{self.respuesta.texto_respuesta}")
