from django.shortcuts import render
from django.http import HttpResponse

def about(request):
    return render(request, 'monApp/about.html')