from django.contrib import admin
from .models import Commande
from .forms import CommandeForm
from Products.models import Variant, Produit
from Gestionnaires.models import Gestionnaire
from django.urls import path
from django.http import JsonResponse


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    form = CommandeForm
    list_display = ('id_commande_display','date_commande', 'etat_commande', 'get_display_variant','prix_total_dzd',)
    search_fields = ('etat_commande', 'nom_client', 'numero_client', 'produit_commandé__produit__nom_produit')
    list_filter = ('etat_commande','date_commande', 'produit_commandé__produit','produit_commandé__couleur','produit_commandé__taille', 'type_livraison', 'wilaya')
    ordering = ('-date_commande',)
    fieldsets = [
        ('Détails de produit', {
            'fields': ['produit', 'couleur', 'taille', 'quantite_commandé']
        }),
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
    def get_display_variant(self, obj):
        return f"{obj.produit_commandé.produit.nom_produit} - {obj.produit_commandé.couleur.nom_couleur} - {obj.produit_commandé.taille.nom_taille}" if obj.produit_commandé else "Aucun produit"
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
