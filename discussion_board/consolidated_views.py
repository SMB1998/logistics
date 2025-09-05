from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from discussion_board.models import DiscussionBoard, DiscussionBoardComponent
from components.models import Components
from users.models import Users
from collections import defaultdict

class DiscussionBoardConsolidatedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, discussion_board_id):
        from discussion_board.serializers import ComponentsSerializer
        board = get_object_or_404(DiscussionBoard, id=discussion_board_id)
        components = DiscussionBoardComponent.objects.filter(discussion_board=board)
        consolidated = {}
        for comp in components:
            cid = comp.component.id
            if cid not in consolidated:
                comp_data = ComponentsSerializer(comp.component).data
                comp_obj = comp_data.copy()
                comp_obj["component_id"] = cid
                comp_obj["component_name"] = comp.component.nombre if hasattr(comp.component, 'nombre') else str(comp.component)
                comp_obj["quantity"] = 0
                consolidated[cid] = comp_obj
            consolidated[cid]["quantity"] += comp.quantity
        return Response({
            "discussion_board_id": str(board.id),
            "discussion_board_name": board.nombre,
            "components": list(consolidated.values())
        })

class DiscussionBoardUsersConsolidatedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, discussion_board_id):
        from discussion_board.serializers import ComponentsSerializer
        board = get_object_or_404(DiscussionBoard, id=discussion_board_id)
        components = DiscussionBoardComponent.objects.filter(discussion_board=board)
        users_consolidated = defaultdict(lambda: {
            "user_id": None,
            "username": None,
            "components": []
        })
        for comp in components:
            if comp.created_by:
                uid = comp.created_by.id
                users_consolidated[uid]["user_id"] = uid
                users_consolidated[uid]["username"] = comp.created_by.username
                comp_data = ComponentsSerializer(comp.component).data
                comp_obj = comp_data.copy()
                comp_obj["quantity"] = comp.quantity
                comp_obj["type"] = comp.type
                comp_obj["component_id"] = comp.component.id
                comp_obj["component_name"] = comp.component.nombre if hasattr(comp.component, 'nombre') else str(comp.component)
                # Agregar info de la request
                if comp.request:
                    comp_obj["request_id"] = str(comp.request.id)
                    comp_obj["request_name"] = getattr(comp.request, "__str__", lambda: str(comp.request))()
                    comp_obj["request_message"] = comp.request.message if hasattr(comp.request, "message") else ""
                else:
                    comp_obj["request_id"] = None
                    comp_obj["request_name"] = None
                    comp_obj["request_message"] = None
                users_consolidated[uid]["components"].append(comp_obj)
        return Response({
            "discussion_board_id": str(board.id),
            "discussion_board_name": board.nombre,
            "users": list(users_consolidated.values())
        })
