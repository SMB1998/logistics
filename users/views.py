
# En tu_app/views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users, Role
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
           
            user = authenticate(request, username=username, password=password)
         
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({'message': 'Inicio de sesión exitoso', 'access_token': str(refresh.access_token),'user': {
                        'id': user.id,
                        'username': user.username,
                        'role':user.role
                        # Aquí puedes incluir más campos del usuario si lo deseas
                    }}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Nombre de usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Se esperaba una solicitud POST'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['POST'])
def create_user(request):

    # Obtén los datos del formulario
    username = request.data.get('username')
    password = request.data.get('password')
    role_id = request.data.get('role_id')
    
    # Verifica si se proporcionó un nombre de usuario
    if not username:
        return JsonResponse({'error': 'El nombre de usuario es requerido'}, status=400)

    # Si no se proporciona un nombre de rol, utiliza el rol de cliente por defecto
    if not role_id:
        default_role_name = 'cliente'
        try:
            role = Role.objects.get(name=default_role_name)
        except Role.DoesNotExist:
            # Si no existe un rol de cliente en la base de datos, crea uno
            role = Role.objects.create(name=default_role_name)
    else:
        # Verifica si el rol especificado existe en la base de datos
        try:
            role = Role.objects.get(name='cliente')
        except Role.DoesNotExist:
            return JsonResponse({'error': 'El rol especificado no existe'}, status=400)
    
        

    # Encripta la contraseña antes de guardarla
    hashed_password = make_password(password)

    # Crea un nuevo usuario con la contraseña encriptada
    user = Users.objects.create(username=username, password=password, role=role)

    return JsonResponse({'message': 'Usuario creado correctamente'}, status=201)

    return JsonResponse({'error': 'Se esperaba una solicitud POST'}, status=400)
@permission_classes([IsAuthenticated])
@csrf_exempt
def read_user(request, user_id):
    if request.method == 'GET':
        # Lógica para leer los detalles de un usuario
        try:
            user = Users.objects.get(id=user_id)
            data = {
                'id': user.id,
                'username': user.username,
                'role': user.role.name if user.role else None
            }
            return JsonResponse(data)
        except Users.DoesNotExist:
            return JsonResponse({'error': 'El usuario especificado no existe'}, status=404)
        
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        # Lógica para actualizar los detalles de un usuario
        try:
            user = Users.objects.get(id=user_id)
            username = request.POST.get('username')
            password = request.POST.get('password')
            role_id = request.POST.get('role_id')

            if username:
                user.username = username
            if password:
                user.set_password(password)
            if role_id:
                try:
                    role = Role.objects.get(id=role_id)
                    user.role = role
                except Role.DoesNotExist:
                    return JsonResponse({'error': 'El rol especificado no existe'}, status=400)

            user.save()
            return JsonResponse({'message': 'Usuario actualizado correctamente'})
        except Users.DoesNotExist:
            return JsonResponse({'error': 'El usuario especificado no existe'}, status=404)
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        # Lógica para eliminar un usuario
        try:
            user = Users.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'Usuario eliminado correctamente'})
        except Users.DoesNotExist:
            return JsonResponse({'error': 'El usuario especificado no existe'}, status=404)

