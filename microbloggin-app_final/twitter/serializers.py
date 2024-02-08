from rest_framework import serializers

from twitter.models import Usuario, Publicacion, Tendencias, MensajePriv, RelacionSeguidor


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


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


class RelacionSeguidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelacionSeguidor
        fields = '__all__'


class MensajePrivSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajePriv
        fields = '__all__'
