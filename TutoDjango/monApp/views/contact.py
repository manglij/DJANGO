from django.shortcuts import render
from django.http import HttpResponse

def contact(request):
    return HttpResponse("<h1>nous contacter</h1><p>Envoyez-nous un email à</p>")
