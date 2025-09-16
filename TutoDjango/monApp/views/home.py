from django.shortcuts import render
from django.http import HttpResponse
from monApp.models import *

def home(request, param="Django"):
    string = request.GET['name']
    return HttpResponse(f"<h1>Hello {string}!</h1>")


def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")