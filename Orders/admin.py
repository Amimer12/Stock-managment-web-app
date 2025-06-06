from django.contrib import admin
from .models import Commande
from .forms import CommandeForm
from Products.models import Variant, Produit
from Gestionnaires.models import Gestionnaire
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    form = CommandeForm
    list_display = ('id_commande_display','date_commande', 'etat_commande', 'get_display_variant', 'type_livraison','prix_total_dzd',)
    search_fields = ('etat_commande', 'nom_client', 'numero_client', 'produit_commandé__produit__nom_produit')
    list_filter = ('etat_commande','date_commande', 'produit_commandé__produit','produit_commandé__couleur','produit_commandé__taille', 'type_livraison', 'wilaya')
    ordering = ('-date_commande',)
    fieldsets = [
        ('Details de commande', {
            'classes': ('',),
            'fields': [ 'date_commande', 'etat_commande','produit_commandé', 'quantite_commandé',]}),
        ('Details de livraison', {
            'classes': ('',),
            'fields': ['type_livraison', 'Adresse_livraison', 'wilaya', 'commune']
        }),
        ('Prix total', {
            'classes': ('',),
            'fields': ['prix_total',]
        }),
        ('Detail de client', {
            'classes': ('',),
            'fields': ['nom_client', 'numero_client',]
        }),
        
    ]
    def id_commande_display(self, obj):
        return f"Cmd #{obj.id_commande}"
    id_commande_display.short_description = 'ID Commande'
    def get_display_variant(self, obj):
        return f"{obj.produit_commandé.produit.nom_produit} - {obj.produit_commandé.couleur.nom_couleur} - {obj.produit_commandé.taille.nom_taille}"
    get_display_variant.short_description = 'Produit commandé'

    def prix_total_dzd(self, obj):
        return f"{obj.prix_total} DZD"
    prix_total_dzd.short_description = 'Prix Total (DZD)'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        gestionnaire = Gestionnaire.objects.filter(user=user).first()
        if hasattr(user, 'groups') and user.groups.filter(name="Gestionnaire").exists():
            boutiques = gestionnaire.boutique.all()
            produits = Produit.objects.filter(boutique__in=boutiques)
            form.base_fields['produit_commandé'].queryset = Variant.objects.filter(
                produit__in=produits
            ).distinct()
        return form
    
    class Media:
        js = ('wilaya_bureau.js',)  

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
    readonly_fields = ('created_at','name', 'sheet_url')
