from django.db import models
import uuid 
from users.models import Users
from components.models import Components

class DiscussionBoard(models.Model):
    STATUS_CHOICES = [
        ('created', 'Creado'),
        ('filling_participants', 'Llenando Participantes'),
        ('closed', 'Cerrado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(Users, related_name='discussion_boards_users', blank=True)     
    components = models.ManyToManyField(Components, related_name='discussion_boards_components', blank=True)     
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
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message by {self.author.username} at {self.created_at}"