from django.shortcuts import render
from django.http import HttpResponse
from monApp.models import *



def ListProduits(request):
    prdts = Produit.objects.all()
    return render(request, 'monApp/list_produits.html', {'prdts': prdts})

def ListRayon(request):
    rayon = Rayon.objects.all()
    return render(request, 'monApp/list_rayon.html', {'rayon': rayon})


def ListStatut(request):
    statuts = Statut.objects.all()
    return render(request, 'monApp/list_statut.html', {'statuts': statuts})


def ListCategories(request):
    categories = Categorie.objects.all()
    return render(request, 'monApp/list.cat.html', {'categories': categories})