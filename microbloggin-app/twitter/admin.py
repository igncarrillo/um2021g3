from codecs import register
from django.contrib import admin

# Register your models here.

from .models import Usuario


admin.site.register(Usuario)