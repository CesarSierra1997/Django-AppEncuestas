from django.urls import path
from . import views


urlpatterns = [
    path('crear_encuesta/', views.crear_encuesta, name='crear_encuesta'),
    path('eliminar_encuesta/<int:encuesta_id>/', views.eliminar_encuesta, name='eliminar_encuesta'),
    path('agregar_pregunta/<int:encuesta_id>/', views.agregar_pregunta, name='agregar_pregunta'),
    path('agregar_pregunta/<int:encuesta_id>/pregunta.html', views.pregunta, name='pregunta'),
    path('encuesta/<int:encuesta_id>/', views.encuesta, name='encuesta'),
    path('home/', views.encuestaHome, name='encuestaHome'),
    path('responder_encuesta/<int:encuesta_id>/', views.responder_encuesta, name='responder_encuesta'), 
    path('ver_respuestas/', views.ver_respuestas, name='ver_respuestas'),
    path('buscar/', views.buscar, name='buscar'),
]