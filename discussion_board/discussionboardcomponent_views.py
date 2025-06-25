from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DiscussionBoardComponent
from .discussionboardcomponent_serializers import DiscussionBoardComponentSerializer

class DiscussionBoardComponentListView(generics.ListAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        discussion_board = self.request.query_params.get('discussion_board')
        if discussion_board:
            queryset = queryset.filter(discussion_board=discussion_board)
        return queryset

class DiscussionBoardComponentCreateUpdateView(generics.CreateAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DiscussionBoardComponentUpdateView(generics.UpdateAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer
    lookup_field = 'id'

class DiscussionBoardComponentRetrieveView(generics.RetrieveAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer
    lookup_field = 'id'
