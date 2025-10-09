from django.shortcuts import render
from django.http import HttpResponse
from monApp.forms import *
from monApp.models import *
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.db.models import Count



def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")


class HomeView(TemplateView):
    template_name = "monApp/page_home.html"
    

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Welcome to Django! " + self.kwargs.get('param', '')
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)  
    

class AboutView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    

    def post(self, request, **kwargs):
        return render(request, self.template_name)

def ContactView(request):
    titreh1 = "Contact us !"
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monprojet.com'],
            )

            return redirect('email-sent')
    else:
        form = ContactUsForm()
    return render(request, "monApp/page_home.html", {'titreh1': titreh1, 'form': form})

class EmailSentView(TemplateView):
    template_name = "monApp/email_sent.html"

    def get_context_data(self, **kwargs):
        context = super(EmailSentView, self).get_context_data(**kwargs)
        context['titreh1'] = "Email sent! We'll be in touch."
        return context



class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "prdts"

    def get_queryset(self ) :
        return Produit.objects.order_by("prixUnitaireProd")
    
    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context
    

class ProduitDetailView(DetailView):
    model = Produit
    template_name = "monApp/detail_produit.html"
    context_object_name = "prdt"

    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context
    

class CategorieListView(ListView):
    model = Categorie
    template_name = "monApp/list_categories.html"
    context_object_name = "cats"

    def get_queryset(self ) :
        return Categorie.objects.order_by("nomCat")
    
    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits'))

    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context

class CategorieDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "cat"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits'))

    def get_context_data(self, **kwargs):
        context = super(CategorieDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        context['prdts'] = self.object.produits.all()
        return context
    

class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rays"

    def get_queryset(self ) :
        return Rayon.objects.order_by("nomRayon")
    
    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        rays_dt = []
        for rayon in context['rays']:
            total = 0
            for contenir in rayon.contenir_rayon.all():
                total += contenir.produit.prixUnitaireProd * contenir.quantite
            rays_dt.append({'rayon': rayon, 'total_stock': total})
        context['rays_dt'] = rays_dt
        print(rays_dt)
        return context

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "ray"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        return context
    
class StatutListView(ListView):
    model = Statut
    template_name = "monApp/list_statuts.html"
    context_object_name = "stats"

    def get_queryset(self ) :
        return Statut.objects.order_by("nomStatut")
    
    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Statut.objects.annotate(nb_produits=Count('produits'))

    
    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes statuts"
        return context

class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/detail_statut.html"
    context_object_name = "stat"


    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Statut.objects.annotate(nb_produits=Count('produits'))


    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        context['prdts'] = self.object.produits.all()
        return context
    

class ConnectView(LoginView):
    template_name = 'monApp/page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monApp/page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'monApp/page_register.html')
        

class RegisterView(TemplateView):
    template_name = 'monApp/page_register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monApp/page_login.html')
        else:
            return render(request, 'monApp/page_register.html')
        
from django.contrib.auth import logout

class DisconnectView(TemplateView):
    template_name = 'monApp/page_logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    


class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = "monApp/create_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    

def ProduitUpdate(request, pk):
    prdt = Produit.objects.get(refProd=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=prdt)
        if form.is_valid():
            # mettre à jour le produit existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du produit que nous venons de mettre à jour
            return redirect('dtl_prdt', prdt.refProd)
    else:
        form = ProduitForm(instance=prdt)
    return render(request,'monApp/update_produit.html', {'form': form})

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = "monApp/delete_produit.html"
    success_url = "/monApp/produits/"

    def get_context_data(self, **kwargs):
        context = super(ProduitDeleteView, self).get_context_data(**kwargs)
        context['titremenu'] = "Suppression du produit"
        return context
    

class RayonCreateView(CreateView):
    model = Rayon
    form_class = RayonForm
    template_name = "monApp/create_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('dtl_rayons', rayon.idRayon)

class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = "monApp/create_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        categorie = form.save()
        return redirect('dtl_cat', categorie.idCat)

class StatutCreateView(CreateView):
    model = Statut
    form_class = StatutForm
    template_name = "monApp/create_statut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        statut = form.save()
        return redirect('dtl_statut', statut.idStatut)
    
def CategorieUpdate(request, pk):
    cat = Categorie.objects.get(idCat=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=cat)
        if form.is_valid():
            # mettre à jour la catégorie existante dans la base de données
            form.save()
            # rediriger vers la page détaillée de la catégorie que nous venons de mettre à jour
            return redirect('dtl_cat', cat.idCat)
    else:
        form = CategorieForm(instance=cat)
    return render(request,'monApp/update_categorie.html', {'form': form})

def RayonUpdate(request, pk):
    ray = Rayon.objects.get(idRayon=pk)
    if request.method == 'POST':
        form = RayonForm(request.POST, instance=ray)
        if form.is_valid():
            # mettre à jour le rayon existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du rayon que nous venons de mettre à jour
            return redirect('dtl_rayons', ray.idRayon)
    else:
        form = RayonForm(instance=ray)
    return render(request,'monApp/update_rayon.html', {'form': form})

def StatutUpdate(request, pk):
    stat = Statut.objects.get(idStatut=pk)
    if request.method == 'POST':
        form = StatutForm(request.POST, instance=stat)
        if form.is_valid():
            # mettre à jour le statut existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du statut que nous venons de mettre à jour
            return redirect('dtl_statut', stat.idStatut)
    else:
        form = StatutForm(instance=stat)
    return render(request,'monApp/update_statut.html', {'form': form})

class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/delete_categorie.html"
    success_url = "/monApp/categories/"

    def get_context_data(self, **kwargs):
        context = super(CategorieDeleteView, self).get_context_data(**kwargs)
        context['titremenu'] = "Suppression de la catégorie"
        return context
    

class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/delete_rayon.html"
    success_url = "/monApp/rayons/"

    def get_context_data(self, **kwargs):
        context = super(RayonDeleteView, self).get_context_data(**kwargs)
        context['titremenu'] = "Suppression du rayon"
        return context

class StatutDeleteView(DeleteView):
    model = Statut
    template_name = "monApp/delete_statut.html"
    success_url = "/monApp/statuts/"

    def get_context_data(self, **kwargs):
        context = super(StatutDeleteView, self).get_context_data(**kwargs)
        context['titremenu'] = "Suppression du statut"
        return context
    
