from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Statut

# ----------------------------------------------------------------------
# Tests de la Vue de Création (CreateView: crt-statut)
# ----------------------------------------------------------------------
class StatutCreateViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de création de Statut."""
    def setUp(self):
        # Connexion requise pour cette vue
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('crt-statut') 

    def test_statut_create_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Vérifie que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/create_statut.html') #

    def test_statut_create_view_post_valid(self):
        """Vérifie la création réussie d'un statut (POST avec données valides)."""
        data = { "nomStatut": "StatutPourTestCreation" }
        response = self.client.post(self.url, data)
        
        # Le code de la vue redirige vers la page de détail ('dtl_statut') après la création (Statut 302)
        self.assertEqual(response.status_code, 302) 
        
        # Vérifie qu'un objet a été créé
        self.assertEqual(Statut.objects.count(), 1)
        
        # Vérifie la valeur de l'objet créé
        new_statut = Statut.objects.last()
        self.assertEqual(new_statut.nomStatut, 'StatutPourTestCreation')
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_statut', args=[new_statut.idStatut])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


# ----------------------------------------------------------------------
# Tests de la Vue de Détail (DetailView: dtl_statut)
# ----------------------------------------------------------------------
class StatutDetailViewTest(TestCase):
    """Teste l'affichage de la page de détail d'un Statut."""
    
    def setUp(self):
        # Pas besoin d'être connecté pour cette vue
        self.statut = Statut.objects.create(idStatut=1, nomStatut="StatutPourTestDetail")
        self.url = reverse('dtl_statut', args=[self.statut.idStatut]) 

    def test_statut_detail_view_ok(self):
        """Vérifie l'accès, le template et le contenu affiché pour un Statut existant (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_statut.html') #
        
        # Vérifie que les informations du statut sont affichées
        self.assertContains(response, 'StatutPourTestDetail')
        self.assertContains(response, 'Référence :</strong> 1')
    
    def test_statut_detail_view_ko(self):
        """Vérifie que la page de détail renvoie 404 pour un id non existant."""
        url = reverse('dtl_statut', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


# ----------------------------------------------------------------------
# Tests de la Vue de Mise à Jour (Function View: statut-chng)
# ----------------------------------------------------------------------
class StatutUpdateViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de mise à jour de Statut."""
    
    def setUp(self):
        # Création et connexion requise pour cette vue
        self.statut = Statut.objects.create(idStatut=1, nomStatut="StatutPourTestUpdate")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('statut-chng', args=[self.statut.idStatut])

    def test_statut_update_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_statut.html') #

    def test_statut_update_view_post_valid(self):
        """Vérifie la mise à jour réussie d'un statut (POST avec données valides)."""
        initial_name = self.statut.nomStatut
        self.assertEqual(initial_name, 'StatutPourTestUpdate')
        
        data = {'nomStatut': 'StatutPourTestAfterUpdate'}
        response = self.client.post(self.url, data)
        
        # Redirection après la mise à jour (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Recharger l'objet depuis la base de données
        self.statut.refresh_from_db()
        
        # Vérifier la mise à jour du nom
        self.assertEqual(self.statut.nomStatut, 'StatutPourTestAfterUpdate')
        
        # Vérifie la cible de la redirection
        expected_url = reverse('dtl_statut', args=[self.statut.idStatut])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


# ----------------------------------------------------------------------
# Tests de la Vue de Suppression (DeleteView: statut-del)
# ----------------------------------------------------------------------
class StatutDeleteViewTest(TestCase):
    """Teste l'affichage et la soumission du formulaire de suppression de Statut."""
    
    def setUp(self):
        # Création et connexion requise pour cette vue
        self.statut = Statut.objects.create(idStatut=1, nomStatut="StatutPourTestDelete")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.url = reverse('statut-del', args=[self.statut.idStatut])

    def test_statut_delete_view_get(self):
        """Vérifie l'accès et le template utilisé pour l'affichage du formulaire (GET)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_statut.html') #

    def test_statut_delete_view_post(self):
        """Vérifie la suppression réussie d'un statut (POST)."""
        # Vérifie que l'objet existe avant la suppression
        self.assertTrue(Statut.objects.filter(idStatut=self.statut.idStatut).exists())
        
        response = self.client.post(self.url)
        
        # Vérifier la redirection après la suppression (Statut 302)
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Statut.objects.filter(idStatut=self.statut.idStatut).exists())
        
        # Vérifier que la redirection est vers la liste des statuts ('statuts')
        expected_url = reverse('statuts')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)