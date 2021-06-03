from abc import abstractclassmethod
from typing import ContextManager
from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import CASCADE
from django.db.models.fields.mixins import FieldCacheMixin
#from jsonfield import JSONField

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=16, default='')
    telefono = models.PositiveIntegerField()
    nombre = models.CharField(max_length=255, default='')
    apellido = models.CharField(max_length=255, default='')
    TIPOS_SEXO = [
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino'),
        ('OTRO', 'Otro')
    ]
    sexo = models.CharField(
        max_length=14,
        choices=TIPOS_SEXO,
        default='Masculino',
    )
    fechaNac = models.DateField(default="1930-01-01")
    email = models.EmailField(max_length=254)

    class META:
        abstract = True

    def __str__(self):
        return f'NombreUsuario:{self.nombre_usuario}, Email:{self.email}'

class Usuario(User):
    seguidores = models.JSONField(default=None)
    seguidos = models.JSONField(default=None)

class Administrador(User):
    pass

class Publicacion(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=CASCADE, related_name='realizada')
    contenido = models.CharField(max_length=254, default='')
    etiqueta = models.JSONField(default=None)
    mencion = models.ForeignKey(Usuario, on_delete=CASCADE, default=None, related_name='menciona')
    fecha = models.DateField(auto_now_add=True)
    republicacion = models.ForeignKey('self', null=True, on_delete=CASCADE, related_name='republica')

class Tendencias(models.Model):
    id = models.AutoField(primary_key=True) #Una tendencia lleva id??
    #fecha
    etiqueta = models.ForeignKey(Publicacion, on_delete=CASCADE)
    #contador

class MensajePriv(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    contenido = models.CharField(max_length=254, default='')
    receptor = models.ForeignKey(Usuario, on_delete=CASCADE, related_name= 'recibe')
    emisor = models.ForeignKey(Usuario, on_delete=CASCADE, related_name= 'emite')


