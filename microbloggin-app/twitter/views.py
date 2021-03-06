from collections import defaultdict
import re
from django.http.request import HttpRequest
from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.utils.json import strict_constant

from twitter.models import Usuario, Administrador, Publicacion, Tendencias, MensajePriv
from twitter.serializers import UsuarioSerializer, AdminSerializer, PublicacionSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST'])
def usuarios(request):
    if request.method == 'GET':
        try:
            usuarios = Usuario.objects.all()
        except Usuario.DoesNotExist:
            return JsonResponse({'Error': 'No existe ningun usuario'}, status=status.HTTP_404_NOT_FOUND)
        usuarios_serializer = UsuarioSerializer(usuarios, many = True)
        return JsonResponse(usuarios_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        usuario_data = JSONParser().parse(request)
        usuarios_serializer = UsuarioSerializer(data=usuario_data)
        if usuarios_serializer.is_valid():
            usuarios_serializer.save()
            return JsonResponse(usuarios_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(usuarios_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detalle(request, id):
    try:
        usuario = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        usuarios_serializer = UsuarioSerializer(usuario)
        return JsonResponse(usuarios_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        usuario_data = JSONParser().parse(request)
        try:
            Usuario.objects.filter(pk=id).update(**usuario_data)
            return JsonResponse({'update': usuario_data}, status=status.HTTP_200_OK)
        except Exception as ex: 
            return JsonResponse({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        usuario.delete()
        return JsonResponse({'mensaje': 'usuario eliminada definitivamente!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def publicacion(request):
    if request.method == 'GET':
        try:
            publicaciones = Publicacion.objects.all()
        except Publicacion.DoesNotExist:
            return JsonResponse({'Error': 'No existe ninguna publicacion'}, status=status.HTTP_404_NOT_FOUND)
        publicaciones_serializer = PublicacionSerializer(publicaciones, many = True)
        return JsonResponse(publicaciones_serializer.data, safe=False, status=status.HTTP_200_OK)

    if request.method == 'POST':
        publicacion_data = JSONParser().parse(request)
        publicacion_serializer = PublicacionSerializer(data=publicacion_data)
        if publicacion_serializer.is_valid():
            publicacion_serializer.save()
            return JsonResponse(publicacion_data.data, status=status.HTTP_200_OK)
        return JsonResponse(publicacion_data.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
#Trae el perfil de un usuario
def publicacion_detalle(request, id):
    try:
        usuario = Usuario.objects.get(pk=id)
        publicacion = Publicacion.objects.filter(
            usuario=id
        )
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'El usuario no tiene publicaciones'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        publicaciones = []
        publicacion_serializer = PublicacionSerializer(publicacion, many=True)
        for i in publicacion_serializer.data:
            publicaciones.append(i)
        usuario_serializer = UsuarioSerializer(usuario)
        Dic = {}
        Dic.update(usuario_serializer.data)
        Dic.update({'Publicaciones': publicaciones})
        return JsonResponse(Dic, status=status.HTTP_200_OK)

@api_view(['POST'])
def tendencia(request):
    if request.method == 'POST':
        tendencia_data = JSONParser().parse(request)
        tendencia_serializer = TendenciaSerializer(data=tendencia_data)
        if tendencia_serializer.is_valid():
            tendencia_serializer.save()
            return JsonResponse(tendencia_data.data, status=status.HTTP_200_OK)
        return JsonResponse(tendencia_data.errors, status=status.HTTP_400_BAD_REQUEST)