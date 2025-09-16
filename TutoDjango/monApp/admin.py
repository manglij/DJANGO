from django.contrib import admin
from .models import *
from decimal import Decimal, ROUND_HALF_UP


class ProduitInline(admin.TabularInline):
    model = Produit
    extra = 1 # nombre de lignes vides par défaut

class ProduitFilter(admin.SimpleListFilter):
    title = 'filtre produit'
    parameter_name = 'custom_status'

    def lookups(self, request, model_admin):
        return (
            ('OnLine', 'En ligne'),
            ('OffLine', 'Hors ligne'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'OnLine':
            return queryset.filter(statut=1)
        if self.value() == 'OffLine':
            return queryset.filter(statut=2)
        

def set_Produit_online(modeladmin, request, queryset):
    queryset.update(statut=1)
set_Produit_online.short_description = "Mettre en ligne"

def set_Produit_offline(modeladmin, request, queryset):
    queryset.update(statut=2)
set_Produit_offline.short_description = "Mettre hors ligne"


class ProduitAdmin(admin.ModelAdmin):
    model = Produit
    list_display = ["refProd", "intituleProd", "prixUnitaireProd", "prixTTCProd", "date_fabrication", "categorie", "statut"]
    list_editable = ["intituleProd", "prixUnitaireProd", "date_fabrication"]
    radio_fields = {"statut": admin.VERTICAL}
    search_fields = ('intituleProd', 'date_fabrication')
    list_filter = (ProduitFilter,)
    date_hierarchy = 'date_fabrication'
    ordering = ('-date_fabrication',)
    
    actions = [set_Produit_online, set_Produit_offline]
    


    def prixTTCProd(self, instance):
        return (instance.prixUnitaireProd * Decimal('1.20')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    prixTTCProd.short_description = "Prix TTC"
    prixTTCProd.admin_order_field = "prixUnitaireProd"

class CategorieAdmin(admin.ModelAdmin):
    model = Categorie
    inlines = [ProduitInline]

admin.site.register(Produit, ProduitAdmin)

admin.site.register(Categorie)
admin.site.register(Statut)
admin.site.register(Rayon)