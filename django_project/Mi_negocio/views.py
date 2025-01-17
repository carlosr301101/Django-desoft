from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"Mi_negocio/index.html")

def greet(request, name:str):
    return render(request, "Mi_negocio/greet.html",{
     "name": name.capitalize()   
    })