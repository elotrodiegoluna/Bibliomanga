from django.db import models

# Create your models here.
class Manga(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    precio = models.IntegerField(default=10000)
    stock = models.IntegerField(null=True)
    digital = models.BooleanField(default=False)
    portada = models.TextField(null=True) #URL a la imagen
    premium = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre