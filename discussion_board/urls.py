from django.urls import path
from .views import (
    DiscussionBoardListCreateView,
    DiscussionBoardRetrieveUpdateDestroyView,
    UserDiscussionBoardsView,
    MessageListCreateView,
    MessageDetailView,
    MessageReplyView,
    DiscussionBoardSearchView
)

urlpatterns = [
    path('discussion-boards/', DiscussionBoardListCreateView.as_view(), name='discussion-boards-list-create'),
    path('discussion-boards/<str:pk>/', DiscussionBoardRetrieveUpdateDestroyView.as_view(), name='discussion-boards-detail'),
    path('my-discussion-boards/', UserDiscussionBoardsView.as_view(), name='user-discussion-boards'),
    
    # Endpoints para mensajes
    path('discussion-boards/<str:discussion_board_id>/messages/', MessageListCreateView.as_view(), name='messages-list-create'),
    path('discussion-boards/<str:discussion_board_id>/messages/<str:id>/', MessageDetailView.as_view(), name='message-detail'),
    path('discussion-boards/<str:discussion_board_id>/messages/<str:parent_id>/replies/', MessageReplyView.as_view(), name='message-replies'),
    path('discussion-board/search/', DiscussionBoardSearchView.as_view(), name='discussion-board-search'),
]
