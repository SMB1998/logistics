from django.db import models
from rest_framework import serializers
import uuid 
from providers.models import Providers
import json


    
class Components(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    proveedor = models.ForeignKey(Providers, on_delete=models.CASCADE, related_name='providers') 
    url = models.URLField(max_length=200)
    referencia = models.CharField(max_length=100, blank=True)
    precio = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250, blank=True)
    datasheet_url = models.CharField(max_length=250, blank=True)
    price_breaks = models.CharField(max_length=1000, blank=True)  
    search_index_provider = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo para el nombre del proveedor
    stock_number = models.PositiveIntegerField(default=0)  # Ensure stock_number is always a positive integer
    def __str__(self):
        return f"{self.id} - {self.nombre} - {self.referencia}"

    def save(self, *args, **kwargs):
        if isinstance(self.price_breaks, list):
            # Convert the list to a JSON string before saving
            self.price_breaks = json.dumps(self.price_breaks)
        super().save(*args, **kwargs)

    def get_price_breaks(self):
        try:
            # Convert the JSON string back to a Python object
            return json.loads(self.price_breaks)
        except json.JSONDecodeError:
            return []