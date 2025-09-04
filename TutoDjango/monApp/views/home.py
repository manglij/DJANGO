from django.shortcuts import render
from django.http import HttpResponse

def home(request, param):
    return HttpResponse(f"<h1>Hello {param}!</h1>")
