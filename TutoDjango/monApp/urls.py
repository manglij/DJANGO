from django.urls import path
from .views import *


from django.views.generic import *


urlpatterns = [
    #path("home", home, name="home-simple"),
    path("contact_us/", ContactView, name="contact"),
    path("about_us/", AboutView.as_view(), name="about"),
    path("produits/", ProduitListView.as_view(), name="produit"),
    path("produits/<pk>/",ProduitDetailView.as_view(), name="dtl_prdt"),
    path("statuts/", StatutListView.as_view(), name="statuts"),
    path("statuts/<pk>/", StatutDetailView.as_view(), name="dtl_statut"),
    path("categories/", CategorieListView.as_view(), name="categories"),
    path("categories/<pk>/", CategorieDetailView.as_view(), name="dtl_cat"),
    path("rayons/", RayonListView.as_view(), name="rayons"),
    path("rayons/<pk>/", RayonDetailView.as_view(), name="dtl_rayons"),
    path("accueil/<param>", accueil, name="accueil"),
    path("home/", HomeView.as_view(), name="home"),
    path("home/<param>", HomeView.as_view()),
    path('login/', ConnectView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', DisconnectView.as_view(), name='logout'),
    path('envoi/', EmailSentView.as_view(), name='email-sent'),
    path("produit/",ProduitCreateView.as_view() , name="crt-prdt"),

]