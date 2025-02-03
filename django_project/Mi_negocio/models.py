from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.utils.text import slugify
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

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

def upload_to_articulos(instance, filename):
    # Genera la ruta: articulos/nombre_de_la_tienda/filename
    nombre_tienda = slugify(instance.tienda.nombre)
    return os.path.join('articulos', f"{nombre_tienda}_{str(instance.tienda.id)}", filename)


class Articulo(models.Model):
  #  id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE,related_name='articulos')

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to=upload_to_articulos)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    


    def compress_image(self, image):
        """
        Comprime la imagen utilizando Pillow.
        """
        img = Image.open(image)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        output = BytesIO()

        
        img.save(output, format='JPEG', quality=60)  
        output.seek(0)

        return ContentFile(output.read(), name=image.name)
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save() para comprimir la imagen antes de guardarla.
        """
        if self.imagen:
            self.imagen = self.compress_image(self.imagen)

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.imagen:
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, self.imagen.name)
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)

        super().delete(*args, **kwargs)

