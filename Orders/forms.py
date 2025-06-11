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
    produit = forms.ModelChoiceField(
        queryset=Produit.objects.all(),
        required=True,
        label="Produit"
    )
    couleur = forms.ModelChoiceField(
        queryset=Couleur.objects.all(),
        required=True,
        label="Couleur"
    )
    taille = forms.ModelChoiceField(
        queryset=Taille.objects.all(),
        required=True,
        label="Taille"
    )

    class Meta:
        model = Commande
        fields = '__all__'
        exclude = ['produit_commandé']
        widgets = {
            'commune': forms.Select(),
            'Bureau_Yalidine': forms.Select(),
            'Adresse_livraison': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['prix_total'].label = 'Prix Total (DZD)'

        if self.instance and self.instance.produit_commandé:
            self.fields['produit'].initial = self.instance.produit_commandé.produit
            self.fields['couleur'].initial = self.instance.produit_commandé.couleur
            self.fields['taille'].initial = self.instance.produit_commandé.taille

        self._variant = None  # store the resolved variant for use in save()

    def clean(self):
        cleaned_data = super().clean()
        produit = cleaned_data.get('produit')
        couleur = cleaned_data.get('couleur')
        taille = cleaned_data.get('taille')
        quantite_commandé = cleaned_data.get('quantite_commandé')
        type_livraison = cleaned_data.get('type_livraison')
        adresse = cleaned_data.get('Adresse_livraison')
        numero = cleaned_data.get('numero_client')
        bureau_yalidine = cleaned_data.get('Bureau_Yalidine')
        bureau_zd = cleaned_data.get('Bureau_ZD')

        # Variant resolution
        if bureau_yalidine and bureau_zd:
            raise forms.ValidationError("Veuillez choisir soit le Bureau Yalidine soit le Bureau ZD, pas les deux.")
        
        if produit and couleur and taille:
            try:
                variant = Variant.objects.get(produit=produit, couleur=couleur, taille=taille)
                self._variant = variant  # store to assign in save()
            except Variant.DoesNotExist:
                raise forms.ValidationError("Aucun variant correspondant trouvé pour cette combinaison.")
        else:
            raise forms.ValidationError("Veuillez sélectionner un produit, une couleur et une taille.")

        # Stock check
        if self._variant and quantite_commandé is not None:
            if self.instance.pk is None:
                if quantite_commandé > self._variant.quantite:
                    self.add_error('quantite_commandé', f"Stock insuffisant (stock actuel : {self._variant.quantite})")
            else:
                old_commande = Commande.objects.get(pk=self.instance.pk)
                diff = quantite_commandé - old_commande.quantite_commandé
                if diff > self._variant.quantite:
                    self.add_error('quantite_commandé', f"Stock insuffisant pour cette modification (stock actuel : {self._variant.quantite})")

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
        if self._variant:
            instance.produit_commandé = self._variant
        if commit:
            instance.save()
        return instance
