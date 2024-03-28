from rest_framework import generics
from .models import Providers
from .serializers import ProvidersSerializer



class ProvidersListCreateView(generics.ListCreateAPIView):
    queryset = Providers.objects.all()
    serializer_class = ProvidersSerializer


class ProvidersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Providers.objects.all()
    serializer_class = ProvidersSerializer