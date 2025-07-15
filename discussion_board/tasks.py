from celery import shared_task
from django.core.management import call_command
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def sync_discussion_board_elasticsearch():
    call_command('sync_elasticsearch_disc_boards')

def build_board_email(board):
    subject = f"El tablero '{board.nombre}' ha sido cerrado"
    body = f"El tablero '{board.nombre}' ha sido cerrado.\n\nReferencia: {board.referencia}\nDescripción: {board.description}\nParticipantes: {', '.join([u.username for u in board.users.all()])}\n\nComponentes:\n"
    for comp in board.components.all():
        body += f"- {comp.nombre} (referencia: {comp.referencia})\n"
    body += f"\nEstado final: CERRADO"
    emails = [u.email for u in board.users.all() if u.email]
    return subject, body, emails

@shared_task
def send_board_closed_email(board_id):
    from discussion_board.models import DiscussionBoard
    board = DiscussionBoard.objects.get(pk=board_id)
    subject, body, emails = build_board_email(board)
    if emails:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=True
        )