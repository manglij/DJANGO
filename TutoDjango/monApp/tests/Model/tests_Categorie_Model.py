from django.test import TestCase
from monApp.models import Categorie

class CategorieModelTest(TestCase):

    # Méthode exécutée avant chaque test pour créer les objets nécessaires.
    def setUp(self):
        # Créer un objet Categorie à utiliser dans les tests
        self.ctgr = Categorie.objects.create(nomCat="CategoriePourTest")

    # Vérifie que la création de l'objet Categorie se passe correctement.
    def test_categorie_creation(self):
        self.assertEqual(self.ctgr.nomCat, "CategoriePourTest")

    # Vérifie que la méthode __str__() renvoie le format correct.
    def test_string_representation(self):
        self.assertEqual(str(self.ctgr), "CategoriePourTest")

    # Vérifie la capacité à mettre à jour un objet Categorie.
    def test_categorie_updating(self):
        self.ctgr.nomCat = "CategoriePourTests"
        self.ctgr.save()
        # Récupérer l'objet mis à jour
        updated_ctgr = Categorie.objects.get(idCat=self.ctgr.idCat)
        self.assertEqual(updated_ctgr.nomCat, "CategoriePourTests")

    # Vérifie que l'objet peut être supprimé et qu'il n'est plus en base.
    def test_categorie_deletion(self):
        self.ctgr.delete()
        self.assertEqual(Categorie.objects.count(), 0)