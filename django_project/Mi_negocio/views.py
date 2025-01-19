from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect , get_object_or_404
from .forms import ArticuloForm, TiendaForm
from .models import Articulo,Tienda
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import \
login_required

# Create your views here.

def index(request):
    return render(request,"Mi_negocio/index.html")

def listar_tiendas(request):
    tiendas = Tienda.objects.all()
    return render(request, 'Mi_negocio/listar_tiendas.html', {'tiendas': tiendas})


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
    tiendas = Tienda.objects.all()
    return render(request, 'Mi_negocio/lista_articulos.html', {'tiendas': tiendas})

@login_required
def eliminar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    
    # Verificar si el usuario es el propietario de la tienda
    if articulo.tienda.propietario == request.user:
        articulo.delete()
    
    return redirect('ver_tienda', tienda_id=articulo.tienda.id)

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

    return render(request, 'Mi_negocio/crear_tienda.html', {'tienda_form': tienda_form})

@login_required
def agregar_articulo(request, tienda_id):
    tienda = Tienda.objects.get(id=tienda_id)
    if tienda.propietario != request.user:
        return redirect('index')

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.tienda = tienda
            articulo.save()
            return redirect('ver_tienda', tienda_id=tienda.id)
    else:
        form = ArticuloForm()

    return render(request, 'Mi_negocio/agregar_articulo.html', {'form': form, 'tienda': tienda})

def ver_tienda(request, tienda_id):
    tienda = Tienda.objects.get(id=tienda_id)
    return render(request, 'Mi_negocio/ver_tienda.html', {'tienda': tienda})
