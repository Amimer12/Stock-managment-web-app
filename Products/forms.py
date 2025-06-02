from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prix_produit'].label = 'Prix du produit (DZD)'