from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Products'
    verbose_name = "Gestion des Produits"
    def ready(self):
        import Products.signals
