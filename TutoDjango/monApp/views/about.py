from django.shortcuts import render
from django.http import HttpResponse

def about(request):
    return HttpResponse("<h1>À propos de nous</h1><p>Nous sommes une entreprise dédiée à fournir les meilleurs services.</p>")
