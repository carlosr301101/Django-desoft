from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ArticuloForm, TiendaForm
from .models import Articulo,Tienda
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import \
login_required

# Create your views here.

def index(request):
    return render(request,"Mi_negocio/index.html")

@login_required(login_url='login')
def subir_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'Mi_negocio/subir_articulo.html', {'form': form})

#@login_required(login_url='login')
def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'Mi_negocio/lista_articulos.html', {'articulos': articulos})

def borrar(request,id_borrar:int):
    articulos=Articulo.objects.all()
    articulos[id_borrar].delete()
    return render(request, 'Mi_negocio/lista_articulos.html', {'articulos': articulos})

@login_required
def crear_tienda(request):
    if request.method == 'POST':
        tienda_form = TiendaForm(request.POST)
        if tienda_form.is_valid():
            tienda = tienda_form.save(commit=False)
            tienda.propietario = request.user
            tienda.save()
            return redirect('ver_tienda', tienda_id=tienda.id)
    else:
        tienda_form = TiendaForm()

    return render(request, 'crear_tienda.html', {'tienda_form': tienda_form})

@login_required
def crear_articulo(request, tienda_id):
    tienda = Tienda.objects.get(id=tienda_id, propietario=request.user)
    
    if request.method == 'POST':
        articulo_form = ArticuloForm(request.POST)
        if articulo_form.is_valid():
            articulo = articulo_form.save(commit=False)
            articulo.tienda = tienda
            articulo.save()
            return redirect('ver_tienda', tienda_id=tienda.id)
    else:
        articulo_form = ArticuloForm()

    return render(request, 'subir_articulo.html', {'articulo_form': articulo_form, 'tienda': tienda})

def ver_tienda(request, tienda_id):
    tienda = Tienda.objects.get(id=tienda_id)
    return render(request, 'ver_tienda.html', {'tienda': tienda})
