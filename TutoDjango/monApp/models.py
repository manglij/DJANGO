from django.db import models

class Categorie(models.Model):
    idCat = models.AutoField(primary_key=True)
    nomCat = models.CharField(max_length=100)

    def __str__(self):
        return self.nomCat

class Produit(models.Model):
    refProd = models.AutoField(primary_key=True)
    intituleProd = models.CharField(max_length=200)
    prixUnitaireProd = models.DecimalField(max_digits=10, decimal_places=2)
    # Relation CIF : chaque produit appartient à 1 catégorie (0,N côté catégorie 1,1 côté produit)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name="produits",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.intituleProd

class Rayon(models.Model):
    idRayon = models.AutoField(primary_key=True)
    nomRayon = models.CharField(max_length=100)

    def __str__(self):
        return self.nomRayon
    
class Contenir(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    rayon = models.ForeignKey(Rayon, on_delete=models.CASCADE)
    idcont = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.produit.intituleProd} dans {self.rayon.nomRayon}"