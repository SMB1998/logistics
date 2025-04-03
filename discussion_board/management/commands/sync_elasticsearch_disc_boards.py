from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
from discussion_board.models import DiscussionBoard
from discussion_board.documents import DiscussionBoardDocument
from elasticsearch.helpers import bulk
from django.conf import settings
from elasticsearch_dsl.connections import connections

class Command(BaseCommand):
    help = 'Sincroniza los datos de DiscussionBoard con Elasticsearch'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando sincronización con Elasticsearch...')

        # Conectar con Elasticsearch
        es = connections.get_connection()

        # Recrear el índice
        self.stdout.write('Recreando índice de DiscussionBoard...')
        DiscussionBoardDocument._index.delete(ignore=404)
        DiscussionBoardDocument.init()

        # Preparar datos para bulk indexing
        self.stdout.write('Preparando datos para indexación...')
        discussion_boards = DiscussionBoard.objects.all()
        actions = []

        for board in discussion_boards:
            doc = DiscussionBoardDocument()
            doc_dict = doc.prepare(board)
            action = {
                "_index": DiscussionBoardDocument._index._name,
                "_id": board.id,
                "_source": doc_dict
            }
            actions.append(action)

        if actions:
            # Realizar bulk indexing
            self.stdout.write('Realizando indexación masiva...')
            success, failed = bulk(es, actions)
            self.stdout.write(self.style.SUCCESS(f'Sincronización completada. Éxitos: {success}, Fallos: {failed}'))
        else:
            self.stdout.write(self.style.WARNING('No hay discussion boards para indexar'))