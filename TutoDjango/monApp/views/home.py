from django.shortcuts import render
from django.http import HttpResponse
from monApp.models import *

def home(request, param="Django"):
    return HttpResponse(f"<h1>Hello {param}!</h1>")

def ListProduits(request):
    prdts = Produit.objects.all()
    table = '<ul>'
    for produit in prdts:
        table += '<li>'+ produit.intituleProd +'</li>'

    print(table)
    return HttpResponse(table+'</ul>')
