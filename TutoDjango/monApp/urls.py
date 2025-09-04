from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("monApp/", include("monApp.urls")),
    path("admin/", admin.site.urls),
]