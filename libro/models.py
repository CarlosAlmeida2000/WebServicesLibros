from django.db import models

class libro(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)
    ruta_foto = models.ImageField(upload_to="portada_libro", null=True, blank=False)

