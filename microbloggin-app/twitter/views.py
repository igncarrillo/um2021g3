from collections import defaultdict
import re
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

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
        usuario_data = JSONParser.parse(request, stream=None)
        usuarios_serializer = UsuarioSerializer(data=usuario_data)
        if usuarios_serializer.is_valid():
            usuarios_serializer.save()
            return JsonResponse(usuarios_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(usuarios_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def publicacion(request):
    if request.method == 'POST':
        publicacion_data = JSONParser.parse(request)
        publicacion_serializer = PublicacionSerializer(data=publicacion_data)
        if publicacion_data.is_valid():
            publicacion_data.save()
            return JsonResponse(publicacion_data.data, status=status.HTTP_200_OK)
        return JsonResponse(publicacion_data.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def tendencia(request):
    if request.method == 'POST':
        tendencia_data = JSONParser.parse(request)
        tendencia_serializer = TendenciaSerializer(data=tendencia_data)
        if tendencia_data.is_valid():
            tendencia_data.save()
            return JsonResponse(tendencia_data.data, status=status.HTTP_200_OK)
        return JsonResponse(tendencia_data.errors, status=status.HTTP_400_BAD_REQUEST)