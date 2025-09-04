from django.urls import path
from .views.home import home
from .views.contact import contact
from .views.about import about

urlpatterns = [
    path("home", home, name="home-simple"),
    path("home/<param>", home, name="home"),
    path("contact_us/", contact, name="contact"),
    path("about_us/", about, name="about"),
]