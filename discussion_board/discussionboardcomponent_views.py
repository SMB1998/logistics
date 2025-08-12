from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DiscussionBoardComponent
from .discussionboardcomponent_serializers import DiscussionBoardComponentSerializer

class DiscussionBoardComponentListView(generics.ListAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = super().get_queryset()
        discussion_board = self.request.query_params.get('discussion_board')
        if discussion_board:
            queryset = queryset.filter(discussion_board=discussion_board)
        return queryset

class DiscussionBoardComponentCreateUpdateView(generics.CreateAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DiscussionBoardComponentUpdateView(generics.UpdateAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class DiscussionBoardComponentRetrieveView(generics.RetrieveAPIView):
    queryset = DiscussionBoardComponent.objects.all()
    serializer_class = DiscussionBoardComponentSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
