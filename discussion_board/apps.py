from django.apps import AppConfig



class DiscussionBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'discussion_board'

    def ready(self):
        import discussion_board.signals
