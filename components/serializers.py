from rest_framework import serializers
from .models import Components
from providers.models import Providers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providers
        fields = '__all__'  # Incluye todos los campos del modelo Provider

class ComponentsSerializer(serializers.ModelSerializer):
    proveedor = ProviderSerializer()  # Utiliza el serializador del proveedor para serializar la información del proveedor

    class Meta:
        model = Components
        fields = '__all__'
   