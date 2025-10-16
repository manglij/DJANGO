from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Rayon

# ----------------------------------------------------------------------
# Tests de la Vue de Création (CreateView: crt-rayon)
# ----------------------------------------------------------------------
class RayonCreateViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de création de Rayon."""
    def setUp(self):
        # Connexion requise pour cette vue
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('crt-rayon') 

    def test_rayon_create_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Vérifie que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/create_rayon.html') #

    def test_rayon_create_view_post_valid(self):
        """Vérifie la création réussie d'un rayon (POST avec données valides)."""
        data = { "nomRayon": "RayonPourTestCreation" }
        response = self.client.post(self.url, data)
        
        # Le code de la vue redirige vers la page de détail ('dtl_rayons') après la création (Statut 302)
        self.assertEqual(response.status_code, 302) 
        
        # Vérifie qu'un objet a été créé
        self.assertEqual(Rayon.objects.count(), 1)
        
        # Vérifie la valeur de l'objet créé
        new_rayon = Rayon.objects.last()
        self.assertEqual(new_rayon.nomRayon, 'RayonPourTestCreation')
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_rayons', args=[new_rayon.idRayon])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


# ----------------------------------------------------------------------
# Tests de la Vue de Détail (DetailView: dtl_rayons)
# ----------------------------------------------------------------------
class RayonDetailViewTest(TestCase):
    """Teste l'affichage de la page de détail d'un Rayon."""
    
    def setUp(self):
        # Pas besoin d'être connecté pour cette vue
        self.rayon = Rayon.objects.create(idRayon=1, nomRayon="RayonPourTestDetail")
        self.url = reverse('dtl_rayons', args=[self.rayon.idRayon]) 

    def test_rayon_detail_view_ok(self):
        """Vérifie l'accès, le template et le contenu affiché pour un Rayon existant (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_rayon.html') #
        
        # Vérifie que les informations du rayon sont affichées
        self.assertContains(response, 'RayonPourTestDetail')
        self.assertContains(response, 'Référence :</strong> 1')
    
    def test_rayon_detail_view_ko(self):
        """Vérifie que la page de détail renvoie 404 pour un id non existant."""
        url = reverse('dtl_rayons', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


# ----------------------------------------------------------------------
# Tests de la Vue de Mise à Jour (Function View: rayon-chng)
# ----------------------------------------------------------------------
class RayonUpdateViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de mise à jour de Rayon."""
    
    def setUp(self):
        # Création et connexion requise pour cette vue
        self.rayon = Rayon.objects.create(idRayon=1, nomRayon="RayonPourTestUpdate")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('rayon-chng', args=[self.rayon.idRayon])

    def test_rayon_update_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_rayon.html') #

    def test_rayon_update_view_post_valid(self):
        """Vérifie la mise à jour réussie d'un rayon (POST avec données valides)."""
        initial_name = self.rayon.nomRayon
        self.assertEqual(initial_name, 'RayonPourTestUpdate')
        
        data = {'nomRayon': 'RayonPourTestAfterUpdate'}
        response = self.client.post(self.url, data)
        
        # Redirection après la mise à jour (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Recharger l'objet depuis la base de données
        self.rayon.refresh_from_db()
        
        # Vérifier la mise à jour du nom
        self.assertEqual(self.rayon.nomRayon, 'RayonPourTestAfterUpdate')
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_rayons', args=[self.rayon.idRayon])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


# ----------------------------------------------------------------------
# Tests de la Vue de Suppression (DeleteView: rayon-del)
# ----------------------------------------------------------------------
class RayonDeleteViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de suppression de Rayon."""
    
    def setUp(self):
        # Création et connexion requise pour cette vue
        self.rayon = Rayon.objects.create(idRayon=1, nomRayon="RayonPourTestDelete")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('rayon-del', args=[self.rayon.idRayon])

    def test_rayon_delete_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_rayon.html') #

    def test_rayon_delete_view_post(self):
        """Vérifie la suppression réussie d'un rayon (POST)."""
        # Vérifie que l'objet existe avant la suppression
        self.assertTrue(Rayon.objects.filter(idRayon=self.rayon.idRayon).exists())
        
        response = self.client.post(self.url)
        
        # Vérifier la redirection après la suppression (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Rayon.objects.filter(idRayon=self.rayon.idRayon).exists())
        
        # Vérifier que la redirection est vers la liste des rayons ('rayons')
        expected_url = reverse('rayons')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)