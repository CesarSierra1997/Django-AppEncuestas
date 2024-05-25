from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    #RUTAS PRIVADAS
    path('home/',   views.encuestaHome, name='encuestaHome'),
    #encuesta
    path('crear_encuesta/', login_required(views.crear_encuesta), name='crear_encuesta'),
    path('editar_encuesta/<int:encuesta_id>/', login_required(views.editar_encuesta), name='editar_encuesta'),
    path('eliminar_encuesta/<int:encuesta_id>/', login_required(views.eliminar_encuesta), name='eliminar_encuesta'),
    path('encuesta/<int:encuesta_id>/', login_required(views.encuesta), name='encuesta'),
    #pregunta
    path('agregar_pregunta/<int:encuesta_id>/', login_required(views.agregar_pregunta), name='agregar_pregunta'),
    path('agregar_pregunta/<int:encuesta_id>/pregunta.html', login_required(views.pregunta), name='pregunta'),
    path('editar_encuesta/<int:encuesta_id>/editar_pregunta/<int:pregunta_id>/', login_required(views.editar_pregunta), name='editar_pregunta'),
    path('<int:encuesta_id>/pregunta/<int:pregunta_id>/eliminar/', login_required(views.eliminar_pregunta), name='eliminar_pregunta'),

    #RUTAS PUBLICAS
    #respuesta
    path('responder_encuesta/<int:encuesta_id>/', views.responder_encuesta, name='responder_encuesta'), 
    path('ver_respuestas/', login_required(views.ver_respuestas), name='ver_respuestas'),
    path('buscar/', login_required(views.buscar), name='buscar'),
]