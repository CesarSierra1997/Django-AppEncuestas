from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UsuarioManager(BaseUserManager):
        def _create_user(self, username, email, nombres, apellidos, password, is_staff, is_superuser, **extra_fields):
            user = self.model(
                username = username,
                email = email,
                nombres = nombres,
                apellidos = apellidos,
                is_staff = is_staff,
                is_superuser = is_superuser,
                **extra_fields
            )
            user.set_password(password)
            user.save(using=self.db)
            return user
        
        def create_user(self, username, email, nombres, apellidos, password = None, **extra_fields):
             return self._create_user(username, email, nombres, apellidos, password, False, False, **extra_fields)
        
        def create_superuser(self, username, email, nombres, apellidos, password = None, **extra_fields):
             return self._create_user(username, email, nombres, apellidos, password, True, True, **extra_fields)



class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("Nombre de Usuario",unique=True, max_length=20)
    email = models.EmailField('Correo Electrónico', max_length=30, unique =True)
    nombres = models.CharField('Nombres', max_length=30, blank= True, null =True)
    apellidos= models.CharField('Apellidos ', max_length=30, blank= True, null =True)
    imagen = models.ImageField('Imagen de Perfil', upload_to ='perfil/', height_field=None, width_field=None, max_length=200, blank= True,)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UsuarioManager()
    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos']

    def __str__ (self):
        return f'{self.nombres} {self.apellidos}'
