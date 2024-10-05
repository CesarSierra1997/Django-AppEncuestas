from django.urls import reverse
from django.test import TestCase

class EncuestaURLTests(TestCase):

    def test_encuestaHome_url(self):
        url = reverse('encuesta:encuestaHome')
        self.assertEqual(url, '/encuestaHome/')  # Verifica que la URL sea la correcta

    def test_inicio_encuestas_url(self):
        url = reverse('encuesta:inicio_encuestas')
        self.assertEqual(url, '/inicio_encuestas/')  # Verifica la URL de inicio de encuestas

    def test_crear_encuesta_url(self):
        url = reverse('encuesta:crear_encuesta')
        self.assertEqual(url, '/crear_encuesta/')  # Verifica la URL para crear encuesta

    def test_editar_encuesta_url(self):
        url = reverse('encuesta:editar_encuesta', kwargs={'encuesta_id': 1})
        self.assertEqual(url, '/editar_encuesta/1/')  # Verifica la URL de editar encuesta

    def test_eliminar_encuesta_url(self):
        url = reverse('encuesta:eliminar_encuesta', kwargs={'encuesta_id': 1})
        self.assertEqual(url, '/eliminar_encuesta/1/')  # Verifica la URL de eliminar encuesta

    def test_publicar_encuesta_url(self):
        url = reverse('encuesta:publicar_encuesta', kwargs={'encuesta_id': 1})
        self.assertEqual(url, '/publicar_encuesta/1/')  # Verifica la URL de publicar encuesta

    def test_ver_encuestas_publicas_url(self):
        url = reverse('encuesta:ver_encuestas_publicas')
        self.assertEqual(url, '/encuestas_publicas/')  # Verifica la URL de ver encuestas públicas

    def test_buscar_url(self):
        url = reverse('encuesta:buscar')
        self.assertEqual(url, '/buscar/')  # Verifica la URL de buscar
