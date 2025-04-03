from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Components 

@registry.register_document
class ComponentsDocument(Document):
    proveedor = fields.IntegerField(attr='proveedor.id')  # Indexa el ID del proveedor
    class Index:
        name = 'components'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Components
        fields = [
            'id',
            'url',
            'referencia',
            'precio',
            'nombre',
            'image_url',
            'datasheet_url',
            
            'search_index_provider',
        ]
