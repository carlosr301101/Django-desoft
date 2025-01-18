from django import forms
from .models import Articulo,Tienda


class TiendaForm(forms.ModelForm):
    class Meta:
        model=Tienda
        fields=['nombre','direccion','telefono','correo']

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'descripcion','precio' , 'imagen']