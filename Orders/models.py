from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from Products.models import Variant
from django.core.exceptions import ValidationError
from decimal import Decimal
import re

WILAYA_CHOICES = [
    ('Adrar', 'Adrar'), ('Chlef', 'Chlef'), ('Laghouat', 'Laghouat'), ('Oum El Bouaghi', 'Oum El Bouaghi'),
    ('Batna', 'Batna'), ('Bejaia', 'Bejaia'), ('Biskra', 'Biskra'), ('Bechar', 'Bechar'),
    ('Blida', 'Blida'), ('Bouira', 'Bouira'), ('Tamanrasset', 'Tamanrasset'), ('Tebessa', 'Tebessa'),
    ('Tlemcen', 'Tlemcen'), ('Tiaret', 'Tiaret'), ('Tizi Ouzou', 'Tizi Ouzou'), ('Alger', 'Alger'),
    ('Djelfa', 'Djelfa'), ('Jijel', 'Jijel'), ('Setif', 'Setif'), ('Saida', 'Saida'),
    ('Skikda', 'Skikda'), ('Sidi Bel Abbes', 'Sidi Bel Abbes'), ('Annaba', 'Annaba'), ('Guelma', 'Guelma'),
    ('Constantine', 'Constantine'), ('Medea', 'Medea'), ('Mostaganem', 'Mostaganem'), ('Msila', 'Msila'),
    ('Mascara', 'Mascara'), ('Ouargla', 'Ouargla'), ('Oran', 'Oran'), ('El Bayadh', 'El Bayadh'),
    ('Illizi', 'Illizi'), ('Bordj Bou Arreridj', 'Bordj Bou Arreridj'), ('Boumerdes', 'Boumerdes'),
    ('El Tarf', 'El Tarf'), ('Tindouf', 'Tindouf'), ('Tissemsilt', 'Tissemsilt'), ('El Oued', 'El Oued'),
    ('Khenchela', 'Khenchela'), ('Souk Ahras', 'Souk Ahras'), ('Tipaza', 'Tipaza'), ('Mila', 'Mila'),
    ('Ain Defla', 'Ain Defla'), ('Naama', 'Naama'), ('Ain Temouchent', 'Ain Temouchent'), ('Ghardaia', 'Ghardaia'),
    ('Relizane', 'Relizane'), ('Timimoun', 'Timimoun'), ('Bordj Badji Mokhtar', 'Bordj Badji Mokhtar'),
    ('Ouled Djellal', 'Ouled Djellal'), ('Beni Abbes', 'Beni Abbes'), ('In Salah', 'In Salah'),
    ('In Guezzam', 'In Guezzam'), ('Touggourt', 'Touggourt'), ('Djanet', 'Djanet'), ('El M\'Ghair', 'El M\'Ghair'),
    ('El Menia', 'El Menia')
]

class Commande(models.Model):
    id_commande = models.AutoField(primary_key=True)
    date_commande = models.DateField(default=now)
    produit_commandé = models.ForeignKey("Products.Variant", related_name="produit_commandé", on_delete=models.CASCADE)
    quantite_commandé = models.IntegerField(default=1)
    etat_commande = models.CharField(
        max_length=30,
        choices=[
            ("En attente", _("En attente")),
            ("Livrée", _("Livrée")),
            ("Retour", _("Retour")),
        ],
        default="En attente",
    )
    nom_client = models.CharField(max_length=100, blank=False, null=False)
    numero_client = models.CharField(max_length=15, blank=False, null=False)
    prix_total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    type_livraison = models.CharField(
        max_length=30,
        choices=[
            ("Bureau", _("Bureau")),
            ("Domicile", _("Domicile")),
        ],
        default="Bureau",
    )
    Adresse_livraison = models.CharField(max_length=255, blank=True, null=True)
    wilaya = models.CharField(max_length=100, choices=WILAYA_CHOICES,default='Alger', blank=False, null=False)
    commune = models.CharField(max_length=255, blank=True, null=True)
    def clean(self):
        # Stock check
        variant = self.produit_commandé
        if self.pk is None and self.quantite_commandé > variant.quantite:
            raise ValidationError({
                'quantite_commandé': f"Stock insuffisant pour ce produit (stock actuel: {variant.quantite})"
            })
        if self.type_livraison == 'Domicile' and not self.Adresse_livraison:
            raise ValidationError({
                'Adresse_livraison': "Veuillez entrer une adresse de livraison."
            })
        # Phone number check (must be 10 or 11 digits)
        if not re.fullmatch(r'\d{10,11}', self.numero_client or ''):
            raise ValidationError({
                'numero_client': "Entrez un numéro de téléphone réel."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        variant = self.produit_commandé
        if self.pk is None:  # Only on creation
            variant.quantite -= self.quantite_commandé
            variant.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id_commande)
    class Meta:
        indexes = [
                models.Index(fields=['date_commande', 'etat_commande']),
                models.Index(fields=['produit_commandé', 'etat_commande']), 
            ]