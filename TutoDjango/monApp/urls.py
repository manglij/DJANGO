from django.urls import path
from .views.home import home, accueil
from .views.contact import contact
from .views.about import about
from .views.prod import ListProduits
from .views.prod import ListStatut
from .views.prod import ListCategories
from .views.prod import ListRayon


urlpatterns = [
    path("home", home, name="home-simple"),
    path("home/<param>", home, name="home"),
    path("contact_us/", contact, name="contact"),
    path("about_us/", about, name="about"),
    path("produit/", ListProduits, name="produit"),
    path("statut/", ListStatut, name="statut"),
    path("categorie/", ListCategories, name="categorie"),
    path("rayon/", ListRayon, name="rayon"),
    path("accueil/<param>", accueil, name="accueil"),
]