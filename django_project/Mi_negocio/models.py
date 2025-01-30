from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings

# Create your models here.
class Tienda(models.Model):
   # id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    nombre=models.CharField(max_length=64)
    direccion=models.TextField(max_length=200)
    telefono=models.CharField(max_length=12)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    correo=models.EmailField()

    def __str__(self):
        return self.nombre



class Articulo(models.Model):
  #  id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE,related_name='articulos')

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='articulos/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        # Borra la imagen del sistema de archivos
        if self.imagen:
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, self.imagen.name)
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
        
        # Llama al método delete() de la clase padre para borrar el artículo
        super().delete(*args, **kwargs)

