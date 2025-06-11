from django.contrib import admin
from .models import Commande, ProduitCommande
from .forms import CommandeForm
from Products.models import Variant, Produit
from Gestionnaires.models import Gestionnaire
from django.urls import path
from django.http import JsonResponse
from django import forms

class ProduitCommandeInlineForm(forms.ModelForm):
    class Meta:
        model = ProduitCommande
        fields = ['produit', 'couleur', 'taille', 'quantite']

    def clean(self):
        cleaned_data = super().clean()
        produit = cleaned_data.get("produit")
        couleur = cleaned_data.get("couleur")
        taille = cleaned_data.get("taille")
        quantite = cleaned_data.get("quantite")

        # Skip validation for empty rows
        if not (produit or couleur or taille or quantite):
            return cleaned_data  # Do nothing

        if not (produit and couleur and taille):
            raise forms.ValidationError("Veuillez sélectionner un produit, une couleur et une taille.")

        try:
            variant = Variant.objects.get(produit=produit, couleur=couleur, taille=taille)
        except Variant.DoesNotExist:
            raise forms.ValidationError("Aucun variant correspondant pour cette combinaison.")

        if quantite is not None and quantite > variant.quantite:
            raise forms.ValidationError(f"Stock insuffisant. Disponible : {variant.quantite}")

        return cleaned_data



class ProduitCommandeInline(admin.TabularInline):
    model = ProduitCommande
    form = ProduitCommandeInlineForm
    extra = 0



@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    inlines = [ProduitCommandeInline]
    list_display = ('id_commande_display', 'date_commande', 'etat_commande', 'prix_total_dzd',)
    search_fields = ('etat_commande', 'nom_client', 'numero_client', 'lignes__variant__produit__nom_produit')
    list_filter = ('etat_commande','date_commande', 'type_livraison', 'wilaya')
    ordering = ('-date_commande',)
    form = CommandeForm
    fieldsets = [
        ('Details de commande', {
            'fields': ['date_commande', 'etat_commande']
        }),
        ('Details de livraison', {
            'fields': ['type_livraison', 'Adresse_livraison', 'wilaya', 'commune','Bureau_Yalidine','Bureau_ZD']
        }),
        ('Prix total', {
            'fields': ['prix_total']
        }),
        ('Detail de client', {
            'fields': ['nom_client', 'numero_client']
        }),
    ]

    def id_commande_display(self, obj):
        return f"Cmd #{obj.id_commande}"
    id_commande_display.short_description = 'ID Commande'

    def prix_total_dzd(self, obj):
        return f"{obj.prix_total} DZD"
    prix_total_dzd.short_description = 'Prix Total (DZD)'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('check-variant/', self.admin_site.admin_view(self.check_variant)),
        ]
        return custom_urls + urls

    def check_variant(self, request):
        produit_id = request.GET.get('produit')
        couleur_id = request.GET.get('couleur')
        taille_id = request.GET.get('taille')

        try:
            variant = Variant.objects.get(
                produit_id=produit_id,
                couleur_id=couleur_id,
                taille_id=taille_id
            )
            return JsonResponse({'message': f"Quantité disponible: {variant.quantite}"})
        except Variant.DoesNotExist:
            return JsonResponse({'message': "Aucun variant correspondant."})
    class Media:
        js = ('wilaya_bureau.js','bureau.js',)  

# admin.py
from django.contrib import admin
from .models import Sheet

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'sheet_url')
    search_fields = ('name', 'sheet_url')
    fieldsets = (
        (None, {
            'fields': ('name', 'sheet_url')
        }),
        ('Created at', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)
