from celery import shared_task
from django.core.management import call_command

@shared_task
def sync_discussion_board_elasticsearch():
    call_command('sync_elasticsearch_disc_boards') 