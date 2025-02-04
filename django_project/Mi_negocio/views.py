from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect , get_object_or_404
from .forms import ArticuloForm, TiendaForm, BusquedaForm
from .models import Articulo,Tienda
from django.contrib.auth.decorators import \
login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from io import BytesIO
import json
from django.conf import settings
import os
import requests
from datetime import datetime
from django.utils.text import slugify


# Create your views here.
def index(request):
    return render(request,"Mi_negocio/index.html")

def listar_tiendas(request):
    tiendas = Tienda.objects.all()  
    
    paginator= Paginator(tiendas,10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'Mi_negocio/listar_tiendas.html', {
        'page_obj': page_obj,
        'cantidad':tiendas.count })

""" 
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
 """


# @login_required(login_url='login')
def lista_articulos(request): 
    
    productos = Articulo.objects.select_related('tienda').all().order_by('tienda')

    
    paginator = Paginator(productos, 6)
    page_number = request.GET.get('page')  

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'Mi_negocio/lista_articulos.html', {
        'page_obj': page_obj,
    })


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

    articulos=Articulo.objects.filter(tienda=tienda_id)

    paginator = Paginator(articulos, 6)
    page_number = request.GET.get('page')  

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'Mi_negocio/ver_tienda.html', {
        'tienda': tienda,
        'page_obj': page_obj,
    })

def buscar_articulos(request):
        form = BusquedaForm(request.GET or None)
        resultados_tiendas = []  # Lista de tuplas (tienda, productos)

        if form.is_valid():
            termino = form.cleaned_data['termino']
            
            productos = Articulo.objects.filter(
                Q(titulo__icontains=termino) | Q(descripcion__icontains=termino)
            )
            
            tiendas = Tienda.objects.filter(
                articulos__in=productos
            ).distinct().order_by('nombre')

           
            for tienda in tiendas:
                productos_tienda = productos.filter(tienda=tienda)
                resultados_tiendas.append((tienda, productos_tienda))

    
        paginator = Paginator(resultados_tiendas, 6)
        page_number = request.GET.get('page')  

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        return render(request, 'Mi_negocio/buscar.html', {
        'form': form,
        'page_obj': page_obj,
        'termino_busqueda': request.GET.get('termino', '')  # Para mantener el término en la paginación
    })


def send_pdf_to_whatsapp(tienda,time_format):
    #minegocio.pythonanywhere.com
    nombre=slugify(tienda.nombre)
    pdf_file_path = os.path.join('media', 'facturas',nombre, f'factura_{time_format}.pdf')
    pdf_url = f"http://minegocio.pythonanywhere.com/{pdf_file_path}"

    # Enviar el enlace al WhatsApp del dueño
    #55246437
    url=f"https://wa.me/{tienda.telefono}?text=Aquí%20está%20la%20factura:%20{pdf_url}"
    #url = f"https://api.whatsapp.com/send?phone={tienda.telefono}&text=Aquí%20está%20la%20factura:%20{pdf_url}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Enlace enviado correctamente.")
    else:
        print("Error al enviar el enlace.")
    return url




def generate_pdf(request,tienda_id):
    tienda = Tienda.objects.get(id=tienda_id)
    nombre=slugify(tienda.nombre)
    if request.method == 'POST':
        # Obtener los datos del carrito del formulario
        cart_data = request.POST.get('cart_data')
        if not cart_data:
            return HttpResponse("El carrito está vacío.")

        # Convertir los datos del carrito de JSON a Python
        try:
            cart = json.loads(cart_data)
        except json.JSONDecodeError:
            return HttpResponse("Error al procesar el carrito.")

        # Crear un archivo PDF en memoria
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Encabezado
        p.drawString(100, 800, f"Factura de Compra de la tienda {tienda.nombre}")
        p.drawString(100, 790, "-------------------------------------------------------------------------")
        p.drawString(100, 770, f"Telefono del propietario de la tienda: {tienda.telefono}")
        p.drawString(100, 750, f"Direccion: {tienda.direccion}")
        p.drawString(100, 730, "-------------------------------------------------------------------------")
        # Detalles del carrito
        y = 700
        total = 0
        for item in cart:
            titulo = item.get('titulo', 'Sin título')
            precio = float(item.get('precio', 0))
            quantity = int(item.get('quantity', 1))

            p.drawString(100, y, f"{titulo} - $ {precio} x {quantity}")
            total += precio * quantity
            y -= 20

        # Total
        p.drawString(100, y - 20, f"Total: $ {total:.2f}")
        # Finalizar el PDF
        p.showPage()
        p.save()

         # Guardar el PDF en el servidor
        time=datetime.now()
        time_format=time.strftime("%d_%m_%Y_%H_%M_%S")

        
        path=os.path.join(settings.MEDIA_ROOT, 'facturas', nombre)



        # Verificar si la carpeta existe
        if not os.path.exists(path):
            # Crear la carpeta si no existe
            os.makedirs(path)
                
        
            
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'facturas',nombre, f'factura_{time_format}.pdf')
        with open(pdf_file_path, 'wb') as f:
            f.write(buffer.getvalue())

            # Enviar el PDF al WhatsApp del dueño de la tienda
        

            # Obtener el valor del buffer y devolverlo como respuesta
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{time_format}.pdf"'
        response.write(pdf)
        return redirect(send_pdf_to_whatsapp(tienda,time_format))
        return HttpResponseRedirect(send_pdf_to_whatsapp(tienda,time_format))