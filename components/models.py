from django.db import models
from rest_framework import serializers
import uuid 
from providers.models import Providers



    
class Components(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    proveedor = models.ForeignKey(Providers, on_delete=models.CASCADE, related_name='providers') 
    url = models.URLField(max_length=200)
    referencia = models.CharField(max_length=100, blank=True)
    precio = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250, blank=True)
    datasheet_url = models.CharField(max_length=250, blank=True)
    
  

    def __str__(self):
         return f"{self.id} - {self.nombre} - {self.referencia}"
    