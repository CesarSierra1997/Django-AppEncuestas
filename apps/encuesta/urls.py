from django.urls import path
from . import views

app_name = 'encuesta'  # Nombre del grupo de URLs para la app encuesta

# Agrupación de rutas relacionadas a encuestas
urlpatterns = [
    # Ruta principal de la aplicación de encuestas
    path('encuestaHome/', views.EncuestaHomeApp.as_view(), name='encuestaHome'),

    # Rutas exclusivas para administradores con permisos
    path('inicio_encuestas/', views.InicioEncuestas.as_view(), name='inicio_encuestas'),
    path('crear_encuesta/', views.CrearEncuesta.as_view(), name='crear_encuesta'),
    path('editar_encuesta/<int:encuesta_id>/', views.EditarEncuesta.as_view(), name='editar_encuesta'),
    path('eliminar_encuesta/<int:encuesta_id>/', views.EliminarEncuesta.as_view(), name='eliminar_encuesta'),
    path('publicar_encuesta/<int:encuesta_id>/', views.PublicarEncuesta.as_view(), name='publicar_encuesta'),

    # Rutas para las preguntas de una encuesta específica
    path('encuesta/<int:encuesta_id>/', views.EncuestaDetail.as_view(), name='encuesta_detail'),
    path('encuesta/agregar_pregunta/<int:encuesta_id>/', views.AgregarPregunta.as_view(), name='agregar_pregunta'),
    path('encuesta/agregar_pregunta_opciones/<int:pregunta_id>/', views.OpcionPregunta_SelectMultiple.as_view(), name='agregar_opciones'),
    path('encuesta/editar_pregunta/<int:encuesta_id>/pregunta/<int:pregunta_id>/', views.EditarPregunta.as_view(), name='editar_pregunta'),
    path('encuesta/eliminar_pregunta/<int:encuesta_id>/pregunta/<int:pregunta_id>/', views.EliminarPregunta.as_view(), name='eliminar_pregunta'),

    # Ruta para ver las encuestas publicadas, activas y vigentes
    path('encuestas_publicas/', views.VerEncuestasPublicas.as_view(), name='ver_encuestas_publicas'),
    path('encuesta/encuestas_privadas', views.VerEncuestasPrivadas.as_view(), name='ver_encuestas_privadas'),


    # Rutas para las respuestas
    path('responder_publica/<int:encuesta_id>/', views.ResponderEncuestaPublica.as_view(), name='responder_encuesta_publica'),


    path('responder_encuesta_privada/<int:encuesta_id>/', views.ResponderEncuestaPrivada.as_view(), name='responder_encuesta_privada'),

    path('ver_respuestas/', views.VerRespuestas.as_view(), name='ver_respuestas'),
    path('exportar-respuestas-publicas/', views.ExportarRespuestasPublicasExcel.as_view(), name='exportar_respuestas_publicas'),
]
