from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q
from .models import DiscussionBoard, Message
from .serializers import DiscussionBoardSerializer, MessageSerializer, DiscussionBoardDocumentSerializer
from elasticsearch_dsl.query import MultiMatch, Bool

from .documents import DiscussionBoardDocument
from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas

from rest_framework.permissions import AllowAny, IsAuthenticated

class DiscussionBoardListCreateView(generics.ListCreateAPIView):
    queryset = DiscussionBoard.objects.all()
    serializer_class = DiscussionBoardSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Permitir acceso sin autenticación para listar
            return [AllowAny()]
        elif self.request.method == 'POST':
            # Requerir autenticación para crear
            return [IsAuthenticated()]
        return super().get_permissions()

class DiscussionBoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscussionBoard.objects.all()
    serializer_class = DiscussionBoardSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            # Permitir acceso sin autenticación para listar
            return [AllowAny()]
        else:
            # Requerir autenticación para crear
            return [IsAuthenticated()]

    
class UserDiscussionBoardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user, flush=True)
        
        # Obtener las colas asociadas al usuario autenticado
        discussion_boards = DiscussionBoard.objects.filter(Q(users=user) | Q(admin=user)).distinct()
        serializer = DiscussionBoardSerializer(discussion_boards, many=True, context={'request': request})
        return Response(serializer.data)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        discussion_board_id = self.kwargs.get('discussion_board_id')
        return Message.objects.filter(discussion_board_id=discussion_board_id, parent=None)

    def perform_create(self, serializer):
        discussion_board_id = self.kwargs.get('discussion_board_id')
        discussion_board = DiscussionBoard.objects.get(id=discussion_board_id)
        serializer.save(
            discussion_board=discussion_board,
            author=self.request.user
        )

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        discussion_board_id = self.kwargs.get('discussion_board_id')
        return Message.objects.filter(discussion_board_id=discussion_board_id)

    def perform_update(self, serializer):
        serializer.save(is_edited=True)

class MessageReplyView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        discussion_board_id = self.kwargs.get('discussion_board_id')
        parent_id = self.kwargs.get('parent_id')
        return Message.objects.filter(
            discussion_board_id=discussion_board_id,
            id=parent_id
        )

    def perform_create(self, serializer):
        discussion_board_id = self.kwargs.get('discussion_board_id')
        parent_id = self.kwargs.get('parent_id')
        discussion_board = DiscussionBoard.objects.get(id=discussion_board_id)
        parent_message = Message.objects.get(id=parent_id)
        
        serializer.save(
            discussion_board=discussion_board,
            parent=parent_message,
            author=self.request.user
        )

class DiscussionBoardSearchView(generics.ListAPIView):
    serializer_class = DiscussionBoardDocumentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        bool_query = Bool()

        q = self.request.query_params.get("q", None)

        if q:
            query = MultiMatch(query=q, fields=["nombre", "referencia", "status"], fuzziness="AUTO")
            bool_query.must.append(query)

        if bool_query.must:
            queryset = DiscussionBoardDocument.search().query(bool_query)
        else:
            queryset = DiscussionBoardDocument.search().query("match_all")

        return self.paginate_queryset(queryset)