from django.contrib import admin

from .models import Publicacion, Usuario

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Publicacion)
