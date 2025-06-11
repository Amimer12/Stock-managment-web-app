from django import forms
from django.contrib.auth.models import User
from Gestionnaires.models import Gestionnaire
from django.core.exceptions import ValidationError
from Products.models import Boutique,Produit, Couleur, Taille, Variant
from Orders.models import Commande
import re



class EmployeRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label=''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer Mot de passe'}),
        label=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        labels = {
            'username': '',
            'email': '',
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        if len(password2) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_staff = True
        if commit:
            user.save()
        return user
    

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'
        widgets = {
            'commune': forms.Select(),
            'Bureau_Yalidine': forms.Select(),
            'Adresse_livraison': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prix_total'].label = 'Prix Total (DZD)'


    def clean(self):
        cleaned_data = super().clean()
        produit = cleaned_data.get('produit')
        couleur = cleaned_data.get('couleur')
        taille = cleaned_data.get('taille')
        type_livraison = cleaned_data.get('type_livraison')
        adresse = cleaned_data.get('Adresse_livraison')
        numero = cleaned_data.get('numero_client')
        bureau_yalidine = cleaned_data.get('Bureau_Yalidine')
        bureau_zd = cleaned_data.get('Bureau_ZR')

        # Variant resolution
        if bureau_yalidine and bureau_zd:
            raise forms.ValidationError("Veuillez choisir soit le Bureau Yalidine soit le Bureau ZD, pas les deux.")
        

        # Address required for home delivery
        if type_livraison == 'Domicile' and not adresse:
            self.add_error('Adresse_livraison', "Veuillez entrer une adresse de livraison.")

        # Phone number validation
        if numero and not re.fullmatch(r'\d{10,11}', numero):
            self.add_error('numero_client', "Entrez un numéro de téléphone réel.")

        return cleaned_data

    def save(self, commit=True):
        # Assign produit_commandé manually before saving
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
