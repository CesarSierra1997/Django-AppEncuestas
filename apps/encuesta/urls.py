from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    #RUTAS 
    path('/', views, name=''),

]