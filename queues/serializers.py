from rest_framework import serializers
from .models import Queues


class QueuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queues
        fields = '__all__'  # Incluye todos los campos del modelo Provider

