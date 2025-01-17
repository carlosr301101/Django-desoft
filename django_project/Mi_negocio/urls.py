from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path('subir/', views.subir_articulo, name='subir_articulo'),
    path('articulos/', views.lista_articulos, name='lista_articulos'),
]