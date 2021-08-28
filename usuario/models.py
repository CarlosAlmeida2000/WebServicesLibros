from django.db import models

class usuarios(models.Model):
    nombre = models.CharField(max_length=60)
    rol = models.CharField(max_length=2)
    usuario = models.CharField(max_length=15)
    clave = models.CharField(max_length=15)
    
