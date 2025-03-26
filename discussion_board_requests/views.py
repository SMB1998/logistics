from rest_framework import generics
from .models import DiscussionBoardRequest
from .serializers import DiscussionBoardRequestSerializer


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas

@permission_classes([IsAuthenticated])
class DiscussionBoardRequestListCreateView(generics.ListCreateAPIView):
    queryset = DiscussionBoardRequest.objects.all()
    serializer_class = DiscussionBoardRequestSerializer
    pagination_class = CustomLimitOffsetPagination  # Agrega paginación

@permission_classes([IsAuthenticated])
class DiscussionBoardRequestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscussionBoardRequest.objects.all()
    serializer_class = DiscussionBoardRequestSerializer