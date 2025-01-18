from django.db import models

# Create your models here.
class Tienda(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    nombre=models.CharField(max_length=64)
    direccion=models.TextField(max_length=200)
    telefono=models.CharField(max_length=12)
    correo=models.EmailField()

    def __str__(self):
        return self.nombre
    
    articulos=[]


class Articulo(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.CharField(max_length=10)
    imagen = models.ImageField(upload_to='articulos/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

