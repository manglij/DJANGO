from django.test import TestCase
from monApp.models import Categorie
from monApp.forms import CategorieForm

class CategorieFormTest(TestCase):

    def test_form_valid_data(self):
        """Vérifie que le formulaire est valide avec des données correctes."""
        # Les données correctes sont un nom de catégorie (max_length=100 selon models.py)
        form = CategorieForm(data={'nomCat': 'CategoriePourTest'})
        self.assertTrue(form.is_valid()) # Le formulaire doit être valide

    def test_form_invalid_data_too_long(self):
        """Vérifie que le formulaire est invalide si nomCat est trop long."""
        # Crée une chaîne de plus de 100 caractères (max_length dans models.py)
        long_name = 'a' * 101 # 101 caractères pour dépasser la limite de 100
        
        form = CategorieForm(data={'nomCat': long_name})
        
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('nomCat', form.errors) # Le champ 'nomCat' doit contenir une erreur
        # Le message d'erreur est basé sur la validation par défaut de CharField.
        # Note : Le message que vous avez fourni ('Assurez-vous que cette valeur comporte au plus 100
        # caractères (actuellement 102).') suppose 102 caractères. J'utilise 101 pour l'exemple.
        
        # Pour une validation stricte du message d'erreur :
        # Le modèle Categorie a `nomCat = models.CharField(max_length=100)`.
        self.assertEqual(form.errors['nomCat'], [f'Assurez-vous que cette valeur comporte au plus 100 caractères (actuellement {len(long_name)}).'])
        
    def test_form_invalid_data_missed(self):
        """Vérifie que le formulaire est invalide si nomCat est manquant (vide)."""
        # Le champ est obligatoire (par défaut pour CharField)
        form = CategorieForm(data={'nomCat': ''})
        
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('nomCat', form.errors) # Le champ 'nomCat' doit contenir une erreur
        self.assertEqual(form.errors['nomCat'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        """Vérifie que le formulaire peut être enregistré et que l'objet créé est correct."""
        data = {'nomCat': 'NouvelleCategorie'}
        form = CategorieForm(data=data)
        
        self.assertTrue(form.is_valid())
        
        # Vérifie que la base de données est vide avant la sauvegarde
        self.assertEqual(Categorie.objects.count(), 0)
        
        ctgr = form.save()
        
        # Vérifie que l'objet a été créé en base
        self.assertEqual(Categorie.objects.count(), 1)
        
        # Vérifie que les données sauvegardées correspondent
        self.assertEqual(ctgr.nomCat, data['nomCat'])
        # Le champ idCat est AutoField et sera 1 pour le premier objet
        self.assertEqual(ctgr.idCat, 1)