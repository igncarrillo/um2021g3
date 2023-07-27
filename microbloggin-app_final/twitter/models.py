from abc import abstractclassmethod
from typing import ContextManager
from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import CASCADE
from django.db.models.fields.mixins import FieldCacheMixin
#from jsonfield import JSONField

# Create your models here.

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=255, default='')
    contraseña=models.CharField(max_length=255)
    telefono = models.PositiveIntegerField(default=99999999)
    nombre = models.CharField(max_length=255, default='')
    apellido = models.CharField(max_length=255, default='')
    TIPOS_SEXO = [
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino'),
        ('OTRO', 'Otro')]
    sexo = models.CharField(
        max_length=14,
        choices=TIPOS_SEXO,
        default='Masculino',
    )
    fecha_nacimiento = models.DateField(default="1999-01-01")
    email = models.EmailField(max_length=254, default="ejemplo@gmail.com")

    def __str__(self):
        return f'NombreUsuario: {self.nombre_usuario}, Email: {self.email}'
    
    def login(self,contraseña):
        return contraseña==self.contraseña

class RelacionSeguidor(models.Model):
    seguido = models.ForeignKey(Usuario, on_delete=CASCADE, related_name="follower")
    seguidores = models.ForeignKey(Usuario, on_delete=CASCADE, related_name="followed")

class Publicacion(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=CASCADE, related_name='realizada')
    contenido = models.CharField(max_length=254, default='')
    etiqueta = models.JSONField(default=str, null=True, blank=True)
    mencion = models.ForeignKey(Usuario, null=True, blank=True, on_delete=CASCADE, default=None, related_name='menciona')
    fecha = models.DateField(auto_now_add=True)
    republicacion = models.ForeignKey('self', null=True, blank=True, on_delete=CASCADE, related_name='republica')
    is_edited = models.BooleanField(default=False)


    def __str__(self):
        return f'Publicacion: {self.contenido}, Usuario: {self.usuario.nombre_usuario}'
    
class Tendencias(models.Model):
    id = models.AutoField(primary_key=True) 
    #fecha
    etiqueta = models.ForeignKey(Publicacion, on_delete=CASCADE)
    #contador

class MensajePriv(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    contenido = models.CharField(max_length=254, default='')
    receptor = models.ForeignKey(Usuario, on_delete=CASCADE, related_name= 'recibe')
    emisor = models.ForeignKey(Usuario, on_delete=CASCADE, related_name= 'emite')
