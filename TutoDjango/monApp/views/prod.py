from django.shortcuts import render
from django.http import HttpResponse
from monApp.models import *



def ListProduits(request):
    prdts = Produit.objects.all()
    return render(request, 'monApp/list_produits.html', {'prdts': prdts})




def ListStatut(request):
    st = Statut.objects.all()
    table = '<ul>'
    for statut in st:
        table += '<li>'+ statut.nomStatut +'</li>'
    print(table)
    return HttpResponse(table+'</ul>')


def ListCategories(request):
    categories = Categorie.objects.all()
    table = '<ul>'
    for categorie in categories:
        table += '<li>'+ categorie.nomCat +'</li>'
    print(table)
    return HttpResponse(table+'</ul>')