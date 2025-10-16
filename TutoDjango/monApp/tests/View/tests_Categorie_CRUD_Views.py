from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Categorie

# Importez la fonction de modification si vous voulez tester la redirection
# Cependant, les tests ci-dessous se concentrent sur la vue et non sur l'URL elle-même, 
# donc les imports de vues ne sont pas strictement nécessaires ici.


# ----------------------------------------------------------------------
# Tests de la Vue de Création (CreateView: crt-cat)
# ----------------------------------------------------------------------
class CategorieCreateViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de création de Categorie."""
    def setUp(self):
        # Connexion requise pour cette vue (décorateur @method_decorator(login_required))
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('crt-cat') # Nom de l'URL pour la création

    def test_categorie_create_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Vérifie que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/create_categorie.html') #

    def test_categorie_create_view_post_valid(self):
        """Vérifie la création réussie d'une catégorie (POST avec données valides)."""
        data = { "nomCat": "CategoriePourTestCreation" }
        response = self.client.post(self.url, data)
        
        # Le code de la vue redirige vers la page de détail ('dtl_cat') après la création (Statut 302)
        self.assertEqual(response.status_code, 302) 
        
        # Vérifie qu'un objet a été créé
        self.assertEqual(Categorie.objects.count(), 1)
        
        # Vérifie la valeur de l'objet créé
        new_category = Categorie.objects.last()
        self.assertEqual(new_category.nomCat, 'CategoriePourTestCreation')
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_cat', args=[new_category.idCat])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


# ----------------------------------------------------------------------
# Tests de la Vue de Détail (DetailView: dtl_cat)
# ----------------------------------------------------------------------
class CategorieDetailViewTest(TestCase):
    """Teste l'affichage de la page de détail d'une Categorie."""
    def setUp(self):
        # Pas besoin d'être connecté pour cette vue
        self.ctgr = Categorie.objects.create(idCat=1, nomCat="CategoriePourTestDetail")
        self.url = reverse('dtl_cat', args=[self.ctgr.idCat]) # Nom de l'URL pour le détail

    def test_categorie_detail_view(self):
        """Vérifie l'accès, le template et le contenu affiché (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_categorie.html') #
        
        # Vérifie que les informations sont affichées
        self.assertContains(response, 'CategoriePourTestDetail')
        self.assertContains(response, '1')


# ----------------------------------------------------------------------
# Tests de la Vue de Mise à Jour (Function View: cat-chng)
# ----------------------------------------------------------------------
class CategorieUpdateViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de mise à jour de Categorie."""
    def setUp(self):
        # Création et connexion requise pour cette vue (décorateur @login_required)
        self.ctgr = Categorie.objects.create(idCat=1, nomCat="CategoriePourTestUpdate")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('cat-chng', args=[self.ctgr.idCat]) # Nom de l'URL pour la modification

    def test_categorie_update_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_categorie.html') #

    def test_update_view_post_valid(self):
        """Vérifie la mise à jour réussie d'une catégorie (POST avec données valides)."""
        initial_name = self.ctgr.nomCat
        self.assertEqual(initial_name, 'CategoriePourTestUpdate')
        
        data = {'nomCat': 'CategoriePourTestAfterUpdate'}
        response = self.client.post(self.url, data)
        
        # Redirection après la mise à jour (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Recharger l'objet depuis la base de données
        self.ctgr.refresh_from_db()
        
        # Vérifier la mise à jour du nom
        self.assertEqual(self.ctgr.nomCat, 'CategoriePourTestAfterUpdate')
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_cat', args=[self.ctgr.idCat])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

# ----------------------------------------------------------------------
# Tests de la Vue de Suppression (DeleteView: cat-del)
# ----------------------------------------------------------------------
class CategorieDeleteViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de suppression de Categorie."""
    def setUp(self):
        # Création et connexion requise pour cette vue (décorateur @method_decorator(login_required))
        self.ctgr = Categorie.objects.create(idCat=1, nomCat="CategoriePourTesDelete")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('cat-del', args=[self.ctgr.idCat]) # Nom de l'URL pour la suppression

    def test_categorie_delete_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_categorie.html') #

    def test_categorie_delete_view_post(self):
        """Vérifie la suppression réussie d'une catégorie (POST)."""
        # Vérifie que l'objet existe avant la suppression
        self.assertTrue(Categorie.objects.filter(idCat=self.ctgr.idCat).exists())
        
        response = self.client.post(self.url)
        
        # Vérifier la redirection après la suppression (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Categorie.objects.filter(idCat=self.ctgr.idCat).exists())
        
        # Vérifier que la redirection est vers la liste des catégories ('categories')
        expected_url = reverse('categories')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        