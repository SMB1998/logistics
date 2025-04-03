from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
from components.models import Components
from components.documents import ComponentsDocument
from elasticsearch.helpers import bulk
from django.conf import settings
from elasticsearch_dsl.connections import connections

class Command(BaseCommand):
    help = 'Sincroniza los datos con Elasticsearch'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando sincronización con Elasticsearch...')
        
        # Conectar con Elasticsearch
        es = connections.get_connection()
        
        # Recrear el índice
        self.stdout.write('Recreando índice de Components...')
        ComponentsDocument._index.delete(ignore=404)
        ComponentsDocument.init()
        
        # Preparar datos para bulk indexing
        self.stdout.write('Preparando datos para indexación...')
        components = Components.objects.all()
        actions = []
        
        for component in components:
            doc = ComponentsDocument()
            doc_dict = doc.prepare(component)
            action = {
                "_index": ComponentsDocument._index._name,
                "_id": component.id,
                "_source": doc_dict
            }
            actions.append(action)
        
        if actions:
            # Realizar bulk indexing
            self.stdout.write('Realizando indexación masiva...')
            success, failed = bulk(es, actions)
            self.stdout.write(self.style.SUCCESS(f'Sincronización completada. Éxitos: {success}, Fallos: {failed}'))
        else:
            self.stdout.write(self.style.WARNING('No hay componentes para indexar')) 