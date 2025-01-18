from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
   # path("", views.blank, name="index"),
    
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('subir/', views.subir_articulo, name='subir_articulo'),
    path('articulos/', views.lista_articulos, name='lista_articulos'),
]