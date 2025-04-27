from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Components 

@registry.register_document
class ComponentsDocument(Document):
    proveedor = fields.IntegerField(attr='proveedor.id')  # Indexa el ID del proveedor
    price_breaks = fields.TextField()  # Add price_breaks as a searchable field
    stock_number = fields.IntegerField()

    def prepare_price_breaks(self, instance):
        # Convierte el JSON almacenado en la base de datos a una cadena legible
        return instance.price_breaks if instance.price_breaks else None

    def prepare_stock_number(self, instance):
        # Ensure stock_number is indexed as an integer
        return instance.stock_number

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
