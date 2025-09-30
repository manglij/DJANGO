from django import forms
from .models import *



class ContactUsForm(forms.Form):
	name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField(max_length=1000)




class ProduitForm(forms.ModelForm):
	class Meta:
		model = Produit
		fields = '__all__'
		exclude = ('categorie', 'statut')