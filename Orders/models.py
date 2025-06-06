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
        is_new = self.pk is None
        variant = self.produit_commandé

        if is_new:
            variant.quantite -= self.quantite_commandé
            variant.save()
        else:
            old = Commande.objects.get(pk=self.pk)
            if old.produit_commandé != self.produit_commandé or old.quantite_commandé != self.quantite_commandé:
                variant.quantite += old.quantite_commandé
                variant.quantite -= self.quantite_commandé
                variant.save()

        super().save(*args, **kwargs)

        # Sync with sheet
        if is_new:
            append_commande_to_sheet(self)
        else:
            update_commande_on_sheet(self)
    
    def delete(self, *args, **kwargs):
        sheet_obj = Sheet.objects.first()
        if sheet_obj and sheet_obj.sheet_id:
            delete_commande_from_sheet(self.id_commande, sheet_obj.sheet_id)
        super().delete(*args, **kwargs)


    def __str__(self):
        return str(self.id_commande)

def delete_commande_from_sheet(commande_id, sheet_id):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()

        data = sheet.values().get(
            spreadsheetId=sheet_id,
            range="A2:A"
        ).execute()
        rows = data.get('values', [])

        for idx, row in enumerate(rows, start=2):
            if str(commande_id) == row[0]:
                request = {
                    "requests": [{
                        "deleteDimension": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "ROWS",
                                "startIndex": idx - 1,
                                "endIndex": idx
                            }
                        }
                    }]
                }
                service.spreadsheets().batchUpdate(
                    spreadsheetId=sheet_id,
                    body=request
                ).execute()
                break
    except Exception as e:
        print("Erreur lors de la suppression de Google Sheet:", e)


def update_commande_on_sheet(commande):
    try:
        sheet_obj = Sheet.objects.first()
        if not sheet_obj or not sheet_obj.sheet_id:
            return

        sheet_id = sheet_obj.sheet_id
        service = get_sheets_service()
        sheet = service.spreadsheets()

        produit = commande.produit_commandé.produit
        couleur = commande.produit_commandé.couleur.nom_couleur
        taille = commande.produit_commandé.taille.nom_taille
        sku = f"{produit.id_produit}-{couleur}-{taille}"
        boutique_name = produit.boutique.nom_boutique

        updated_row = [
            str(commande.id_commande),
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
        ]

        # Find row by ID
        data = sheet.values().get(
            spreadsheetId=sheet_id,
            range="A2:A"
        ).execute()
        rows = data.get('values', [])

        for idx, row in enumerate(rows, start=2):
            if str(commande.id_commande) == row[0]:
                range_str = f"A{idx}:P{idx}"
                sheet.values().update(
                    spreadsheetId=sheet_id,
                    range=range_str,
                    valueInputOption="USER_ENTERED",
                    body={'values': [updated_row]}
                ).execute()
                break
    except Exception as e:
        print("Erreur de mise à jour Google Sheet:", e)


def initialize_sheet_headers(sheet_id):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    # Step 1: Add headers
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

    # Step 2: Format the header row (bold + colored background)
    requests = [{
        "repeatCell": {
            "range": {
                "sheetId": 0,
                "startRowIndex": 0,
                "endRowIndex": 1
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 0.2,
                        "green": 0.6,
                        "blue": 0.86
                    },
                    "textFormat": {
                        "bold": True,
                        "foregroundColor": {
                            "red": 1.0,
                            "green": 1.0,
                            "blue": 1.0
                        }
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat)"
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": requests}
    ).execute()

def export_all_commandes_to_sheet(sheet_id):
    from Orders.models import Commande
    service = get_sheets_service()
    sheet = service.spreadsheets()

    commandes = Commande.objects.all().order_by('id_commande')
    rows = []

    for commande in commandes:
        produit = commande.produit_commandé.produit
        couleur = commande.produit_commandé.couleur.nom_couleur
        taille = commande.produit_commandé.taille.nom_taille
        sku = f"{produit.id_produit}-{couleur}-{taille}"
        boutique_name = produit.boutique.nom_boutique

        rows.append([
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
        ])

    body = {'values': rows}

    sheet.values().append(
        spreadsheetId=sheet_id,
        range="A2:P",
        valueInputOption="USER_ENTERED",
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
            export_all_commandes_to_sheet(self.sheet_id)


    @property
    def sheet_id(self):
        import re
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", self.sheet_url)
        return match.group(1) if match else None

