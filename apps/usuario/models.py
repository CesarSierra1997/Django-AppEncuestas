from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UsuarioManager(BaseUserManager):
        def create_user(self, email, username, nombres, password = None):
            if not email:
                raise ValueError('El usuario debe tener un correo electrónico!')
            
            user = self.model(
                username=username,
                email = self.normalize_email(email),
                nombres = nombres
            )

            user.set_password(password)
            user.save()
            return user
        
        def create_superuser(self, username, email, nombres, password):
            user = self.create_user(
            email,
            username =username,
            nombres =nombres,
            password=password
            )
            user.usuario_administrador = True
            user.save()
            return user
        
class Rol(models.Model):
    rol = models.CharField('Nombre del Rol', max_length=100, unique = True)
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['-id']
    
    def __str__(self):
        return self.rol
    
class Usuario(AbstractBaseUser):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cedula de Ciudadania'),
        ('TI', 'Tarjeta de Identidad'),
        ('PASAPORTE', 'Pasaporte'),
        ('REGISTRO CIVIL', 'Registro civil'),
    ]
    tipoDocumento = models.CharField('Tipo de Documento', max_length=20, choices=TIPO_DOCUMENTO_CHOICES, default=False)
    numeroDocumento = models.IntegerField('Digite su numero de documento', blank=False, null=False, default=False)
    username = models.CharField("Nombre de Usuario",unique=True, max_length=50)
    email = models.EmailField('Correo Electrónico', max_length=254, unique =True)
    nombres = models.CharField('Nombres', max_length=200, blank= True, null =True)
    apellidos= models.CharField('Apellidos ', max_length=200, blank= True, null =True)
    usuario_activo = models.BooleanField(default = True)
    usuario_administrador = models.BooleanField(default = False)
    objects = UsuarioManager()
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True )
    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'nombres']

    def __str__ (self):
        return f'{self.nombres}, {self.apellidos}'

    def has_perm(self,perm,obj = None):
        return True

    def has_nodule_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador
    
    def has_module_perms(self, app_label):
        return True
    