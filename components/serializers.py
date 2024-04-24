from rest_framework import serializers
from .models import Components
from providers.models import Providers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providers
        fields = '__all__'  

class ComponentsSerializer(serializers.ModelSerializer):
    proveedor = ProviderSerializer()  

    class Meta:
        model = Components
        fields = '__all__'
   