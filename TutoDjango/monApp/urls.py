from django.urls import path
from .views.home import home
from .views.contact import contact
from .views.about import about
from .views.prod import ListProduits
from .views.prod import ListStatut
from .views.prod import ListCategories

urlpatterns = [
    path("home", home, name="home-simple"),
    path("home/<param>", home, name="home"),
    path("contact_us/", contact, name="contact"),
    path("about_us/", about, name="about"),
    path("produit/", ListProduits, name="produit"),
    path("statut/", ListStatut, name="statut"),
    path("categorie/", ListCategories, name="categorie"),
]