from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class Produit(models.Model):
    id_produit = models.AutoField(primary_key=True)
    nom_produit = models.CharField(max_length=30)
    prix_produit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    descreption_produit = models.TextField(blank=True)
    quantite_produit = models.IntegerField(blank=True, default=0)  
    boutique = models.ForeignKey('Boutique', related_name='produits', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nom_produit
    
class Couleur(models.Model):
    id_couleur = models.AutoField(primary_key=True)
    nom_couleur = models.CharField(max_length=30)

    def __str__(self):
        return self.nom_couleur

class Taille(models.Model):
    id_taille = models.AutoField(primary_key=True)
    nom_taille = models.CharField(max_length=30)

    def __str__(self):
        return self.nom_taille
class Boutique(models.Model):
    id_boutique = models.AutoField(primary_key=True)
    nom_boutique = models.CharField(max_length=30)
    def __str__(self):
        return self.nom_boutique

class Variant(models.Model):
    id_variant = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit, related_name="produit_couleur_taille", on_delete=models.CASCADE)
    couleur = models.ForeignKey(Couleur, related_name="produit_couleur_taille", on_delete=models.CASCADE)
    taille = models.ForeignKey(Taille, related_name="produit_couleur_taille", on_delete=models.CASCADE)
    quantite = models.IntegerField()

    class Meta:
        unique_together = ('produit', 'couleur', 'taille')

    def __str__(self):
        return f"{self.produit.nom_produit} - {self.couleur.nom_couleur} - {self.taille.nom_taille}"

    def clean(self):
        if self.quantite < 0:
            raise ValidationError({'quantite': "La quantité ne peut pas etre négative."})

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is called
        super().save(*args, **kwargs)
        self.update_produit_quantite()

    def delete(self, *args, **kwargs):
        produit = self.produit
        super().delete(*args, **kwargs)
        self.update_produit_quantite(produit)

    def update_produit_quantite(self, produit=None):
        if produit is None:
            produit = self.produit
        total = Variant.objects.filter(produit=produit).aggregate(models.Sum('quantite'))['quantite__sum'] or 0
        produit.quantite_produit = total
        produit.save(update_fields=['quantite_produit'])


