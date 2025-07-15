from rest_framework import serializers
from .models import DiscussionBoardRequest
from discussion_board.models import DiscussionBoardComponent
from users.models import Users
from components.models import Components
from discussion_board.discussionboardcomponent_serializers import DiscussionBoardComponentSerializer

# Serializador para el modelo Users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['password'] 


class DiscussionBoardRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    components = DiscussionBoardComponentSerializer(many=True, required=False)

    class Meta:
        model = DiscussionBoardRequest
        fields = '__all__'