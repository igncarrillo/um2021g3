from datetime import datetime

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from twitter.models import Usuario, Publicacion, MensajePriv, RelacionSeguidor
from twitter.serializers import UsuarioSerializer, PublicacionSerializer, RelacionSeguidorSerializer, \
    MensajePrivSerializer


# Create your views here.


class LoginController(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        usuario = Usuario.objects.filter(nombre_usuario=data['nombre_usuario']).first()

        if usuario.login(data['contraseña']):
            return JsonResponse({'msg': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'msg': 'Incorrect credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserController(APIView):
    def post(self, request):
        body_request = JSONParser().parse(request)
        usuarios_serializer = UsuarioSerializer(data=body_request)
        if usuarios_serializer.is_valid():
            usuarios_serializer.save()
            return JsonResponse(usuarios_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(usuarios_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioDetalleController(APIView):

    def put(self, request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        usuario_data = JSONParser().parse(request)
        try:
            Usuario.objects.filter(pk=id).update(**usuario_data)
            return JsonResponse({'update': usuario_data}, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class PublicacionController(APIView):

    def post(self, request):
        publicacion_data = JSONParser().parse(request)
        publicacion_serializer = PublicacionSerializer(data=publicacion_data)
        if publicacion_serializer.is_valid():
            publicacion_serializer.save()
            return JsonResponse(publicacion_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(publicacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TablonController(APIView):
    def get(self, request, id):
        try:
            _ = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        seguidos = RelacionSeguidor.objects.filter(seguidores__id=id)

        publicaciones = Publicacion.objects.filter(
            usuario__in=seguidos.values_list('seguido_id', flat=True)) | Publicacion.objects.filter(usuario_id=id)

        serializer = PublicacionSerializer(publicaciones.order_by("fecha"), many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class FollowersController(APIView):
    def get(self, request, id):

        usuario = get_object_or_404(Usuario, id=id)

        if request.method == 'GET':
            usuarios_seguidores = RelacionSeguidor.objects.filter(seguido=usuario)
            if usuarios_seguidores.exists():
                usuarios_seguidores_serialized = RelacionSeguidorSerializer(usuarios_seguidores, many=True)

                seguidores = []
                for i in usuarios_seguidores_serialized.data:
                    seguidores.append(Usuario.objects.get(pk=i["seguidores"]))

                seguidores_serialized = UsuarioSerializer(seguidores, many=True)
                return JsonResponse({"seguidores": seguidores_serialized.data}, status=status.HTTP_200_OK)
            return JsonResponse({'Error': 'No tiene seguidores'}, status=status.HTTP_404_NOT_FOUND)


class FollowerController(APIView):
    def post(self, request, id):

        followed_id = request.data["followed_id"]

        if int(followed_id) == int(id):
            return JsonResponse({'error': 'No puede seguirse a si mismo'}, status=status.HTTP_409_CONFLICT)

        usuario_fd = get_object_or_404(Usuario, id=followed_id)
        usuario_fr = get_object_or_404(Usuario, id=id)

        is_following = usuario_fr.follows(usuario_fd)

        if is_following:
            return JsonResponse({'error': "ya sigue a este usuario"}, status=status.HTTP_409_CONFLICT)

        RelacionSeguidor.objects.create(seguidores=usuario_fr, seguido=usuario_fd)
        return JsonResponse({'mensaje': "usuario seguido"}, status=status.HTTP_200_OK)

    def delete(self, request, id):

        followed_id = request.data["followed_id"]

        if int(followed_id) == int(id):
            return JsonResponse({'error': 'No puede seguirse a si mismo'}, status=status.HTTP_409_CONFLICT)

        usuario_fd = get_object_or_404(Usuario, id=followed_id)
        usuario_fr = get_object_or_404(Usuario, id=id)

        is_following = usuario_fr.follows(usuario_fd)

        if not is_following:
            return JsonResponse({'error': "usted no sigue a este usuario"}, status=status.HTTP_409_CONFLICT)

        RelacionSeguidor.objects.filter(seguidores=usuario_fr, seguido=usuario_fd).delete()
        return JsonResponse({'mensaje': "usuario se ha dejado de seguir"}, status=status.HTTP_200_OK)


class ChatController(APIView):
    def get(self, request, id):
        receptor = get_object_or_404(Usuario, id=id)
        emisor = get_object_or_404(Usuario, id=request.data["user"])
        mensajes = MensajePriv.objects.filter(emisor=emisor, receptor=receptor) | MensajePriv.objects.filter(
            emisor=receptor, receptor=emisor)
        mensajes = mensajes.order_by("fecha")
        mensajes_serialized = MensajePrivSerializer(mensajes, many=True)

        return JsonResponse({"msg": mensajes_serialized.data}, status=status.HTTP_200_OK)

    def post(self, request, id):
        emisor = get_object_or_404(Usuario, id=id)
        receptor = get_object_or_404(Usuario, id=request.data["user"])

        contenido = request.data["contenido"]
        mensaje = MensajePriv.objects.create(
            contenido=contenido,
            receptor=receptor,
            emisor=emisor
        )

        return JsonResponse({"msg": mensaje.contenido, "fecha": str(mensaje.fecha)}, status=status.HTTP_200_OK)


class PublicacionDetalleController(APIView):
    def get(self, request, id):
        try:
            publicacion = Publicacion.objects.get(pk=id)
        except Publicacion.DoesNotExist:
            return JsonResponse({'Error': 'No existe ninguna publicacion'}, status=status.HTTP_404_NOT_FOUND)

        publicacion_serializer = PublicacionSerializer(publicacion)
        return JsonResponse(publicacion_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            publicacion = Publicacion.objects.get(pk=id)
        except Publicacion.DoesNotExist:
            return JsonResponse({'Error': 'No existe ninguna publicacion'}, status=status.HTTP_404_NOT_FOUND)

        publicacion_data = request.data
        publicacion.contenido = publicacion_data.get('contenido', publicacion.contenido)
        publicacion.etiqueta = publicacion_data.get('etiqueta', publicacion.etiqueta)
        publicacion.is_edited = True
        publicacion.fecha = datetime.now().date()
        publicacion.save()
        publicacion_serializer = PublicacionSerializer(publicacion)
        return JsonResponse(publicacion_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            publicacion = Publicacion.objects.get(pk=id)
        except Publicacion.DoesNotExist:
            return JsonResponse({'Error': 'No existe ninguna publicacion'}, status=status.HTTP_404_NOT_FOUND)

        publicacion.delete()
        return JsonResponse({'message': 'Publicacion eliminada exitosamente.'}, status=status.HTTP_200_OK)
