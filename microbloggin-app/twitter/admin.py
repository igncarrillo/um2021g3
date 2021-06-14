from codecs import register
from django.contrib import admin

# Register your models here.

from .models import Publicacion, Usuario


admin.site.register(Usuario)
admin.site.register(Publicacion)