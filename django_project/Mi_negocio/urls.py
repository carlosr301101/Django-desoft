from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
   # path("", views.blank, name="index"),
    
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
   # path('subir/', views.subir_articulo, name='subir_articulo'),
    path('articulos/', views.lista_articulos, name='lista_articulos'),
    path('generate-pdf/<int:tienda_id>/', views.generate_pdf, name='generate_pdf'),
    path('buscar/', views.buscar_articulos, name='buscar_articulo'),
    path('listar_tiendas/', views.listar_tiendas, name='listar_tiendas'),
    path('crear_tienda/', views.crear_tienda, name='crear_tienda'),
    path('ver_tienda/<int:tienda_id>/', views.ver_tienda, name='ver_tienda'),
    path('ver_tienda/<int:tienda_id>/agregar_articulo/', views.agregar_articulo, name='agregar_articulo'),
    path('ver_tienda/eliminar/<int:articulo_id>/', views.eliminar_articulo, name='eliminar_articulo'),
]