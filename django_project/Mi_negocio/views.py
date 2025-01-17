from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ArticuloForm
from .models import Articulo
# Create your views here.

def blank (request):
    return HttpResponseRedirect('subir')


def index(request):
    return render(request,"Mi_negocio/index.html")

def subir_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'Mi_negocio/subir_articulo.html', {'form': form})

def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'Mi_negocio/lista_articulos.html', {'articulos': articulos})

def borrar(request,id_borrar:int):
    articulos=Articulo.objects.all()
    articulos[id_borrar].delete()
    return render(request, 'Mi_negocio/lista_articulos.html', {'articulos': articulos})