from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ArticuloForm
from .models import Articulo
# Create your views here.
def index(request):
    return render(request,"Mi_negocio/index.html")

def greet(request, name:str):
    return render(request, "Mi_negocio/greet.html",{
     "name": name.capitalize()   
    })


def subir_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'mi_app/subir_articulo.html', {'form': form})

def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'mi_app/lista_articulos.html', {'articulos': articulos})