from django.urls import path
from .views import ComponentsListCreateView, ComponentsRetrieveUpdateDestroyView

urlpatterns = [
    path('components/', ComponentsListCreateView.as_view(), name='inventario-list-create'),
    path('components/<str:pk>/', ComponentsRetrieveUpdateDestroyView.as_view(), name='inventario-detail'),
]
