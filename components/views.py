from rest_framework import generics
from .models import Components
from .serializers import ComponentsSerializer, ComponentDocumentSerializer
from elasticsearch_dsl.query import MultiMatch, Bool, Term
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.pagination import LimitOffsetPagination
from .documents import ComponentsDocument

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35

@permission_classes([IsAuthenticated])
class ComponentsListCreateView(generics.ListCreateAPIView):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
    pagination_class = CustomLimitOffsetPagination

@permission_classes([IsAuthenticated])
class ComponentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer



class ComponentSearchView(generics.ListAPIView):
    serializer_class = ComponentDocumentSerializer
    pagination_class = CustomLimitOffsetPagination  # Usar la paginación personalizada

    def get_queryset(self):
        bool_query = Bool()

        q = self.request.query_params.get("q", None)
        proveedor_id = self.request.query_params.get("provider_id", None)

        print(f"🔍 Buscando: {q}, Proveedor: {proveedor_id}", flush=True)

        # Manejo de búsqueda de texto
        if q:
            query = MultiMatch(query=q, fields=["nombre", "referencia", "search_index_provider"], fuzziness="AUTO")
            bool_query.must.append(query)

        # Filtro de proveedor si es válido
        if proveedor_id:
            proveedor_query = Term(proveedor={"value": proveedor_id})
            bool_query.filter.append(proveedor_query)

        # Si hay filtros, aplicar la consulta; si no, traer todo con match_all
        if bool_query.must or bool_query.filter:
            # Aquí se aplica la paginación
            queryset = ComponentsDocument.search().query(bool_query)
        else:
            queryset = ComponentsDocument.search().query("match_all")

        # Aplicar la paginación a los resultados
        return self.paginate_queryset(queryset)