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
                consolidated[cid] = {
                    "component_id": cid,
                    "component_name": comp.component.nombre if hasattr(comp.component, 'nombre') else str(comp.component),
                    "component": comp_data,
                    "total_quantity": 0,
                    "details": []
                }
            consolidated[cid]["total_quantity"] += comp.quantity
            consolidated[cid]["details"].append({
                "user_id": comp.created_by.id if comp.created_by else None,
                "username": comp.created_by.username if comp.created_by else None,
                "quantity": comp.quantity,
                "request_id": str(comp.request.id) if comp.request else None,
                "type": comp.type
            })
        return Response({
            "discussion_board_id": str(board.id),
            "discussion_board_name": board.nombre,
            "components": list(consolidated.values())
        })
