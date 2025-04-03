from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import DiscussionBoard

@registry.register_document
class DiscussionBoardDocument(Document):
    users = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        # Agrega otros campos del usuario si es necesario
    })
    components = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'nombre': fields.TextField(),
        # Agrega otros campos del componente si es necesario
    })
    admin = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        # Agrega otros campos del admin si es necesario
    })

    class Index:
        name = 'discussion_boards'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = DiscussionBoard
        fields = [
            'id',
            'referencia',
            'description',
            'created_at',
            'nombre',
            'autoacept',
            'status',
        ] 