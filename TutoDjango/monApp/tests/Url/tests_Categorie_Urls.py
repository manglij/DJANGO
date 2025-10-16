from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Categorie
from monApp.views import CategorieListView, CategorieDetailView, CategorieCreateView, CategorieDeleteView
# Note : CategorieUpdate est une fonction, pas une classe de vue (View class), donc on ne l'importe pas pour resolve().

class CategorieUrlsTest(TestCase):
    
    def setUp(self):
        # 1. Création d'une catégorie pour les tests de détail/modification/suppression
        self.ctgr = Categorie.objects.create(nomCat="CategoriePourTest")
        
        # 2. Création et connexion d'un utilisateur pour tester les vues nécessitant une authentification
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    # --- Tests de résolution des URLs (resolve) ---

    def test_categorie_list_url_is_resolved(self):
        """Vérifie que l'URL 'categories' résout vers CategorieListView."""
        url = reverse('categories')
        # Vérification du nom d'URL
        self.assertEqual(resolve(url).view_name, 'categories')
        # Vérification de la classe de vue
        self.assertEqual(resolve(url).func.view_class, CategorieListView)

    def test_categorie_detail_url_is_resolved(self):
        """Vérifie que l'URL 'dtl_cat' résout vers CategorieDetailView."""
        # Note: on utilise le nom d'URL 'dtl_cat' comme défini dans urls.py
        url = reverse('dtl_cat', args=[1]) 
        self.assertEqual(resolve(url).view_name, 'dtl_cat')
        self.assertEqual(resolve(url).func.view_class, CategorieDetailView)

    def test_categorie_create_url_is_resolved(self):
        """Vérifie que l'URL 'crt-cat' résout vers CategorieCreateView."""
        url = reverse('crt-cat')
        self.assertEqual(resolve(url).view_name, 'crt-cat')
        self.assertEqual(resolve(url).func.view_class, CategorieCreateView)

    def test_categorie_update_url_is_resolved(self):
        """Vérifie que l'URL 'cat-chng' résout vers la fonction CategorieUpdate."""
        # Note : CategorieUpdate est une fonction dans views.py, pas une classe View.
        from monApp.views import CategorieUpdate
        url = reverse('cat-chng', args=[1])
        self.assertEqual(resolve(url).view_name, 'cat-chng')
        self.assertEqual(resolve(url).func, CategorieUpdate)

    def test_categorie_delete_url_is_resolved(self):
        """Vérifie que l'URL 'cat-del' résout vers CategorieDeleteView."""
        url = reverse('cat-del', args=[1])
        self.assertEqual(resolve(url).view_name, 'cat-del')
        self.assertEqual(resolve(url).func.view_class, CategorieDeleteView)

    # --- Tests de statut de réponse HTTP (GET) ---

    def test_categorie_list_response_code(self):
        """Vérifie que la page de liste des catégories est accessible (code 200)."""
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_categorie_create_response_code_OK(self):
        """Vérifie que la page de création est accessible (code 200) en étant connecté."""
        response = self.client.get(reverse('crt-cat'))
        self.assertEqual(response.status_code, 200)

    def test_categorie_detail_response_code_OK(self):
        """Vérifie que la page de détail est accessible (code 200) pour une id existante."""
        url = reverse('dtl_cat', args=[self.ctgr.idCat]) # idCat existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_categorie_detail_response_code_KO(self):
        """Vérifie que la page de détail renvoie 404 pour une id non existante."""
        url = reverse('dtl_cat', args=[9999]) # idCat non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_categorie_update_response_code_OK(self):
        """Vérifie que la page de modification est accessible (code 200) pour une id existante."""
        url = reverse('cat-chng', args=[self.ctgr.idCat]) # idCat existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_categorie_update_response_code_KO(self):
        """Vérifie que la page de modification renvoie 404 pour une id non existante."""
        url = reverse('cat-chng', args=[9999]) # idCat non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_categorie_delete_response_code_OK(self):
        """Vérifie que la page de suppression est accessible (code 200) pour une id existante."""
        url = reverse('cat-del', args=[self.ctgr.idCat]) # idCat existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_categorie_delete_response_code_KO(self):
        """Vérifie que la page de suppression renvoie 404 pour une id non existante."""
        url = reverse('cat-del', args=[9999]) # idCat non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # --- Tests de redirection (POST) ---
    
    # Note : Crée une nouvelle catégorie, qui aura l'id '2' si la catégorie '1' est celle de setUp.
    def test_redirect_after_categorie_creation(self):
        """Vérifie la redirection après la création réussie d'une catégorie."""
        new_cat_name = 'CategoriePourTestRedirectionCreation'
        response = self.client.post(reverse('crt-cat'), {'nomCat': new_cat_name})

        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        
        # Le code de la vue CategorieCreateView redirige vers 'dtl_cat'
        # On suppose que c'est le 2ème objet créé (le 1er étant self.ctgr)
        new_cat_id = Categorie.objects.get(nomCat=new_cat_name).idCat
        expected_url = reverse('dtl_cat', args=[new_cat_id])
        
        # Vérification de la redirection vers la vue de détail
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        
    def test_redirect_after_categorie_updating(self):
        """Vérifie la redirection après la modification réussie d'une catégorie."""
        new_name = "CategoriePourTestRedirectionMaj"
        url = reverse('cat-chng', args=[self.ctgr.idCat])
        response = self.client.post(url, data={"nomCat": new_name})

        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        
        # Redirection vers la vue de détail
        expected_url = reverse('dtl_cat', args=[self.ctgr.idCat])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        
        # Vérifie que le nom a été mis à jour
        self.assertEqual(Categorie.objects.get(idCat=self.ctgr.idCat).nomCat, new_name)

    def test_redirect_after_categorie_deletion(self):
        """Vérifie la redirection après la suppression réussie d'une catégorie."""
        # Note : On utilise self.ctgr.idCat car pk dans Categorie est idCat
        url = reverse('cat-del', args=[self.ctgr.idCat])
        response = self.client.post(url)
        
        # Vérifie qu'on a bien une redirection (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # La vue CategorieDeleteView a success_url = "/monApp/categories/" (alias 'categories')
        expected_url = reverse('categories')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Categorie.objects.filter(pk=self.ctgr.idCat).exists())