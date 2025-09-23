from django.urls import path
from .views.home import *

from .views.prod import ListProduits
from .views.prod import ListStatut
from .views.prod import ListCategories
from .views.prod import ListRayon
from django.views.generic import *


urlpatterns = [
    #path("home", home, name="home-simple"),
    path("contact_us/", ContactView.as_view(), name="contact"),
    path("about_us/", AboutView.as_view(), name="about"),
    path("produit/", ListProduits, name="produit"),
    path("statut/", ListStatut, name="statut"),
    path("categorie/", ListCategories, name="categorie"),
    path("rayon/", ListRayon, name="rayon"),
    path("accueil/<param>", accueil, name="accueil"),
    path("home/", HomeView.as_view()),
    path("home/<param>", HomeView.as_view()),
]