from django.db import models

# Create your models here.

class MangaDigital(models.Model):
    nombre = models.CharField(max_length=64)
    tomo = models.IntegerField()
    desc = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.");
    portada = models.ImageField(upload_to='mangas/portadas', default='mangas/portadas/default.png')
    activo = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    path = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    promedio_puntuacion = models.IntegerField(default=0)  # Campo para almacenar el promedio de puntuación
    
    def nombre_manga(self):
        return "{} {}". format(self.nombre, self.tomo)

    def __str__(self):
        return self.nombre_manga()
    
    