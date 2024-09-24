from django.contrib import admin
from .models import Usuario
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# Register your models here.
admin.site.register(Usuario),
admin.site.register(Permission),
admin.site.register(ContentType),

