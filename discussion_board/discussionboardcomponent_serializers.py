from rest_framework import serializers
from .models import DiscussionBoardComponent
from components.models import Components

class DiscussionBoardComponentSerializer(serializers.ModelSerializer):
    component = serializers.PrimaryKeyRelatedField(queryset=Components.objects.all())
    class Meta:
        model = DiscussionBoardComponent
        fields = ['id', 'discussion_board', 'component', 'quantity', 'type', 'created_by', 'request']
        read_only_fields = ['id']
