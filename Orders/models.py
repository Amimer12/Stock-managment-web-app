from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from Products.models import Variant
from django.core.exceptions import ValidationError
from decimal import Decimal
import re

# utils.py or models.py if preferred

from Orders.google_sheets import get_sheets_service
from datetime import datetime

def append_commande_to_sheet(commande):
    try:
        sheet_obj = Sheet.objects.first()
        if not sheet_obj:
            return  # No sheet configured
        sheet_id = sheet_obj.sheet_id
        if not sheet_id:
            return

        service = get_sheets_service()
        sheet = service.spreadsheets()
        produit = commande.produit_commandé.produit

        couleur = commande.produit_commandé.couleur.nom_couleur
        taille = commande.produit_commandé.taille.nom_taille
        sku = f"{produit.id_produit}-{couleur}-{taille}"
        boutique_name = produit.boutique.nom_boutique

        values = [[
            commande.id_commande,
            commande.date_commande.strftime('%d/%m/%Y'),
            produit.nom_produit,
            sku,
            boutique_name,
            couleur,
            taille,
            commande.quantite_commandé,
            commande.etat_commande,
            commande.nom_client,
            commande.numero_client,
            f"{float(commande.prix_total)} DZD",
            commande.type_livraison,
            commande.Adresse_livraison or '',
            commande.wilaya,
            commande.commune or ''
        ]]

        body = {
            'values': values
        }

        sheet.values().append(
            spreadsheetId=sheet_id,
            range="A:P",  # 16 columns
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
    except Exception as e:
        print("Erreur lors de l'ajout à Google Sheet:", e)


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
    produit_commandé = models.ForeignKey("Products.Variant", related_name="produit_commandé", on_delete=models.SET_NULL, null=True)
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
        if self.pk is None and variant and self.quantite_commandé > variant.quantite:
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
        is_new = self.pk is None
        if is_new:
            variant.quantite -= self.quantite_commandé
            variant.save()

        super().save(*args, **kwargs)

        if is_new:
            append_commande_to_sheet(self)

    def __str__(self):
        return str(self.id_commande)


def initialize_sheet_headers(sheet_id):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    headers = [[
        "ID", "Date", "Produit", "SKU", "Boutique", "Couleur", "Taille", "Quantité",
        "État", "Nom client", "Téléphone", "Prix total", "Type livraison", "Adresse", "Wilaya", "Commune"
    ]]

    body = {'values': headers}

    sheet.values().update(
        spreadsheetId=sheet_id,
        range="A1:P1",
        valueInputOption="RAW",
        body=body
    ).execute()


class Sheet(models.Model):
    name = models.CharField(max_length=100, help_text="A name or label for the sheet")
    sheet_url = models.URLField(help_text="The full Google Sheets URL")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.sheet_id:
            initialize_sheet_headers(self.sheet_id)

    @property
    def sheet_id(self):
        import re
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", self.sheet_url)
        return match.group(1) if match else None

