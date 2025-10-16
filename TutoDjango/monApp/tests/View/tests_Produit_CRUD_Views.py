from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Produit, Categorie, Statut
from datetime import date

# ----------------------------------------------------------------------
# Mixin pour initialiser l'utilisateur et les dépendances (Catégorie, Statut)
# ----------------------------------------------------------------------
class ProduitTestSetup(TestCase):
    """Configuration de base pour les tests de Produit (dépendances et utilisateur)."""
    
    def setUp(self):
        # Dépendances pour créer un Produit
        self.categorie = Categorie.objects.create(nomCat="TestCat")
        self.statut = Statut.objects.create(nomStatut="Online")
        
        # Utilisateur connecté requis pour les opérations CRUD
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        
        # Données de base pour un produit
        self.product_data = {
            "intituleProd": "Ecouteurs sans fil",
            "prixUnitaireProd": 50.00,
            "date_fabrication": date(2025, 10, 16),
            # Note : Categorie et Statut sont exclus du ProduitForm, mais peuvent être utilisés
            # si la vue était une CreateView/UpdateView générique. Ici, nous nous concentrons
            # sur les champs inclus dans le ProduitForm par défaut (fields = '__all__', exclude = ('categorie', 'statut'))
        }

# ----------------------------------------------------------------------
# Tests de la Vue de Création (CreateView: crt-prdt)
# ----------------------------------------------------------------------
class ProduitCreateViewTest(ProduitTestSetup):
    """Teste l'affichage et la soumission du formulaire de création de Produit."""
    
    def test_produit_create_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(reverse('crt-prdt'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/create_produit.html')

    def test_produit_create_view_post_valid(self):
        """Vérifie la création réussie d'un produit (POST avec données valides)."""
        initial_count = Produit.objects.count()
        response = self.client.post(reverse('crt-prdt'), self.product_data)
        
        # Le code de la vue redirige vers la page de détail ('dtl_prdt') après la création (Statut 302)
        self.assertEqual(response.status_code, 302) 
        
        # Vérifie qu'un objet a été créé
        self.assertEqual(Produit.objects.count(), initial_count + 1)
        
        # Vérifie la valeur de l'objet créé
        new_product = Produit.objects.last()
        self.assertEqual(new_product.intituleProd, self.product_data['intituleProd'])
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_prdt', args=[new_product.refProd])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

# ----------------------------------------------------------------------
# Tests de la Vue de Détail (DetailView: dtl_prdt)
# ----------------------------------------------------------------------
class ProduitDetailViewTest(ProduitTestSetup):
    """Teste l'affichage de la page de détail d'un Produit."""
    
    def setUp(self):
        super().setUp()
        # Créer un produit spécifique pour le test de détail
        self.product = Produit.objects.create(
            refProd=10, 
            categorie=self.categorie, 
            statut=self.statut,
            **self.product_data
        )
        self.url = reverse('dtl_prdt', args=[self.product.refProd])
        
    def test_produit_detail_view_ok(self):
        """Vérifie l'accès, le template et le contenu affiché pour un Produit existant (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_produit.html')
        
        # Vérifie que les informations du produit sont affichées
        self.assertContains(response, self.product.intituleProd)
        self.assertContains(response, str(self.product.refProd))
    
    def test_produit_detail_view_ko(self):
        """Vérifie que la page de détail renvoie 404 pour une id non existante."""
        url = reverse('dtl_prdt', args=[9999])
        response = self.client.get(url)
        # DetailView utilise get_object_or_404 implicitement
        self.assertEqual(response.status_code, 404)

# ----------------------------------------------------------------------
# Tests de la Vue de Mise à Jour (Function View: prdt-chng)
# ----------------------------------------------------------------------
class ProduitUpdateViewTest(ProduitTestSetup):
    """Teste l'affichage et la soumission du formulaire de mise à jour de Produit."""
    
    def setUp(self):
        super().setUp()
        # Créer un produit spécifique pour le test de modification
        self.product = Produit.objects.create(
            refProd=20, 
            categorie=self.categorie, 
            statut=self.statut,
            **self.product_data
        )
        self.url = reverse('prdt-chng', args=[self.product.refProd])

    def test_produit_update_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_produit.html')

    def test_produit_update_view_post_valid(self):
        """Vérifie la mise à jour réussie d'un produit (POST avec données valides)."""
        # Mise à jour des données
        updated_data = self.product_data.copy()
        updated_data['intituleProd'] = 'Ecouteurs NOUVEAU NOM'
        
        response = self.client.post(self.url, updated_data)
        
        # Redirection après la mise à jour (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Recharger l'objet depuis la base de données
        self.product.refresh_from_db()
        
        # Vérifier la mise à jour du nom
        self.assertEqual(self.product.intituleProd, updated_data['intituleProd'])
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_prdt', args=[self.product.refProd])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

# ----------------------------------------------------------------------
# Tests de la Vue de Suppression (DeleteView: prdt-del)
# ----------------------------------------------------------------------
class ProduitDeleteViewTest(ProduitTestSetup):
    """Teste l'affichage et la soumission du formulaire de suppression de Produit."""
    
    def setUp(self):
        super().setUp()
        # Créer un produit spécifique pour le test de suppression
        self.product = Produit.objects.create(
            refProd=30, 
            categorie=self.categorie, 
            statut=self.statut,
            **self.product_data
        )
        self.url = reverse('prdt-del', args=[self.product.refProd])

    def test_produit_delete_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_produit.html')

    def test_produit_delete_view_post(self):
        """Vérifie la suppression réussie d'un produit (POST)."""
        # Vérifie que l'objet existe avant la suppression
        self.assertTrue(Produit.objects.filter(refProd=self.product.refProd).exists())
        
        response = self.client.post(self.url)
        
        # Vérifier la redirection après la suppression (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Produit.objects.filter(refProd=self.product.refProd).exists())
        
        # Vérifier que la redirection est vers la liste des produits ('produit')
        expected_url = reverse('produit')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)