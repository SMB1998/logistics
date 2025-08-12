from django.db import models
import uuid 
from users.models import Users
from components.models import Components

class DiscussionBoardComponent(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Si este componente está asociado a un request, actualizar el mensaje automático
        if self.request:
            from discussion_board.models import Message
            msg = Message.objects.filter(request=self.request).first()
            if msg:
                componentes = self.request.components.all()
                if componentes:
                    detalles = '\n'.join([
                        f"- {c.component.nombre if hasattr(c.component, 'nombre') else str(c.component)} (referencia: {c.component.referencia if hasattr(c.component, 'referencia') else '-'}) : {c.quantity}" for c in componentes
                    ])
                    msg.content = f"{self.request.user.username} se unió al board y adjuntó los siguientes componentes:\n{detalles}"
                else:
                    msg.content = f"{self.request.user.username} se unió al board."
                msg.save()
    discussion_board = models.ForeignKey('DiscussionBoard', on_delete=models.CASCADE, null=True, blank=True)
    component = models.ForeignKey('components.Components', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=20, choices=[('initial', 'Inicial'), ('request', 'Request')], default='initial')
    created_by = models.ForeignKey('users.Users', on_delete=models.CASCADE, null=True, blank=True)
    request = models.ForeignKey('discussion_board_requests.DiscussionBoardRequest', on_delete=models.SET_NULL, null=True, blank=True, related_name='components')

    class Meta:
        unique_together = ('discussion_board', 'component', 'created_by', 'type')

    def __str__(self):
        return f"{self.discussion_board} - {self.component} (Cantidad: {self.quantity}, Tipo: {self.type}, Usuario: {self.created_by})"

class DiscussionBoard(models.Model):
    def save(self, *args, **kwargs):
        status_before = None
        # Solo buscar el objeto viejo si ya existe en la base de datos
        if self.pk and DiscussionBoard.objects.filter(pk=self.pk).exists():
            old = DiscussionBoard.objects.get(pk=self.pk)
            status_before = old.status
        super().save(*args, **kwargs)
        # Si el status cambió a 'closed', enviar correos por Celery
        if status_before != 'closed' and self.status == 'closed':
            from discussion_board.tasks import send_board_closed_email
            send_board_closed_email.delay(self.id)
    STATUS_CHOICES = [
        ('created', 'Creado'),
        ('filling_participants', 'Llenando Participantes'),
        ('closed', 'Cerrado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(Users, related_name='discussion_boards_users', blank=True)     
    components = models.ManyToManyField(Components, through='DiscussionBoardComponent', related_name='discussion_boards_components', blank=True)     
    referencia = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    nombre = models.CharField(max_length=100)
    admin = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='admin_discussion_boards', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    autoacept = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    def __str__(self):
        return self.nombre

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discussion_board = models.ForeignKey(DiscussionBoard, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='messages')
    request = models.ForeignKey('discussion_board_requests.DiscussionBoardRequest', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message by {self.author.username} at {self.created_at}"