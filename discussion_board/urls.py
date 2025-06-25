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
from .discussionboardcomponent_views import DiscussionBoardComponentListView, DiscussionBoardComponentCreateUpdateView, DiscussionBoardComponentUpdateView, DiscussionBoardComponentRetrieveView
from .ia_local_views import LocalIAInteractView, IAResultView

urlpatterns = [
    path('discussion-boards/', DiscussionBoardListCreateView.as_view(), name='discussion-boards-list-create'),
    path('discussion-boards/<str:pk>/', DiscussionBoardRetrieveUpdateDestroyView.as_view(), name='discussion-boards-detail'),
    path('user-discussion-boards/<str:user_id>/', UserDiscussionBoardsView.as_view(), name='user-discussion-boards'),
    
    # Endpoints para mensajes
    path('discussion-boards/<str:discussion_board_id>/messages/', MessageListCreateView.as_view(), name='messages-list-create'),
    path('discussion-boards/<str:discussion_board_id>/messages/<str:id>/', MessageDetailView.as_view(), name='message-detail'),
    path('discussion-boards/<str:discussion_board_id>/messages/<str:parent_id>/replies/', MessageReplyView.as_view(), name='message-replies'),
    path('discussion-board/search/', DiscussionBoardSearchView.as_view(), name='discussion-board-search'),

    # Endpoints para DiscussionBoardComponent
    path('discussion-board-components/', DiscussionBoardComponentListView.as_view(), name='discussion-board-component-list'),
    path('discussion-board-components/create/', DiscussionBoardComponentCreateUpdateView.as_view(), name='discussion-board-component-create'),
    path('discussion-board-components/<int:id>/', DiscussionBoardComponentRetrieveView.as_view(), name='discussion-board-component-detail'),
    path('discussion-board-components/<int:id>/update/', DiscussionBoardComponentUpdateView.as_view(), name='discussion-board-component-update'),

    # Endpoint de IA local
    path('ia-local/', LocalIAInteractView.as_view(), name='ia-local'),
    path('ia-local-result/<str:task_id>/', IAResultView.as_view(), name='ia-local-result'),
]
