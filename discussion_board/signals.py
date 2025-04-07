from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DiscussionBoard
from .tasks import sync_discussion_board_elasticsearch

@receiver(post_save, sender=DiscussionBoard)
def discussion_board_post_save(sender, instance, created, **kwargs):
    sync_discussion_board_elasticsearch.delay()

@receiver(post_delete, sender=DiscussionBoard)
def discussion_board_post_delete(sender, instance, **kwargs):
    sync_discussion_board_elasticsearch.delay()