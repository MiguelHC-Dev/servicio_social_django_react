from rest_framework import serializers
from .models import Carrera, Usuario, TiposFormatos, Formato, ServicioSocial


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'tipo_usuario', 'carrera', 'servicio', 'residencia', 'ingles', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class TiposFormatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposFormatos
        fields = '__all__'


class FormatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formato
        fields = '__all__'


class ServicioSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioSocial
        fields = '__all__'
