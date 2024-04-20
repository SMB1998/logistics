from django.db import models
from rest_framework import serializers
import uuid 
from users.models import Users
from components.models import Components

class Queues(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(Users, related_name='queues', blank=True, on_delete=models.CASCADE)     
    components = models.ManyToManyField(Components, related_name='queues', blank=True, on_delete=models.CASCADE)     
    referencia = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    admin = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True) 

    def __str__(self):
    return self.nombre
    