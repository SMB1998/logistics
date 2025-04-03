from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DiscussionBoard
from .tasks import sync_discussion_board_elasticsearch

@receiver(post_save, sender=DiscussionBoard)
def discussion_board_post_save(sender, instance, created, **kwargs):
    sync_discussion_board_elasticsearch.delay() 