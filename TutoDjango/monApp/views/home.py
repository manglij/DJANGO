from django.shortcuts import render
from django.http import HttpResponse
from monApp.models import *
from django.views.generic import TemplateView


def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")


class HomeView(TemplateView):
    template_name = "monApp/page_home.html"
    

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Welcome to Django! " + self.kwargs.get('param')
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)  
    

class AboutView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    

    def post(self, request, **kwargs):
        return render(request, self.template_name)
    

class ContactView(TemplateView):
    template_name = "monApp/contact.html"

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['titreh1'] = "Contact us..."
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)  