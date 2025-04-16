from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = Users.objects.get(email='santiagomunoz318@gmail.com')

        print(password, flush=True)

        # Verificar si el usuario existe y las credenciales son válidas
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Credenciales inválidasaa')

        if not user.is_active:
            raise serializers.ValidationError('La cuenta de usuario está desactivada')

        return data