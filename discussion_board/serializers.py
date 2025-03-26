from rest_framework import serializers
from .models import DiscussionBoard, Message
from users.models import Users
from components.models import Components
from users.serializers import UsersSerializer

# Serializador para el modelo Users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['password']  # Excluir el campo de contraseña


# Serializador para el modelo Components
class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = '__all__'

# Serializador para el modelo DiscussionBoard
class DiscussionBoardSerializer(serializers.ModelSerializer):
    users = UsersSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = DiscussionBoard
        fields = '__all__'

    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data

# Serializador para el modelo Queues
class QueuesSerializer(serializers.ModelSerializer):
    admin = UsersSerializer()  # Incluir el serializador de Users para el campo admin
    users = UsersSerializer(many=True)  # Incluir el serializador de Users para el campo users
    components = ComponentsSerializer(many=True)  # Incluir el serializador de Components para el campo components
    is_admin = serializers.SerializerMethodField()  # Campo personalizado is_admin

    class Meta:
        model = DiscussionBoard
        fields = '__all__'

    def get_is_admin(self, obj):
        # Obtener el usuario que realiza la solicitud
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Comprobar si el usuario autenticado es el administrador de la cola
            print(obj, flush=True)
            b=obj.admin.id
            a=request.user.id
            _request = request 
            return obj.admin.id == request.user.id
        return False

class MessageSerializer(serializers.ModelSerializer):
    author = UsersSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'discussion_board', 'author', 'content', 'parent', 'created_at', 'updated_at', 'is_edited', 'replies']
        read_only_fields = ['created_at', 'updated_at', 'is_edited']

    def get_replies(self, obj):
        replies = obj.replies.all()
        return MessageSerializer(replies, many=True).data