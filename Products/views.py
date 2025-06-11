import io
import xlsxwriter
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Boutique, Variant
from Orders.models import Commande
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def get_product_price(request, variant_id):
    try:
        variant = Variant.objects.select_related('produit').get(pk=variant_id)
        return JsonResponse({'price': float(variant.produit.prix_produit)})
    except Variant.DoesNotExist:
        return JsonResponse({'price': 0.0})

def telechargement_sheet_view(request):
    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        if action_type == 'download_variants':
            boutique_id = request.POST.get('boutique_id')
            return download_integration_sheet(request, boutique_id)
        elif action_type == 'download_commandes':
            etat_commande = request.POST.get('etat_commande')
            return download_commandes_sheet(request, etat_commande)

     # Get all boutiques for the select dropdown
    boutiques = Boutique.objects.all().order_by('nom_boutique')
    
    # Get command states for the select dropdown (excluding "all" option for verification)
    etat_choices = Commande._meta.get_field('etat_commande').choices
    
    return render(request, 'telechargementsheet.html', {
        "boutiques": boutiques,
        "etat_choices": etat_choices,
        "content": "This is the telechargement sheet page."
    })

def integration_sheet_view(request):
    if request.method == 'POST':
        return verify_commandes_sheet(request)
    nbr_enattente = '-'
    nbr_livre = '-'
    nbr_retour = '-'
    # Get all boutiques for the select dropdown
    boutiques = Boutique.objects.all().order_by('nom_boutique')
    nbr_retour = Commande.objects.filter(etat_commande='Retour').count()
    nbr_livre = Commande.objects.filter(etat_commande='Livrée').count()
    nbr_enattente = Commande.objects.filter(etat_commande='En attente').count()
    # Get command states for the select dropdown (excluding "all" option for verification)
    etat_choices = Commande._meta.get_field('etat_commande').choices
    
    return render(request, 'integration_sheet.html', {
        "boutiques": boutiques,
        "etat_choices": etat_choices,
        "content": "This is the integration sheet page.",
        "nbr_retour": nbr_retour,
        "nbr_livre": nbr_livre,
        "nbr_enattente": nbr_enattente,
    })

def download_integration_sheet(request, boutique_id=None):
    """
    Generate and download Excel file with variant data
    """
    # Create a workbook and add a worksheet
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Variants')
    
    # Define header format
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#D7E4BC',
        'border': 1
    })
    
    # Define cell format
    cell_format = workbook.add_format({
        'border': 1,
        'align': 'left'
    })
    
    # Write headers
    headers = [
        'ID Produit',
        'Nom Produit', 
        'Prix Produit',
        'Quantité',
        'Couleur',
        'Taille'
    ]
    
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Get variants based on boutique selection
    if boutique_id and boutique_id != 'all':
        try:
            boutique = Boutique.objects.get(id_boutique=boutique_id)
            variants = Variant.objects.filter(
                produit__boutique=boutique
            ).select_related('produit', 'couleur', 'taille').order_by('produit__nom_produit')
            filename_suffix = f"_{boutique.nom_boutique}"
        except Boutique.DoesNotExist:
            variants = Variant.objects.none()
            filename_suffix = "_boutique_inexistante"
    else:
        # All boutiques
        variants = Variant.objects.select_related(
            'produit', 'couleur', 'taille'
        ).order_by('produit__nom_produit')
        filename_suffix = "_toutes_boutiques"
    
    # Write data rows
    row = 1
    for variant in variants:
        worksheet.write(row, 0, variant.produit.ID, cell_format)
        worksheet.write(row, 1, variant.produit.nom_produit, cell_format)
        worksheet.write(row, 2, float(variant.produit.prix_produit), cell_format)
        worksheet.write(row, 3, variant.quantite, cell_format)
        worksheet.write(row, 4, variant.couleur.nom_couleur, cell_format)
        worksheet.write(row, 5, variant.taille.nom_taille, cell_format)
        row += 1
    
    # Adjust column widths
    worksheet.set_column('A:A', 12)  # ID Produit
    worksheet.set_column('B:B', 25)  # Nom Produit
    worksheet.set_column('C:C', 15)  # Prix Produit
    worksheet.set_column('D:D', 12)  # Quantité
    worksheet.set_column('E:E', 15)  # Couleur
    worksheet.set_column('F:F', 15)  # Taille
    
    # Close workbook
    workbook.close()
    output.seek(0)
    
    # Create HTTP response
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="integration_sheet{filename_suffix}.xlsx"'
    
    return response

import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect
from Orders.models import Commande  # Adjust to your actual app
from django.utils.html import format_html

def verify_commandes_sheet(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('commandes_sheet')

        if not uploaded_file:
            messages.error(request, "Veuillez sélectionner un fichier.")
            return redirect('integration_sheet')

        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            messages.error(request, f"Erreur de lecture du fichier : {str(e)}")
            return redirect('integration_sheet')

        required_columns = ['ID Commande', 'État Commande']
        if not all(col in df.columns for col in required_columns):
            messages.error(request, "Le fichier doit contenir les colonnes 'ID Commande' et 'État Commande'.")
            return redirect('integration_sheet')

        for _, row in df.iterrows():
            try:
                cmd_id = int(row['ID Commande'])
                new_etat = str(row['État Commande']).strip()

                try:
                    commande = Commande.objects.get(id_commande=cmd_id)
                    old_etat = commande.etat_commande

                    if old_etat == new_etat:
                        messages.info(request, f"🔵 La commande '{cmd_id}' est déjà '{new_etat}'.")
                    else:
                        commande.etat_commande = new_etat
                        commande.save()
                        messages.success(request, f"✅ L'état de la commande '{cmd_id}' a été modifié de '{old_etat}' à '{new_etat}' avec succès.")
                except Commande.DoesNotExist:
                    messages.error(request, f"❌ La commande '{cmd_id}' n'est pas trouvée. Vérifiez SVP.")

            except Exception as e:
                messages.error(request, f"Erreur lors du traitement de la ligne : {str(e)}")

    return redirect('integration_sheet')


def download_commandes_sheet(request, etat_commande=None):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Commandes')

    # Formats
    header_format = workbook.add_format({'bold': True, 'bg_color': '#FFE6CC', 'border': 1})
    cell_format = workbook.add_format({'border': 1, 'align': 'left'})
    date_format = workbook.add_format({'border': 1, 'num_format': 'dd/mm/yyyy'})

    # Headers
    headers = [
        'ID Commande', 'Date Commande', 'Produit Commandé', 'SKU',
        'Boutique', 'État Commande', 'Nom Client', 'Numéro Client', 'Prix Total',
        'Type Livraison', 'Adresse Livraison', 'Wilaya', 'Commune',
        "Bureau Yalidine", "Bureau ZD"
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Build queryset
    commandes = Commande.objects.prefetch_related(
        'produits__produit', 'produits__couleur', 'produits__taille', 'produits__produit__boutique'
    ).order_by('-date_commande')

    if etat_commande and etat_commande != 'all':
        commandes = commandes.filter(etat_commande=etat_commande)

    print(f"[DEBUG] Loaded {commandes.count()} commandes")

    row = 1
    for cmd in commandes:
        produits = list(cmd.produits.all())

        if produits:
            produits_str = ", ".join([
                f"{p.produit.nom_produit}-{p.couleur.nom_couleur}-{p.taille.nom_taille} (x{p.quantite})"
                for p in produits
            ])

            skus = []
            for p in produits:
                variant = p.get_variant()
                skus.append(variant.SKU if variant and variant.SKU else "N/A")
            skus = ", ".join(skus)

            boutique_name = produits[0].produit.boutique.nom_boutique if produits[0].produit.boutique else "N/A"

        else:
            print(f"[DEBUG] Commande {cmd.id_commande} has no ProduitCommande")
            produits_str = "Aucun produit"
            skus = "N/A"
            boutique_name = "N/A"

        print(f"[DEBUG] Writing commande {cmd.id_commande}: {produits_str}")

        worksheet.write(row, 0, cmd.id_commande, cell_format)
        worksheet.write_datetime(row, 1, cmd.date_commande, date_format)
        worksheet.write(row, 2, produits_str, cell_format)
        worksheet.write(row, 3, skus, cell_format)
        worksheet.write(row, 4, boutique_name, cell_format)
        worksheet.write(row, 5, cmd.etat_commande, cell_format)
        worksheet.write(row, 6, cmd.nom_client, cell_format)
        worksheet.write(row, 7, cmd.numero_client, cell_format)
        worksheet.write(row, 8, f"{float(cmd.prix_total)} DZD", cell_format)
        worksheet.write(row, 9, cmd.type_livraison, cell_format)
        worksheet.write(row, 10, cmd.Adresse_livraison or '', cell_format)
        worksheet.write(row, 11, cmd.wilaya, cell_format)
        worksheet.write(row, 12, cmd.commune or '', cell_format)
        worksheet.write(row, 13, cmd.Bureau_Yalidine or '', cell_format)
        worksheet.write(row, 14, cmd.Bureau_ZD or '', cell_format)
        row += 1

    # Column widths
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 45)  # Produits
    worksheet.set_column('D:D', 25)  # SKU
    worksheet.set_column('E:E', 20)  # Boutique
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 20)
    worksheet.set_column('H:H', 20)
    worksheet.set_column('I:I', 25)
    worksheet.set_column('J:J', 15)
    worksheet.set_column('K:K', 25)
    worksheet.set_column('L:L', 25)
    worksheet.set_column('M:M', 25)
    worksheet.set_column('N:N', 25)
    worksheet.set_column('O:O', 25)

    # Return response
    workbook.close()
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    suffix = f"_{etat_commande}" if etat_commande and etat_commande != 'all' else "_tous_etats"
    response['Content-Disposition'] = f'attachment; filename="commandes_sheet{suffix}.xlsx"'
    return response
