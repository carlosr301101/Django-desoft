from django.db import models

# Create your models here.
class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.CharField(max_length=10)
    imagen = models.ImageField(upload_to='articulos/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo