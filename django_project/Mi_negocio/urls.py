from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path('subir/', views.subir_articulo, name='subir_articulo'),
    path('articulos/', views.lista_articulos, name='lista_articulos'),
]