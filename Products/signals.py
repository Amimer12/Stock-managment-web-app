from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from .models import Boutique, Produit

# Flag to prevent signal recursion
# _updating_relationships = False

# @receiver(pre_save, sender=Produit)
# def handle_produit_boutique_change(sender, instance, **kwargs):
#     """Handle when a product's boutique is changed"""
#     global _updating_relationships
    
#     if _updating_relationships:
#         return
        
#     # Only process if this is an existing product
#     if not instance.pk:
#         return
    
#     try:
#         old_instance = Produit.objects.get(pk=instance.pk)
#     except Produit.DoesNotExist:
#         return
    
#     # Check if boutique has changed
#     if old_instance.boutique != instance.boutique:
#         _updating_relationships = True
#         try:
#             # Remove from old boutique's liste_produits
#             if old_instance.boutique:
#                 old_instance.boutique.liste_produits.remove(instance)
            
#             # Add to new boutique's liste_produits (if not None)
#             if instance.boutique:
#                 instance.boutique.liste_produits.add(instance)
#         finally:
#             _updating_relationships = False

# @receiver(post_save, sender=Produit)
# def ensure_produit_in_boutique_list(sender, instance, created, **kwargs):
#     """Ensure newly created products are added to their boutique's list"""
#     global _updating_relationships
    
#     if _updating_relationships:
#         return
        
#     if created and instance.boutique:
#         _updating_relationships = True
#         try:
#             # Add the new product to its boutique's liste_produits
#             instance.boutique.liste_produits.add(instance)
#         finally:
#             _updating_relationships = False

# @receiver(m2m_changed, sender=Boutique.liste_produits.through)
# def sync_produit_boutique_from_m2m(sender, instance, action, pk_set, **kwargs):
#     """Sync produit.boutique when liste_produits is modified"""
#     global _updating_relationships
    
#     if _updating_relationships:
#         return
        
#     _updating_relationships = True
#     try:
#         if action == 'post_add' and pk_set:
#             # Products added to the list - update their boutique field and remove from old boutique
#             for pk in pk_set:
#                 try:
#                     produit = Produit.objects.get(pk=pk)
#                     old_boutique = produit.boutique
                    
#                     # If product was in another boutique, remove it from that boutique's list
#                     if old_boutique and old_boutique != instance:
#                         old_boutique.liste_produits.remove(produit)
                    
#                     # Update the product's boutique field
#                     if produit.boutique != instance:
#                         produit.boutique = instance
#                         produit.save(update_fields=['boutique'])
#                 except Produit.DoesNotExist:
#                     continue
                    
#         elif action == 'post_remove' and pk_set:
#             # Products removed from the list - clear their boutique field
#             for pk in pk_set:
#                 try:
#                     produit = Produit.objects.get(pk=pk)
#                     if produit.boutique == instance:
#                         produit.boutique = None
#                         produit.save(update_fields=['boutique'])
#                 except Produit.DoesNotExist:
#                     continue
                    
#         elif action == 'post_clear':
#             # All products removed from the list - clear boutique for all that had this boutique
#             produits = Produit.objects.filter(boutique=instance)
#             for produit in produits:
#                 produit.boutique = None
#                 produit.save(update_fields=['boutique'])
                
#     finally:
#         _updating_relationships = False