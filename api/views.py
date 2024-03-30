from rest_framework import viewsets
from .models import Carrera, Usuario, TiposFormatos, Formato, ServicioSocial
from .serializers import CarreraSerializer, UsuarioSerializer, TiposFormatosSerializer, FormatoSerializer, ServicioSocialSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import DatabaseError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError




@api_view(['POST'])
def login(request):
    # Obtén el tipo de usuario y el nombre de usuario de la solicitud
    tipo_usuario = request.data.get('tipo_usuario')
    username = request.data.get('username')

    if not tipo_usuario or not username:
        return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Busca un usuario con el nombre de usuario y el tipo de usuario dados
        usuario = Usuario.objects.get(username=username, tipo_usuario=tipo_usuario)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except DjangoValidationError:
        return Response({'error': 'Datos de entrada inválidos.'}, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError:
        return Response({'error': 'Problema al acceder a la base de datos.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Verifica la contraseña
    if not usuario.check_password(request.data.get('password')):
        return Response({'error': 'Contraseña inválida.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Crea o obtiene un token para el usuario
        token, created = Token.objects.get_or_create(user=usuario)
    except DatabaseError:
        return Response({'error': 'Problema al crear o recuperar el token del usuario.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Serializa los datos del usuario
    try:
        serializer = UsuarioSerializer(instance=usuario)
    except ValidationError as e:
        return Response({'error': 'Error al serializar los datos del usuario.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Devuelve el token y los datos del usuario serializados
    return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        # Es importante no devolver la contraseña, incluso si está hasheada.
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def profile(request):
    return Response({})


class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class TiposFormatosViewSet(viewsets.ModelViewSet):
    queryset = TiposFormatos.objects.all()
    serializer_class = TiposFormatosSerializer

class FormatoViewSet(viewsets.ModelViewSet):
    queryset = Formato.objects.all()
    serializer_class = FormatoSerializer

class ServicioSocialViewSet(viewsets.ModelViewSet):
    queryset = ServicioSocial.objects.all()
    serializer_class = ServicioSocialSerializer
