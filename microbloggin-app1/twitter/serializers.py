from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import DictField
from twitter.models import User, Usuario, Administrador, Publicacion, Tendencias, MensajePriv

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Administrador
        fields = {'id',
        'nombre_usuario',
        'telefono'
        'nombre',
        'apellido',
        'sexo'
        'fechaNac',
        'email',
        }

class PublicacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publicacion
        fields = '__all__'

class TendenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tendencias
        fields = {'id'
        'etiqueta'
        }

class MensajePrivSerializer(serializers.ModelSerializer):

    class Meta:
        model = MensajePriv
        fields = {'id'
        'fecha'
        'contenido'
        'receptor'
        'emisor'
        }