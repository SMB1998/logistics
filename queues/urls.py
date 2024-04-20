from django.urls import path
from .views import QueuesListCreateView, QueuesRetrieveUpdateDestroyView

urlpatterns = [
    path('queues/', QueuesListCreateView.as_view(), name='queues-list-create'),
    path('queues/<str:pk>/', QueuesRetrieveUpdateDestroyView.as_view(), name='queues-detail'),
]
