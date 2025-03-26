from django.urls import path
from .views import DiscussionBoardRequestListCreateView, DiscussionBoardRequestRetrieveUpdateDestroyView

urlpatterns = [
    path('discussion-board-requests/', DiscussionBoardRequestListCreateView.as_view(), name='discussion-board-requests-list-create'),
    path('discussion-board-requests/<str:pk>/', DiscussionBoardRequestRetrieveUpdateDestroyView.as_view(), name='discussion-board-requests-detail'),
]
