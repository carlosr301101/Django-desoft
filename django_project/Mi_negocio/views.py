from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect , get_object_or_404
from .forms import ArticuloForm, TiendaForm, BusquedaForm, CustomerForm
from .models import Articulo,Tienda
from django.contrib.auth.decorators import \
login_required
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
import json
from django.conf import settings
import os
from datetime import datetime
from django.utils.text import slugify
import qrcode
from django.contrib import messages


# Create your views here.
def index(request):
    request.session['cart']='cart'
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

    
    paginator = Paginator(productos, 9)
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
    
    return redirect('ver_tienda', tienda_name=articulo.tienda.nombre)


@login_required
def modificar_articulo(request, articulo_id):
    # Obtener el artículo o devolver un error 404 si no existe
    articulo = get_object_or_404(Articulo, id=articulo_id)
    
    # Verificar que el usuario actual es el propietario de la tienda del artículo
    if articulo.tienda.propietario != request.user:
        return redirect('index')  # Redirige a una página de error si no tiene permisos

    if request.method == 'POST':
        # Si el formulario fue enviado, procesarlo
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()  # Guarda los cambios en la base de datos
            return redirect('ver_tienda', tienda_name=articulo.tienda.nombre)  # Redirige a la vista del artículo modificado
    else:
        # Si es una solicitud GET, mostrar el formulario prellenado
        form = ArticuloForm(instance=articulo)
   
    return render(request, 'Mi_negocio/modificar_articulo.html', {'form': form, 'articulo': articulo})

@login_required
def crear_tienda(request):
    if request.method == 'POST':
        tienda_form = TiendaForm(request.POST)
        if tienda_form.is_valid():
            tienda = tienda_form.save(commit=False)
            tienda.propietario = request.user
            tienda.save()
            
            return redirect('ver_tienda', tienda_name=tienda.nombre)
    else:
        tienda_form = TiendaForm()
    return render(request, 'Mi_negocio/crear_tienda.html', {'tienda_form': tienda_form})

@login_required
def agregar_articulo(request, tienda_name):
    tienda = Tienda.objects.get(nombre=tienda_name)
    if tienda.propietario != request.user:
        return redirect('index')

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.tienda = tienda
            articulo.save()
            return redirect('ver_tienda', tienda_name=tienda.nombre)
    else:
        form = ArticuloForm()

    return render(request, 'Mi_negocio/agregar_articulo.html', {'form': form, 'tienda': tienda})

def ver_tienda(request, tienda_name):
    tienda = Tienda.objects.get(nombre=tienda_name)
    form=CustomerForm(request.GET or None)
    articulos=Articulo.objects.filter(tienda=tienda.id)

    paginator = Paginator(articulos, 10)
    page_number = request.GET.get('page')  
   # 
    print(request.body)

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'Mi_negocio/ver_tienda.html', {
        'form' : form,
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

    
        paginator = Paginator(resultados_tiendas, 9)
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
    #url=f"https://api.whatsapp.com/send?phone={tienda.telefono}?text=Aquí%20está%20la%20factura:%20{pdf_url}"
    url = f"https://wa.me/{tienda.telefono}?text=Hola%20aquí%20está%20la%20factura:{pdf_url}"
    #response = requests.get(url)
    #if response.status_code == 200:
    #    print("Enlace enviado correctamente.")
    #else:
    #    print("Error al enviar el enlace.")

    return url

def generate_qr(request,tienda_id):
    
    # URL de tu tienda
    tienda = Tienda.objects.get(id=tienda_id)
    url_tienda = f"https://minegocio.pythonanywhere.com/Mi_negocio/ver_tienda/{tienda.nombre}"
   # print (request)
  
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url_tienda)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
   # path=os.path.join('Mi_negocio',settings.STATIC_URL, 'Mi_negocio' )
 

    # Guardar la imagen en un buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Devolver la imagen como respuesta HTTP
    response = HttpResponse(content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="tienda_{tienda.nombre}.png"'
    response.write(buffer.getvalue())

    return response


def generate_pdf(request,tienda_id):
    form= CustomerForm(request.POST or None)
    cart_user=request.POST['cart_user']
    print(request.POST)
    if form.is_valid():
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
            p.drawString(100, 700,f"Nombre del beneficiario: {cart_user} ")
            p.drawString(100, 680, "-------------------------------------------------------------------------")
            # Detalles del carrito
            y = 660
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
            #print(response)
            return render(request,'Mi_negocio/generate_pdf.html',{'url_wsp':send_pdf_to_whatsapp(tienda,time_format),'tienda':tienda})
        else:
            return render(request,'Mi_negocio/ver_tienda.html',{'tienda':tienda})