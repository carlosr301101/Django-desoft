from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
   # path("", views.blank, name="index"),
    
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('subir/', views.subir_articulo, name='subir_articulo'),
    path('articulos/', views.lista_articulos, name='lista_articulos'),
    
    path('crear_tienda/', views.crear_tienda, name='crear_tienda'),
    path('crear_articulo/<int:tienda_id>/', views.crear_articulo, name='subir_articulo'),
    path('ver_tienda/<int:tienda_id>/', views.ver_tienda, name='ver_tienda'),
]