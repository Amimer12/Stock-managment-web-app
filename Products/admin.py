from django.contrib import admin
from .models import Produit, Couleur, Taille, Variant, Boutique
from .forms import ProduitForm
from django.contrib import admin
from Gestionnaires.models import Gestionnaire

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    form = ProduitForm
    list_display = ('ID','nom_produit', 'prix_produit_dzd', 'quantite_produit','boutique',)
    search_fields = ('ID','nom_produit', 'categorie_produit','boutique__nom_boutique')
    list_filter = ('boutique',)
    ordering = ('-id_produit',)
    fieldsets = [
        ('Details de produit', {
            'classes': ('',),
            'fields': [ 'ID','nom_produit', 'boutique','prix_produit', 'quantite_produit',]}),
    ]
    readonly_fields = ['quantite_produit']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        gestionnaire = Gestionnaire.objects.filter(user=user).first()
        if hasattr(user, 'groups') and user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(boutique__in=gestionnaire.boutique.all()).distinct()
        return qs

    def prix_produit_dzd(self, obj):
        return f"{obj.prix_produit} DZD"
    prix_produit_dzd.short_description = 'Prix (DZD)'

@admin.register(Couleur)
class CouleurAdmin(admin.ModelAdmin):
    list_display = ('nom_couleur',)  
    search_fields = ('nom_couleur',)
    ordering = ('-id_couleur',)
    fieldsets = [
        ('Couleur', {
            'classes': ('',),
            'fields': ['nom_couleur',]}),
    ]

@admin.register(Taille)
class TailleAdmin(admin.ModelAdmin):
    list_display = ('nom_taille',)  
    search_fields = ('nom_taille',)
    ordering = ('-id_taille',)
    fieldsets = [
        ('Taille', {
            'classes': ('',),
            'fields': ['nom_taille',]}),
    ]

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('get_display_variant','produit', 'couleur', 'taille', 'quantite')
    search_fields = ('produit__nom_produit', 'couleur__nom_couleur', 'taille__nom_taille','SKU')
    list_filter = ('produit', 'couleur', 'taille')
    ordering = ('-id_variant',)
    fieldsets = [
            ('Details de produit', {
                'classes': ('',),
                'fields': [ 'SKU','produit', 'couleur','taille', 'quantite',]}),
        ]
    def get_display_variant (self, obj):
        return '{obj.produit} - {obj.couleur.nom_couleur} - {obj.taille.nom_taille}'.format(obj=obj)
        
    get_display_variant.short_description = 'Variant'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        gestionnaire = Gestionnaire.objects.filter(user=user).first()
        if hasattr(user, 'groups') and user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(produit__boutique__in=gestionnaire.boutique.all()).distinct()
        return qs

from django.contrib import admin
from Products.models import Produit


class ProduitInline(admin.TabularInline):
    model = Produit
    extra = 0  # Show one blank form for new entry
    fields = ('ID','nom_produit', 'prix_produit', 'quantite_produit')  # Only show selected fields
    can_delete = False  # Remove the delete checkbox
    show_change_link = True  # Optional: link to full edit page
    readonly_fields = ('ID','nom_produit', 'prix_produit', 'quantite_produit')
    def has_add_permission(self, request, obj=None):
        return False  




@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom_boutique','nombre_produits',)
    inlines = [ProduitInline]
    search_fields = ('nom_boutique',)
    ordering = ('-id_boutique',)
    fieldsets = [
        ('Boutique', {
            'classes': ('',),
            'fields': ['nom_boutique',]}),
    ]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        gestionnaire = Gestionnaire.objects.filter(user=user).first()
        if hasattr(user, 'groups') and user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(id_boutique__in=gestionnaire.boutique.all()).distinct()
        return qs
    def nombre_produits(self, obj):
        return obj.produits.count()  
    nombre_produits.short_description = 'Nombres de Produits'
