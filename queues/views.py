from rest_framework import generics
from .models import Queues
from .serializers import QueuesSerializer


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas

@permission_classes([IsAuthenticated])
class QueuesListCreateView(generics.ListCreateAPIView):
    queryset = Queues.objects.all()
    serializer_class = QueuesSerializer
    pagination_class = CustomLimitOffsetPagination  # Agrega paginación

@permission_classes([IsAuthenticated])
class QueuesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Queues.objects.all()
    serializer_class = QueuesSerializer