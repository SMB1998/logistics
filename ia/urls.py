from django.urls import path
from .views import LocalIAInteractView, IAResultView

urlpatterns = [
    path('ia-local/', LocalIAInteractView.as_view(), name='ia-local'),
    path('ia-local-result/<str:task_id>/', IAResultView.as_view(), name='ia-local-result'),
]
