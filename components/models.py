from django.db import models
from rest_framework import serializers
import uuid 
from providers.models import Providers



    
class Components(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proveedor = models.ForeignKey(Providers, on_delete=models.CASCADE, related_name='components') 
    url = models.URLField(max_length=200)
    referencia = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250)
    datasheet_url = models.CharField(max_length=250)
    
  

    def __str__(self):
        return self.referencia
    