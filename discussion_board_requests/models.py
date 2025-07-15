from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import uuid
from users.models import Users
from discussion_board.models import DiscussionBoard

from django.db.models.signals import pre_save

class DiscussionBoardRequest(models.Model):
    class Meta:
        unique_together = ('discussion_board', 'user')

    def clean(self):
        # Evitar que un usuario tenga más de un request para el mismo board
        if DiscussionBoardRequest.objects.filter(discussion_board=self.discussion_board, user=self.user).exclude(pk=self.pk).exists():
            from django.core.exceptions import ValidationError
            raise ValidationError('Solo puedes tener una solicitud activa por board.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discussion_board = models.ForeignKey(DiscussionBoard, on_delete=models.CASCADE, related_name='discussion_board_requests')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='discussion_board_requests')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"Request for {self.discussion_board.nombre} by {self.user.username}"



# Señal para guardar el estado anterior antes de guardar
@receiver(pre_save, sender=DiscussionBoardRequest)
def set_previous_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            instance._previous_status = old.status
        except sender.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None

# Señal para manejar cambios de estado y procesar componentes/usuarios
@receiver(post_save, sender=DiscussionBoardRequest)
def process_components_on_status_change(sender, instance, created, **kwargs):
    previous_status = getattr(instance, '_previous_status', None)
    # Si el status cambió a 'approved'
    # Crear mensaje automático si se crea o si se aprueba
    if (created or (previous_status != 'approved' and instance.status == 'approved')):
        from discussion_board.models import Message
        # Solo crear el mensaje si no existe ya uno para este request
        if not Message.objects.filter(request=instance).exists():
            componentes = getattr(instance, 'components', []).all()
            if componentes:
                detalles = '\n'.join([
                    f"- {c.component.nombre if hasattr(c.component, 'nombre') else str(c.component)} (referencia: {c.component.referencia if hasattr(c.component, 'referencia') else '-'}) : {c.quantity}" for c in componentes
                ])
                content = f"{instance.user.username} se unió al board y adjuntó los siguientes componentes:\n{detalles}"
            else:
                content = f"{instance.user.username} se unió al board."
            Message.objects.create(
                discussion_board=instance.discussion_board,
                author=instance.user,
                content=content,
                request=instance
            )
        print(f"[DEBUG] Antes de agregar: usuarios en board: {[u.id for u in instance.discussion_board.users.all()]}", flush=True)
        if instance.user not in instance.discussion_board.users.all():
            instance.discussion_board.users.add(instance.user)
            print(f"[DEBUG] Usuario {instance.user.id} agregado al board {instance.discussion_board.id}", flush=True)
        else:
            print(f"[DEBUG] Usuario {instance.user.id} ya estaba en el board {instance.discussion_board.id}", flush=True)
        instance.discussion_board.refresh_from_db()
        print(f"[DEBUG] Después de agregar: usuarios en board: {[u.id for u in instance.discussion_board.users.all()]}", flush=True)
        # Asocia los componentes al tablero
        for comp in getattr(instance, 'components', []).all():
            comp.discussion_board = instance.discussion_board
            comp.save()
    # Si el status cambió de 'approved' a otro (ej: 'rejected')
    elif previous_status == 'approved' and instance.status != 'approved':
        if instance.user in instance.discussion_board.users.all():
            instance.discussion_board.users.remove(instance.user)
            print(f"[DEBUG] Usuario {instance.user.id} eliminado del board {instance.discussion_board.id}", flush=True)
        # Desasociar los componentes de este request del tablero, pero NO borrarlos
        for comp in getattr(instance, 'components', []).all():
            comp.discussion_board = None
            comp.save()
            print(f"[DEBUG] Componente {comp.id} desasociado del board", flush=True)
        # Eliminar mensaje asociado a este request
        from discussion_board.models import Message
        Message.objects.filter(request=instance).delete()

   