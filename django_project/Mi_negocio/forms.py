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

class BusquedaForm(forms.Form):
    termino= forms.CharField(
        label='Buscar',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder' : 'Ej:camisetas'})
        )

class CustomerForm(forms.Form):
    cart_user= forms.CharField(
        label='Su nombre',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder' : 'Manolo'}),
        )