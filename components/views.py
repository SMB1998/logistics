from rest_framework import generics
from .models import Components
from .serializers import ComponentsSerializer, ComponentDocumentSerializer
from elasticsearch_dsl.query import MultiMatch

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas

@permission_classes([IsAuthenticated])
class ComponentsListCreateView(generics.ListCreateAPIView):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
    pagination_class = CustomLimitOffsetPagination  # Agrega paginación

@permission_classes([IsAuthenticated])
class ComponentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
    


from .documents import ComponentDocument

from .models import Components

class ComponentSearchView(generics.ListAPIView):
    serializer_class = ComponentDocumentSerializer
    
    queryset = ComponentDocument.search().query('match_all')  # Consulta inicial, puede ser modificada según la búsqueda requerida
   
    # search_fields = ('nombre')  # Campos de búsqueda

    def get_queryset(self):
        # Ajustar la consulta según los parámetros de búsqueda proporcionados en la solicitud
        queryset = self.queryset

        # Ejemplo: filtrar por un término de búsqueda específico
        q = self.request.query_params.get('q', None)
        if q:
            query = MultiMatch(query=q, fields=[ "*"], fuzziness="AUTO")
            queryset = ComponentDocument.search().query(query)[0:30]

        return queryset
